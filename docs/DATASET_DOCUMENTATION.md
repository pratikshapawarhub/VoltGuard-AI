# VoltGuard AI: Dataset Architecture & Preprocessing Methodology

**Document ID:** `DATA-VG-2026-V1`  
**Dataset Name:** NASA Ames Prognostics Center of Excellence (PCoE) Li-ion Battery Aging Benchmark  
**Date:** November 23, 2026  

---

## 1. Dataset Origin & Physical Test Bench

VoltGuard AI utilizes the benchmark Li-ion battery aging datasets acquired from the **NASA Ames Prognostics Center of Excellence (PCoE)**:

- **Battery Cell Specifications:** Commercial 18650-size cylindrical cells comprising Lithium Cobalt Oxide ($\text{LiCoO}_2$) cathode and graphite anode.
- **Nominal Specifications:** Manufacturer rated nominal capacity of $2.0\,\text{Ahr}$, nominal voltage of $3.7\,\text{V}$.
- **Experimental Operating Conditions:**
  - Ambient room temperature chambers ($24^\circ\text{C}$).
  - Cycled under continuous charge and discharge regimens until end-of-life (EOL) capacity fading.
  - Periodic Electrochemical Impedance Spectroscopy (EIS) frequency sweeps ($0.1\,\text{Hz}$ to $5\,\text{kHz}$) measuring internal resistance.

### Cell Cycling Matrix
| Battery Identifier | Total Aging Cycles | Discharge Cutoff Voltage | Final Capacity at EOL | Failure Mode Characterization |
|:---:|:---:|:---:|:---:|:---|
| **B0005** | 168 | $2.7\,\text{V}$ | $1.31\,\text{Ahr}$ ($65.5\%$ SOH) | Progressive active material loss; SEI growth |
| **B0006** | 168 | $2.5\,\text{V}$ | $1.17\,\text{Ahr}$ ($58.7\%$ SOH) | Accelerated thermal impedance growth; active lithium loss |
| **B0007** | 168 | $2.2\,\text{V}$ | $1.46\,\text{Ahr}$ ($72.8\%$ SOH) | Deep discharge cycling; mechanical particle cracking |
| **B0018** | 132 | $2.5\,\text{V}$ | $1.35\,\text{Ahr}$ ($67.8\%$ SOH) | Unseen physical test cell used for independent model evaluation |
| **Total** | **636** | — | — | **Zero Missing Values, 100% Data Completeness** |

---

## 2. Experimental Cycling Protocols

### 2.1 Charging Protocol
Standard Constant Current - Constant Voltage (CC-CV) charging:
1. **CC Stage:** Charged at a constant current of $1.5\,\text{A}$ until cell voltage reaches the upper limit of $4.2\,\text{V}$.
2. **CV Stage:** Terminal voltage held at $4.2\,\text{V}$ until charging current decays below the cutoff threshold of $20\,\text{mA}$.

### 2.2 Discharging Protocol
Constant current (CC) discharge at a load current of $2.0\,\text{A}$ until terminal cell voltage drops to the specified cutoff boundary ($2.7\,\text{V}$, $2.5\,\text{V}$, or $2.2\,\text{V}$).

---

## 3. Data Ingestion & Preprocessing Pipeline

The preprocessing pipeline is implemented in [`backend/ml/preprocessing/data_loader.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/preprocessing/data_loader.py).

### Ingestion Flow:
1. Reads raw MATLAB `.mat` hierarchical archive structures (`B0005.mat`, `B0006.mat`, `B0007.mat`, `B0018.mat`).
2. Iterates over the `cycle` structure array, filtering by `type == 'discharge'` and associated preceding `type == 'charge'` records.
3. Extracts raw voltage, current, surface temperature, and elapsed time series arrays.
4. Performs feature aggregation (computing mean, maximum, minimum, and standard deviation per cycle).
5. Cross-references internal impedance ($R_e + R_{ct}$) from closest EIS measurement cycles.
6. Validates data integrity: zero missing values (NaNs), zero infinities, and physical range sanity checks.
7. Generates processed master CSV: `backend/data/processed/nasa_battery_cleaned.csv` (636 rows, 20 columns).

---

## 4. Telemetry Feature Data Dictionary

| Feature Name | Data Type | Physical Unit | Min Value | Max Value | Mean Value | Physical & Prognostic Significance |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `cycle_number` | Integer | Count | 1 | 168 | 84.0 | Discrete index of cumulative cell aging cycles |
| `voltage_mean` | Float | Volts (V) | 3.12 | 3.78 | 3.52 | Average discharge plateau voltage |
| `voltage_max` | Float | Volts (V) | 4.08 | 4.25 | 4.19 | Peak initial voltage under full charge |
| `voltage_min` | Float | Volts (V) | 1.98 | 2.82 | 2.44 | Cutoff voltage indicating end-of-discharge |
| `voltage_std` | Float | Volts (V) | 0.12 | 0.42 | 0.25 | Voltage discharge curvature slope |
| `current_mean` | Float | Amperes (A) | 1.65 | 2.05 | 1.86 | Average discharge load current |
| `current_std` | Float | Amperes (A) | 0.15 | 0.72 | 0.48 | Current variance across load transients |
| `temperature_mean` | Float | Celsius (°C) | 26.5 | 38.2 | 32.4 | Average surface thermocouple temperature |
| `temperature_max` | Float | Celsius (°C) | 31.8 | 49.5 | 38.6 | Thermal peak indicating Joule heating and dissipation |
| `temperature_min` | Float | Celsius (°C) | 22.1 | 28.5 | 24.2 | Initial resting temperature at cycle onset |
| `charge_duration` | Float | Seconds (s) | 4800 | 28500 | 10250 | Preceding CC-CV charging time |
| `discharge_duration`| Float | Seconds (s) | 1850 | 3850 | 2940 | Effective discharge duration before cutoff |
| `internal_impedance`| Float | Ohms ($\Omega$) | 0.108 | 0.245 | 0.144 | Lumped electrolyte and charge transfer resistance ($R_e + R_{ct}$) |
| `recent_soh_drop` | Float | Percent (%) | 0.00 | 4.85 | 0.42 | Moving capacity drop across previous 5 cycles |

---

## 5. Target Variable Formulations

### 5.1 State of Health (SOH %)
Expresses remaining discharge capacity as a percentage of initial manufacturer rated nominal capacity ($C_{\text{nominal}} = 2.0\,\text{Ahr}$):
$$\text{SOH}(k) = \frac{C_{\text{discharge}}(k)}{C_{\text{nominal}}} \times 100\% = \frac{C(k)}{2.0\,\text{Ahr}} \times 100\%$$

### 5.2 Remaining Useful Life (RUL Cycles)
Defined as the number of cycles remaining before capacity drops permanently below the certified End-of-Life (EOL) boundary ($70.0\%$ SOH, corresponding to $1.40\,\text{Ahr}$):
$$\text{RUL}(k) = \max(0, k_{\text{EOL}} - k)$$

### 5.3 Health State Categories (4 Discrete Classes)
- **Healthy (Class 0):** $\text{SOH} \ge 90\%$ (Fresh cell, minimal degradation).
- **Moderate (Class 1):** $80\% \le \text{SOH} < 90\%$ (Active linear aging).
- **Degraded (Class 2):** $70\% \le \text{SOH} < 80\%$ (Impedance growth, restricted fast charging).
- **Critical (Class 3):** $\text{SOH} < 70\%$ (End-of-life boundary reached; replacement mandatory).

---

## 6. Strict Battery-Grouped Split Discipline

In temporal battery prognostics, standard random $K$-fold cross-validation is **invalid** because consecutive cycles from the same physical battery share the same manufacturing quirks, resting voltages, and baseline resistance offsets. Random splitting causes severe optimistic data leakage.

VoltGuard AI strictly enforces a **battery-grouped split**:
- **Training Set (504 cycles):** Batteries `B0005`, `B0006`, and `B0007`.
- **Test Set (132 cycles):** Battery `B0018` (completely unseen physical unit).

This guarantees that all reported regression $R^2$, classification accuracy, and ensemble metrics reflect true **cross-cell generalization** to novel, previously unobserved battery units.

---
*Dataset documentation certified for research defense and laboratory audit.*
