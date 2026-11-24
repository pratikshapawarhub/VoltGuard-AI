"""
VoltGuard AI - NASA Battery Data Extraction & Preprocessing Module
Extracts cycle-level statistical features from raw MATLAB (.mat) files for
cells B0005, B0006, B0007, and B0018.

Implements:
1. Feature extraction from raw discharge, charge, and impedance operations.
2. Ground-truth target derivation:
   - SOH (%): (discharge_capacity / 2.0 Ahr) * 100
   - Health Category: Healthy (>=90%), Moderate (80-90%), Degraded (70-80%), Critical (<70%)
   - RUL (Remaining Useful Life in cycles to EOL threshold of 1.4 Ahr / 70% SOH)
3. Battery-wise grouped train-test split (Train: B0005, B0006, B0007; Test: B0018)
4. Robust feature scaling via StandardScaler (fitted strictly on training set).
"""

import os
import numpy as np
import pandas as pd
import scipy.io
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Tuple, Dict, Any, List

# Verified nominal capacity for NASA 18650 Li-ion cells (Ahr)
NOMINAL_CAPACITY = 2.0
# End-of-life capacity threshold (70% of 2.0 Ahr)
EOL_CAPACITY_THRESHOLD = 1.40

# Project health categories
HEALTH_CATEGORIES = ['Healthy', 'Moderate', 'Degraded', 'Critical']
CATEGORY_TO_LABEL = {'Healthy': 0, 'Moderate': 1, 'Degraded': 2, 'Critical': 3}
LABEL_TO_CATEGORY = {0: 'Healthy', 1: 'Moderate', 2: 'Degraded', 3: 'Critical'}

# Default Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
CLEANED_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "nasa_battery_cleaned.csv")

# Standard ML feature columns for predictions
FEATURE_COLUMNS = [
    'cycle_number',
    'voltage_mean',
    'voltage_max',
    'voltage_min',
    'voltage_std',
    'current_mean',
    'current_std',
    'temperature_mean',
    'temperature_max',
    'temperature_min',
    'charge_duration',
    'discharge_duration',
    'internal_impedance'
]


def extract_cycle_features_from_mat(file_path: str, battery_id: str) -> pd.DataFrame:
    """
    Parses a single NASA .mat file and extracts structured cycle-level tabular records.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    mat = scipy.io.loadmat(file_path)
    if battery_id not in mat:
        raise KeyError(f"Key {battery_id} not found in {file_path}")

    cycle_ops = mat[battery_id][0, 0]['cycle'][0]
    
    records = []
    current_impedance = 0.10  # Baseline internal impedance fallback (Ohms)
    last_charge_duration = 3600.0  # Baseline fallback charge duration in sec
    discharge_cycle_num = 0

    # Sequential pass through operations to link charge/impedance/discharge steps
    for op in cycle_ops:
        op_type = str(op['type'][0])
        op_data = op['data'][0, 0]

        if op_type == 'impedance':
            try:
                # Re: Electrolyte resistance, Rct: Charge transfer resistance
                re = float(op_data['Re'].flatten()[0]) if 'Re' in op_data.dtype.names else 0.05
                rct = float(op_data['Rct'].flatten()[0]) if 'Rct' in op_data.dtype.names else 0.05
                current_impedance = float(np.real(re + rct))
                if np.isnan(current_impedance) or current_impedance <= 0:
                    current_impedance = 0.10
            except Exception:
                pass

        elif op_type == 'charge':
            try:
                time_arr = op_data['Time'].flatten()
                last_charge_duration = float(time_arr[-1] - time_arr[0])
            except Exception:
                pass

        elif op_type == 'discharge':
            try:
                discharge_cycle_num += 1
                cap = float(op_data['Capacity'].flatten()[0])
                voltages = op_data['Voltage_measured'].flatten()
                currents = np.abs(op_data['Current_measured'].flatten())
                temps = op_data['Temperature_measured'].flatten()
                time_arr = op_data['Time'].flatten()

                v_mean = float(np.mean(voltages))
                v_max = float(np.max(voltages))
                v_min = float(np.min(voltages))
                v_std = float(np.std(voltages))

                i_mean = float(np.mean(currents))
                i_std = float(np.std(currents))

                t_mean = float(np.mean(temps))
                t_max = float(np.max(temps))
                t_min = float(np.min(temps))

                d_duration = float(time_arr[-1] - time_arr[0])
                ambient_temp = float(op['ambient_temperature'][0, 0]) if 'ambient_temperature' in op.dtype.names else 24.0

                records.append({
                    'battery_id': battery_id,
                    'cycle_number': discharge_cycle_num,
                    'ambient_temperature': ambient_temp,
                    'discharge_capacity': cap,
                    'voltage_mean': v_mean,
                    'voltage_max': v_max,
                    'voltage_min': v_min,
                    'voltage_std': v_std,
                    'current_mean': i_mean,
                    'current_std': i_std,
                    'temperature_mean': t_mean,
                    'temperature_max': t_max,
                    'temperature_min': t_min,
                    'charge_duration': last_charge_duration,
                    'discharge_duration': d_duration,
                    'internal_impedance': current_impedance
                })
            except Exception as e:
                # Log and skip corrupted cycle record
                print(f"Warning: Skipped corrupted cycle in {battery_id}: {e}")

    df = pd.DataFrame(records)

    # Compute End-of-Life cycle for RUL derivation
    # Find cycle where capacity drops <= EOL_CAPACITY_THRESHOLD (1.40 Ahr)
    eol_cycle = None
    for _, row in df.iterrows():
        if row['discharge_capacity'] <= EOL_CAPACITY_THRESHOLD:
            eol_cycle = row['cycle_number']
            break

    # If battery didn't drop below threshold (e.g. B0007), project using degradation slope
    if eol_cycle is None:
        last_cycles = df.tail(30)
        slope = (last_cycles['discharge_capacity'].iloc[-1] - last_cycles['discharge_capacity'].iloc[0]) / len(last_cycles)
        if slope < 0:
            remaining_to_drop = last_cycles['discharge_capacity'].iloc[-1] - EOL_CAPACITY_THRESHOLD
            needed_cycles = int(np.ceil(remaining_to_drop / abs(slope)))
            eol_cycle = df['cycle_number'].iloc[-1] + needed_cycles
        else:
            eol_cycle = df['cycle_number'].iloc[-1] + 20

    # Calculate State of Health (SOH)
    df['soh'] = (df['discharge_capacity'] / NOMINAL_CAPACITY) * 100.0

    # Calculate Remaining Useful Life (RUL)
    df['rul'] = df['cycle_number'].apply(lambda c: max(0, int(eol_cycle - c)))

    # Assign Health Category
    def categorize_health(soh_val: float) -> str:
        if soh_val >= 90.0:
            return 'Healthy'
        elif soh_val >= 80.0:
            return 'Moderate'
        elif soh_val >= 70.0:
            return 'Degraded'
        else:
            return 'Critical'

    df['health_category'] = df['soh'].apply(categorize_health)
    df['health_category_encoded'] = df['health_category'].map(CATEGORY_TO_LABEL)

    return df


def generate_cleaned_dataset(save_path: str = CLEANED_CSV_PATH) -> pd.DataFrame:
    """
    Extracts and merges all 4 NASA cells (B0005, B0006, B0007, B0018) into a unified CSV.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    all_dfs = []

    batteries = ['B0005', 'B0006', 'B0007', 'B0018']
    for b in batteries:
        mat_path = os.path.join(RAW_DATA_DIR, f"{b}.mat")
        df_b = extract_cycle_features_from_mat(mat_path, b)
        print(f"Extracted {len(df_b)} cycles from {b}. Initial SOH: {df_b['soh'].iloc[0]:.2f}%, Final SOH: {df_b['soh'].iloc[-1]:.2f}%")
        all_dfs.append(df_b)

    full_df = pd.concat(all_dfs, ignore_index=True)

    # Validate dataset integrity
    assert full_df.isnull().sum().sum() == 0, "Missing values detected in cleaned dataset!"
    assert len(full_df) == 636, f"Expected 636 total cycles, got {len(full_df)}"

    full_df.to_csv(save_path, index=False)
    print(f"\nSuccessfully generated {save_path} with shape {full_df.shape}")
    return full_df


def load_cleaned_dataset(csv_path: str = CLEANED_CSV_PATH) -> pd.DataFrame:
    """
    Loads the structured dataset from CSV, generating it from raw .mat files if missing.
    """
    if not os.path.exists(csv_path):
        return generate_cleaned_dataset(csv_path)
    return pd.read_csv(csv_path)


def get_train_test_split(
    csv_path: str = CLEANED_CSV_PATH,
    train_batteries: List[str] = ['B0005', 'B0006', 'B0007'],
    test_batteries: List[str] = ['B0018']
) -> Dict[str, Any]:
    """
    Splits dataset battery-wise to prevent data leakage between cycles of the same battery.
    Returns scaled features and targets for Regression (SOH, RUL) and Classification.
    """
    df = load_cleaned_dataset(csv_path)

    train_mask = df['battery_id'].isin(train_batteries)
    test_mask = df['battery_id'].isin(test_batteries)

    df_train = df[train_mask].copy()
    df_test = df[test_mask].copy()

    X_train_raw = df_train[FEATURE_COLUMNS].values
    X_test_raw = df_test[FEATURE_COLUMNS].values

    # Fit scaler strictly on training set to avoid data leakage
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)

    y_soh_train = df_train['soh'].values
    y_soh_test = df_test['soh'].values

    y_rul_train = df_train['rul'].values
    y_rul_test = df_test['rul'].values

    y_cat_train = df_train['health_category_encoded'].values
    y_cat_test = df_test['health_category_encoded'].values

    return {
        'X_train': X_train,
        'X_test': X_test,
        'X_train_raw': X_train_raw,
        'X_test_raw': X_test_raw,
        'y_soh_train': y_soh_train,
        'y_soh_test': y_soh_test,
        'y_rul_train': y_rul_train,
        'y_rul_test': y_rul_test,
        'y_cat_train': y_cat_train,
        'y_cat_test': y_cat_test,
        'feature_columns': FEATURE_COLUMNS,
        'scaler': scaler,
        'train_df': df_train,
        'test_df': df_test,
        'full_df': df
    }


if __name__ == "__main__":
    df = generate_cleaned_dataset()
    print("\nDataset Summary Statistics:")
    print(df[FEATURE_COLUMNS + ['soh', 'rul']].describe().round(3).T)
