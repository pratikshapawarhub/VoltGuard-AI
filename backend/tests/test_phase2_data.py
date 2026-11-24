"""
VoltGuard AI - Phase 2 Dataset & Preprocessing Validation Tests
Validates dataset dimensions, missing values, derived SOH/RUL targets, and battery-wise train-test splits.
"""

import os
import pytest
import numpy as np
import pandas as pd
from backend.ml.preprocessing.data_loader import (
    load_cleaned_dataset,
    get_train_test_split,
    NOMINAL_CAPACITY,
    EOL_CAPACITY_THRESHOLD,
    FEATURE_COLUMNS,
    CLEANED_CSV_PATH
)

def test_cleaned_dataset_exists_and_complete():
    df = load_cleaned_dataset()
    assert os.path.exists(CLEANED_CSV_PATH), "Cleaned CSV file does not exist"
    assert len(df) == 636, f"Expected 636 total records, got {len(df)}"
    assert df['battery_id'].nunique() == 4, "Must contain exactly 4 batteries (B0005, B0006, B0007, B0018)"

def test_no_missing_or_infinite_values():
    df = load_cleaned_dataset()
    assert df.isnull().sum().sum() == 0, "Cleaned dataset contains NaN/null values"
    for col in FEATURE_COLUMNS + ['soh', 'rul']:
        assert np.isfinite(df[col]).all(), f"Column {col} contains infinite or NaN values"

def test_derived_target_calculations():
    df = load_cleaned_dataset()
    # SOH formula verification: SOH = (discharge_capacity / 2.0) * 100
    expected_soh = (df['discharge_capacity'] / NOMINAL_CAPACITY) * 100.0
    np.testing.assert_allclose(df['soh'].values, expected_soh.values, rtol=1e-5)

    # Health category verification
    for _, row in df.iterrows():
        soh_val = row['soh']
        cat = row['health_category']
        if soh_val >= 90.0:
            assert cat == 'Healthy'
        elif soh_val >= 80.0:
            assert cat == 'Moderate'
        elif soh_val >= 70.0:
            assert cat == 'Degraded'
        else:
            assert cat == 'Critical'

    # RUL non-negative verification
    assert (df['rul'] >= 0).all(), "RUL must be non-negative"

def test_battery_wise_train_test_split_no_leakage():
    split = get_train_test_split(train_batteries=['B0005', 'B0006', 'B0007'], test_batteries=['B0018'])

    # Verify battery separation
    train_bats = set(split['train_df']['battery_id'].unique())
    test_bats = set(split['test_df']['battery_id'].unique())

    assert train_bats == {'B0005', 'B0006', 'B0007'}
    assert test_bats == {'B0018'}
    assert len(train_bats.intersection(test_bats)) == 0, "Data leakage detected: battery present in both train and test!"

    # Verify cycle counts: 168 + 168 + 168 = 504 train, 132 test
    assert len(split['X_train']) == 504
    assert len(split['X_test']) == 132

    # Verify Scaler was fitted strictly on train: mean approx 0, std approx 1
    assert np.allclose(np.mean(split['X_train'], axis=0), 0, atol=1e-2)
    assert np.allclose(np.std(split['X_train'], axis=0), 1, atol=1e-2)
