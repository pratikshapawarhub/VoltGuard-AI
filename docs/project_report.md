# VoltGuard AI: Intelligent Battery Health & Predictive Maintenance Platform
## Comprehensive Academic Laboratory Project Report
**Department of Computer Science and Engineering (Artificial Intelligence & Machine Learning)**  
**Academic Year:** Third Year B.E. / B.Tech Mini-Project  
**Curriculum Scope:** Comprehensive Implementation & Integration of Practicals 1 through 7  

---

## Executive Summary & Abstract

Electrochemical energy storage systems, primarily Lithium-ion (Li-ion) batteries, serve as the mission-critical foundation for electric mobility (EVs), renewable grid buffering, and aerospace exploration. However, continuous cycling under heterogeneous thermal and mechanical stress triggers irreversible degradation mechanisms—including Solid Electrolyte Interphase (SEI) growth, cathode active material loss, transition metal dissolution, and lithium plating. Unmonitored degradation risks catastrophic failure, notably thermal runaway.

Traditional Battery Management Systems (BMS) rely on static, threshold-based voltage cutoffs that fail to capture non-linear, stochastic aging dynamics. **VoltGuard AI** bridges this critical capability gap by combining classical knowledge-based reasoning, heuristic graph search, constraint satisfaction, supervised continuous regression, multi-class classification, out-of-fold ensemble meta-learning, and unsupervised clustering into an industrial, end-to-end predictive maintenance platform.

The system is rigorously benchmarked on the internationally recognized **NASA Ames Prognostics Center Li-ion Battery Aging Dataset** (Cells `B0005`, `B0006`, `B0007`, and `B0018`), comprising 636 complete charge-discharge cycles. To ensure strict academic discipline and avoid data leakage, a **battery-wise grouped train-test split** was enforced: models were trained on cells B0005, B0006, and B0007, and evaluated strictly on the unseen physical test cell B0018.

---

## 1. Syllabus Practical Traceability Matrix

Every single practical specified in the syllabus has been implemented from first principles and integrated into a unified software architecture:

| Practical | Module Title | AI Branch / Paradigm | Mathematical & Algorithmic Core | Python Source Files | UI Module View |
|:---|:---|:---|:---|:---|:---|
| **Practical 1** | Intelligent Battery Monitoring Agent (PEAS & Expert System) | Knowledge-Based Systems & Agent Architecture | • Russell & Norvig PEAS Specification<br>• Forward-chaining IF-THEN deductive inference engine<br>• Safety-critical overrides and audit trailing | `backend/ml/practical1/peas.py`<br>`backend/ml/practical1/expert_system.py`<br>`backend/app/api/practical1_expert.py` | `PEASAndExpertSystem.jsx` (`/expert-system`) |
| **Practical 2** | Intelligent Battery Maintenance Planner (Search & CSP) | Classical Search & Constraint Optimization | • Breadth-First Search (BFS)<br>• Depth-First Search (DFS)<br>• A* Search with admissible heuristic $h(n)$<br>• Steepest-Ascent Hill Climbing local search<br>• Backtracking CSP with MRV heuristic | `backend/ml/practical2/uninformed_search.py`<br>`backend/ml/practical2/informed_search.py`<br>`backend/ml/practical2/local_search.py`<br>`backend/ml/practical2/csp_solver.py` | `SearchLab.jsx` (`/search-lab`) |
| **Practical 3** | Battery Health & RUL Prediction (Regression) | Supervised Continuous Learning | • Manual Batch Gradient Descent from first principles ($w, b, \nabla J$, MSE)<br>• Ordinary Least Squares Linear Regression<br>• Random Forest Regressor (100 estimators) | `backend/ml/practical3/manual_gradient_descent.py`<br>`backend/ml/practical3/linear_regression.py`<br>`backend/ml/practical3/random_forest_regression.py`<br>`backend/ml/practical3/train_regression.py` | `RegressionAnalysis.jsx` (`/regression`) |
| **Practical 4** | Battery Degradation Classification | Supervised Discrete Multi-Class Learning | • Support Vector Classifier (RBF kernel, Platt probability scaling)<br>• Decision Tree Classifier (Gini impurity criterion)<br>• K-Nearest Neighbors (Euclidean distance, $K=5$)<br>• Gaussian Naive Bayes | `backend/ml/practical4/classifiers.py`<br>`backend/ml/practical4/train_classification.py`<br>`backend/app/api/practical4_classification.py` | `ClassificationAnalysis.jsx` (`/classification`) |
| **Practical 5** | Combined Condition Prediction (Ensemble Learning) | Meta-Learning & Ensemble Methods | • Stacking Meta-Classifier (5-fold Out-Of-Fold CV, L2-regularized Logistic Regression meta-learner)<br>• AdaBoost Adaptive Boosting (50 sequential decision stumps)<br>• Hard Majority Voting Ensemble | `backend/ml/practical5/ensemble_models.py`<br>`backend/ml/practical5/train_ensemble.py`<br>`backend/app/api/practical5_ensemble.py` | `EnsembleAnalysis.jsx` (`/ensemble`) |
| **Practical 6** | Intelligent Battery Usage Segmentation (Clustering) | Unsupervised Pattern Discovery | • Multi-feature K-Means Clustering<br>• Automated WCSS Elbow method sweep ($K=2 \dots 8$)<br>• Silhouette Coefficient evaluation<br>• Davies-Bouldin Index validation | `backend/ml/practical6/kmeans_clustering.py`<br>`backend/ml/practical6/train_clustering.py`<br>`backend/app/api/practical6_clustering.py` | `BatteryClustering.jsx` (`/clustering`) |
| **Practical 7** | Integrated Predictive Maintenance Platform | MLOps & Full-Stack System Integration | • Singleton Multi-Model Registry caching 14 serialized models<br>• SQLite operational telemetry persistence<br>• FastAPI asynchronous REST API<br>• React 18 / Tailwind CSS industrial dark dashboard | `backend/app/engine/model_loader.py`<br>`backend/app/engine/engine.py`<br>`backend/app/main.py`<br>`frontend/src/App.jsx` | `OverviewDashboard.jsx`, `BatteryMonitoring.jsx`, `BatteryHealthPrediction.jsx`, `MaintenanceCenter.jsx` |

---

## 2. Dataset Architecture & Preprocessing Discipline

### 2.1 The NASA Li-ion Prognostics Benchmark
The platform utilizes experimental aging datasets acquired from the **NASA Ames Prognostics Center of Excellence (PCoE)**:
- **Cell Specifications**: Commercial 18650-size Lithium Cobalt Oxide ($\text{LiCoO}_2$) cathode and graphite anode cylindrical cells.
- **Nominal Capacity**: $2.0\,\text{Ahr}$, nominal voltage $3.7\,\text{V}$.
- **Experimental Protocol**:
  - **Charge Protocol**: Standard Constant Current - Constant Voltage (CC-CV) charging at $1.5\,\text{A}$ until cell voltage reaches $4.2\,\text{V}$, followed by voltage hold until current drops below $20\,\text{mA}$.
  - **Discharge Protocol**: Constant Current (CC) discharge at $2.0\,\text{A}$ until cutoff voltage boundaries ($2.7\,\text{V}$ for B0005, $2.5\,\text{V}$ for B0006, $2.2\,\text{V}$ for B0007, $2.5\,\text{V}$ for B0018).
  - **Thermal Conditions**: Tested in controlled temperature chambers at ambient room temperature ($24^\circ\text{C}$).

### 2.2 Feature Engineering
From raw voltage, current, temperature, and time series arrays, 15 engineering telemetry features were extracted per cycle:
1. `cycle_number`: Discrete sequence index of cell aging.
2. `voltage_mean`: Average discharge voltage ($\text{V}$).
3. `voltage_max`: Peak initial terminal voltage ($\text{V}$).
4. `voltage_min`: End-of-discharge cutoff voltage ($\text{V}$).
5. `voltage_std`: Voltage variance across discharge duration.
6. `current_mean`: Mean load current magnitude ($\text{A}$).
7. `current_std`: Current fluctuation standard deviation.
8. `temperature_mean`: Surface thermocouple mean temperature ($^\circ\text{C}$).
9. `temperature_max`: Maximum surface thermal peak ($^\circ\text{C}$).
10. `temperature_min`: Initial rest temperature ($^\circ\text{C}$).
11. `charge_duration`: Preceding CC-CV charge elapsed time ($\text{s}$).
12. `discharge_duration`: Cycle discharge active time ($\text{s}$).
13. `internal_impedance`: Lumped electrolyte and charge transfer resistance ($R_e + R_{ct}$) from EIS spectroscopy ($\Omega$).
14. `capacity`: Extracted discharge capacity in Ampere-hours ($\text{Ahr}$).
15. `recent_soh_drop`: Rolling capacity drop over preceding 5 cycles ($\%$).

### 2.3 Target Derivations
- **State of Health (SOH)**:
  $$\text{SOH}(k) = \frac{C_{\text{discharge}}(k)}{C_{\text{nominal}}} \times 100\% = \frac{C(k)}{2.0\,\text{Ahr}} \times 100\%$$
- **Remaining Useful Life (RUL)**:
  Defined as the number of operational cycles remaining until capacity permanently drops below the certified End-of-Life (EOL) safety threshold ($70.0\%$ SOH, corresponding to $1.40\,\text{Ahr}$):
  $$\text{RUL}(k) = k_{\text{EOL}} - k$$
- **Health State Categorization (4 Discrete Classes)**:
  - **Healthy**: $\text{SOH} \ge 90\%$ (Class 0)
  - **Moderate**: $80\% \le \text{SOH} < 90\%$ (Class 1)
  - **Degraded**: $70\% \le \text{SOH} < 80\%$ (Class 2)
  - **Critical**: $\text{SOH} < 70\%$ (Class 3)

### 2.4 Prevention of Data Leakage (Grouped Split Discipline)
In time-series battery prognostics, standard random cross-validation randomly assigns cycles from the same battery to both train and test splits, causing severe optimistic bias (data leakage). VoltGuard AI enforces a **strict battery-wise split**:
- **Training Set (504 cycles)**: Cells `B0005`, `B0006`, and `B0007`.
- **Test Set (132 cycles)**: Cell `B0018` (completely unseen physical unit).

---

## 3. Practical 1: PEAS Framework & Rule-Based Expert System

### 3.1 Russell & Norvig PEAS Descriptors
- **Performance Measure (P)**:
  - Regression accuracy: SOH $R^2 \ge 0.95$, MAE $\le 2.0\%$; RUL MAE $\le 20$ cycles.
  - Zero false-negative thermal runaway detections ($100\%$ Recall).
  - Cost-optimal repair sequence dispatch ($A^*$ Search).
  - Conflict-free technician schedule generation (CSP).
- **Environment (E)**:
  - Partially observable (internal SEI layer growth and lithium dendrite formation cannot be directly measured non-destructively).
  - Stochastic (ambient thermal gradients and non-linear chemical kinetics).
  - Sequential (current cycle stress irreversibly consumes future lifetime).
  - Dynamic (cell temperature and impedance drift while decisions are being computed).
  - Continuous (voltage, current, and temperature vary continuously in time).
- **Actuators (A)**:
  - High-voltage contactor emergency disconnect relay.
  - BMS charging current throttle ($1.0\text{C} \to 0.5\text{C} \to 0.25\text{C}$).
  - Maintenance work order dispatcher (cell rebalancing, electrolyte reconditioning, cell replacement).
- **Sensors (S)**:
  - Hall-effect current transducers, surface thermocouple probes, precision voltage dividers, Electrochemical Impedance Spectroscopy (EIS) analyzer.

### 3.2 Forward-Chaining Deductive Expert Engine
The expert system contains 9 prioritized production rules evaluated via forward chaining. Safety rules carry override priority over operational rules:
1. `R01 (CRITICAL)`: IF $T_{\text{max}} \ge 42.0^\circ\text{C}$ THEN `EMERGENCY_COOLING_DISCONNECT` (Thermal runaway protection).
2. `R02 (WARNING)`: IF $39.5^\circ\text{C} \le T_{\text{max}} < 42.0^\circ\text{C}$ THEN `THROTTLE_CHARGE_RATE` (Thermal mitigation).
3. `R03 (CRITICAL)`: IF $\text{SOH} \le 70.0\%$ OR $\text{RUL} \le 10$ THEN `REPLACE_CELL_IMMEDIATE` (End of life retirement).
4. `R04 (WARNING)`: IF $70.0\% < \text{SOH} \le 80.0\%$ THEN `FLAG_PREVENTIVE_MAINTENANCE` (Degradation warning).
5. `R05 (CRITICAL)`: IF $Z_{\text{internal}} \ge 0.170\,\Omega$ THEN `ELECTROLYTE_RECONDITION_OR_REPLACE` (Impedance growth).
6. `R06 (WARNING)`: IF $0.145\,\Omega \le Z_{\text{internal}} < 0.170\,\Omega$ THEN `SCHEDULE_EIS_DIAGNOSTICS` (Electrochemical check).
7. `R07 (WARNING)`: IF $\Delta\text{SOH}_{\text{recent}} \ge 1.5\%$ THEN `PERFORM_CELL_REBALANCING` (Capacity drop alert).
8. `R08 (CRITICAL)`: IF $V_{\text{min}} \le 2.20\,\text{V}$ THEN `PREVENT_DEEP_DISCHARGE` (Copper dissolution prevention).
9. `R09 (INFO)`: IF all parameters nominal THEN `CONTINUE_NORMAL_OPERATION`.

---

## 4. Practical 2: Problem Solving through Search & CSP Solver

### 4.1 State-Space Maintenance Graph
The maintenance servicing environment is modeled as a weighted directed graph where nodes denote discrete diagnostic/repair states and edges represent transition costs (labor hours and resources):
- Graph Nodes: `CRITICAL_FAULT`, `EMERGENCY_COOLING`, `ISOLATION`, `THERMAL_STABILIZATION`, `PRELIMINARY_SCAN`, `DIAGNOSTIC_EIS`, `MODULE_DISASSEMBLY`, `ELECTROLYTE_RECONDITIONING`, `CELL_REBALANCING`, `CELL_REPLACEMENT`, `CALIBRATION_TEST`, `CERTIFIED_OPERATIONAL`.

### 4.2 Search Algorithm Comparisons
1. **Breadth-First Search (BFS)**:
   - Traversal: FIFO queue exploring layer by layer.
   - Result: 5 steps, 11 nodes explored, **Total Cost = $170.0**. Step-optimal, but cost-suboptimal.
2. **Depth-First Search (DFS)**:
   - Traversal: LIFO stack exploring deep branches first.
   - Result: 7 steps, 9 nodes explored, **Total Cost = $205.0**. Explores expensive early disassembly paths.
3. **A\* Informed Search**:
   - Evaluation Function: $f(n) = g(n) + h(n)$
   - $g(n)$: Exact path cost accumulated from `CRITICAL_FAULT`.
   - $h(n)$: Admissible heuristic function lower-bounding remaining cost to `CERTIFIED_OPERATIONAL` ($h(n) \le h^*(n)$).
   - Heuristic Table: `CRITICAL_FAULT: 105.0`, `ISOLATION: 90.0`, `PRELIMINARY_SCAN: 65.0`, `CELL_REBALANCING: 45.0`, `CALIBRATION_TEST: 20.0`, `CERTIFIED_OPERATIONAL: 0.0`.
   - Result: 5 steps, 8 nodes explored, **Total Cost = $130.0** (Optimal). A* discovered the lowest-cost repair sequence:
     $$\text{CRITICAL\_FAULT} \to \text{ISOLATION} \to \text{PRELIMINARY\_SCAN} \to \text{CELL\_REBALANCING} \to \text{CALIBRATION\_TEST} \to \text{CERTIFIED\_OPERATIONAL}$$

### 4.3 Hill Climbing Local Search (Fleet Dispatch Optimization)
Minimizes aggregate fleet degradation risk under resource constraints.
- Objective Function:
  $$\text{Risk}(\text{Schedule}) = \sum_{i=1}^N (100 - \text{SOH}_i) \cdot P_i \cdot (i) \cdot 1.5 + \sum_{i=1}^N \max(0, T_i - 38.0) \cdot 15.0$$
- Result: Reduced aggregate fleet risk from **1464.00 to 1008.75** (a **31.1% risk reduction**) in 24 swap iterations.

### 4.4 Backtracking Constraint Satisfaction Problem (CSP) Solver
Assigns scheduled battery tasks to certified technicians and time slots:
- **Variables**: Tasks $\{T_1, T_2, T_3, T_4\}$.
- **Domains**: Cartesian product of Technicians $\{\text{Alice (Senior)}, \text{Bob (Junior)}\} \times \text{Slots} \{09:00, 10:00, 11:00, 14:00\}$.
- **Hard Constraints**:
  1. No technician collision in the same slot.
  2. Critical fault tasks require senior technician certification.
  3. Priority ordering slots critical batteries first.
- **Optimization Heuristic**: Minimum Remaining Values (MRV).
- Result: 100% valid schedule discovered with **0 backtracks** and 4 variable assignments.

---

## 5. Practical 3: Regression Models for SOH & RUL

### 5.1 First-Principles Batch Gradient Descent
Implemented from mathematical scratch without scikit-learn helper wrappers:
- Hypothesis: $\hat{y} = X w + b$
- Loss Function: $J(w, b) = \frac{1}{2m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})^2$
- Analytical Gradients:
  $$\frac{\partial J}{\partial w_j} = \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)}) x_j^{(i)}, \quad \frac{\partial J}{\partial b} = \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})$$
- Parameter Updates:
  $$w := w - \alpha \frac{\partial J}{\partial w}, \quad b := b - \alpha \frac{\partial J}{\partial b}$$
- Hyperparameters: Learning rate $\alpha = 0.01$, max iterations $= 2000$, early stopping $\epsilon = 10^{-6}$.

### 5.2 Comparative Empirical Results (Evaluated on Unseen B0018)

#### State of Health (SOH %) Prediction:
| Regression Model | $R^2$ Score | Mean Absolute Error (MAE) | Mean Squared Error (MSE) | Root Mean Squared Error (RMSE) |
|:---|:---:|:---:|:---:|:---:|
| **Sklearn Linear Regression** | **0.9968** | **0.3421%** | **0.1697** | **0.4119%** |
| **Manual Gradient Descent (Scratch)** | 0.9429 | 1.7610% | 3.0184 | 1.7374% |
| **Random Forest Regressor** | 0.8685 | 2.2642% | 6.9536 | 2.6370% |

#### Remaining Useful Life (RUL Cycles) Prediction:
| Regression Model | $R^2$ Score | Mean Absolute Error (MAE) | Mean Squared Error (MSE) | Root Mean Squared Error (RMSE) |
|:---|:---:|:---:|:---:|:---:|
| **Manual Gradient Descent (Scratch)** | **0.5872** | **18.374 cycles** | **525.26** | **22.918 cycles** |
| **Random Forest Regressor** | 0.5264 | 19.471 cycles | 602.68 | 24.549 cycles |
| **Sklearn Linear Regression** | 0.0532 | 27.954 cycles | 1204.81 | 34.710 cycles |

*Key Takeaway*: Linear Regression fitted the capacity degradation curve almost perfectly ($R^2 = 0.9968$, MAE $< 0.35\%$), while Manual Gradient Descent achieved the best generalization on Remaining Useful Life (MAE $= 18.37$ cycles), meeting the syllabus requirement ($\text{MAE} < 20$ cycles).

---

## 6. Practical 4: Battery Condition Classification

### 6.1 Benchmark Models
Four distinct algorithmic paradigms were evaluated for 4-class health state classification:
1. **Support Vector Machine (SVM)**: Radial Basis Function (RBF) kernel with Platt probability scaling ($\gamma = \text{scale}, C = 1.0$).
2. **Decision Tree Classifier**: CART algorithm with Gini impurity criterion ($\text{max\_depth} = 5$).
3. **K-Nearest Neighbors (KNN)**: $K=5$ nearest neighbors with Euclidean metric.
4. **Gaussian Naive Bayes**: Generative model assuming Gaussian class-conditional feature distributions.

### 6.2 Empirical Classification Metrics (Unseen Test Cell B0018)
| Classifier | Test Accuracy | Macro Precision | Macro Recall | Macro F1-Score | Weighted F1-Score | Log Loss |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Decision Tree** | **71.97%** | **0.6542** | **0.6053** | **0.6090** | **0.6417** | 5.340 |
| **Support Vector Machine (SVM)** | 61.36% | 0.5841 | 0.5376 | 0.5257 | 0.5746 | **1.226** |
| **Gaussian Naive Bayes** | 57.58% | 0.6120 | 0.5694 | 0.4977 | 0.4952 | 2.540 |
| **K-Nearest Neighbors (KNN)** | 38.64% | 0.3015 | 0.3472 | 0.2986 | 0.3705 | 2.381 |

*Key Insight*: Decision Tree achieved top accuracy (71.97%) by partitioning non-linear degradation regimes along impedance and temperature cutoffs. SVM delivered the best probability calibration (lowest log loss: 1.226). KNN struggled on unseen physical cells because baseline resistance shifts create spatial offsets in feature space.

---

## 7. Practical 5: Ensemble Learning

### 7.1 Ensemble Architectures
1. **Stacking Ensemble**:
   - Level 0 (Base Models): SVM, Decision Tree, KNN, Naive Bayes.
   - 5-Fold Stratified Out-Of-Fold Cross-Validation on training data to generate meta-features without leakage.
   - Level 1 (Meta-Learner): $L_2$-regularized Logistic Regression ($C = 1.0$).
2. **AdaBoost Ensemble**:
   - 50 sequential Decision Tree stumps with adaptive sample re-weighting via exponential loss.
3. **Hard Majority Voting Ensemble**:
   - Mode prediction across base classifiers.

### 7.2 7-Model Benchmark Comparison (Unseen Test Cell B0018)
| Model Name | Model Class | Accuracy | Macro F1 | Weighted F1 | Log Loss |
|:---|:---|:---:|:---:|:---:|:---:|
| **Stacking Ensemble** | **Meta-Learner** | **71.97%** | **0.6090** | **0.6417** | **1.1602** |
| **Decision Tree** | Base Model | 71.97% | 0.6090 | 0.6417 | 5.3400 |
| **AdaBoost Ensemble** | Boosting | 68.18% | 0.5636 | 0.6273 | 1.2292 |
| **Hard Voting Ensemble** | Voting | 61.36% | 0.5257 | 0.5746 | N/A |
| **Support Vector Machine (SVM)** | Base Model | 61.36% | 0.5257 | 0.5746 | 1.2260 |
| **Gaussian Naive Bayes** | Base Model | 57.58% | 0.4977 | 0.4952 | 2.5400 |
| **K-Nearest Neighbors (KNN)** | Base Model | 38.64% | 0.2986 | 0.3705 | 2.3810 |

*Key Finding*: While Stacking matched Decision Tree's 71.97% classification accuracy, it reduced the test Log Loss from **5.340 down to 1.1602**—the lowest loss across all 7 evaluated models. The meta-learner effectively neutralized the erratic, overconfident probability spikes of individual trees.

---

## 8. Practical 6: Unsupervised Clustering of Operating Regimes

### 8.1 Multi-Feature K-Means Clustering
Clustering was performed across standardized operational features: SOH, discharge capacity, peak temperature, internal impedance, and cycle number.

### 8.2 Cluster Validation & Elbow Method
- Tested $K \in \{2, 3, 4, 5, 6, 7, 8\}$.
- **Elbow Analysis**: WCSS drop exhibits an elbow inflection at $K=3$ ($\text{WCSS} = 985.64$).
- **Silhouette Coefficient**: $0.3608$ (highest separation among valid operational segmentations).
- **Davies-Bouldin Index**: $1.0584$ (low intra-cluster variance, high inter-cluster distance).

### 8.3 Discovered Operating Regimes
- **Cluster 1 (Fresh Baseline, 34.0% of cycles)**:
  - Mean SOH: $90.74\%$, Internal Impedance: $0.1202\,\Omega$, Max Temperature: $35.4^\circ\text{C}$, Cycle: $29.1$.
  - Characteristics: Rapid CC-CV charging, minimal impedance, nominal operating temperature.
- **Cluster 0 (Active Intermediate Aging, 31.1% of cycles)**:
  - Mean SOH: $77.12\%$, Internal Impedance: $0.1442\,\Omega$, Max Temperature: $37.2^\circ\text{C}$, Cycle: $80.0$.
  - Characteristics: Moderate capacity fade, progressive electrolyte consumption.
- **Cluster 2 (Degraded / High-Impedance EOL, 34.9% of cycles)**:
  - Mean SOH: $69.49\%$, Internal Impedance: $0.1565\,\Omega$, Max Temperature: $39.8^\circ\text{C}$, Cycle: $131.7$.
  - Characteristics: Severe SEI growth, high internal resistance, elevated thermal dissipation.

---

## 9. Practical 7: Integrated Predictive Maintenance Engine & Full Web Application

### 9.1 Unified Multi-Model Inference Pipeline
The integrated engine (`backend/app/engine/engine.py`) binds all preceding practicals into a single transaction:
1. Ingests raw multi-dimensional battery measurement payload (`BatteryMeasurementInput`).
2. Dispatches feature vector to Singleton Model Registry (`model_loader.py`).
3. Executes P3 regression ensemble to predict SOH (%) and RUL (cycles).
4. Dispatches to P4 base classifiers and P5 ensemble meta-classifier for 4-class degradation categorization.
5. Projects features into standardized space and assigns P6 operational regime cluster ID.
6. Fires P1 forward-chaining expert rules against physical telemetry facts.
7. Evaluates P2 $A^*$ search and CSP scheduler if maintenance intervention is mandated.
8. Writes unified diagnostic payload to SQLite persistence database (`voltguard.db`).

### 9.2 Software Architecture & Tech Stack
- **Backend**:
  - Python 3.14 runtime.
  - FastAPI asynchronous web framework with Swagger OpenAPI (`/docs`).
  - SQLAlchemy ORM with SQLite file-based persistence.
  - Pydantic v2 schemas for strict boundary validation.
  - Test suite: 39 automated unit and integration tests passing with 100% success rate.
- **Frontend Dashboard**:
  - React 18 with Vite high-performance bundler.
  - Tailwind CSS dark industrial design theme (`navy-950`, `navy-900`, `cyan-400`, `emerald-400`, `amber-400`, `rose-400`).
  - Recharts responsive visualization engine (loss curves, confusion matrices, elbow plots, cluster scatters).
  - Lucide React icon library.

---

## 10. Verification & Test Suite Summary

The entire backend test suite was executed against real serialized models and SQLite database fixtures:
- `backend/tests/test_preprocessing.py`: 5 tests verifying NASA mat ingestion, 636 cycles, zero NaNs, feature scaling.
- `backend/tests/test_ml_models.py`: 18 tests verifying Manual GD analytical gradient calculations, regression models, classification models, stacking meta-learner, and K-Means clustering.
- `backend/tests/test_search_expert.py`: 7 tests verifying PEAS descriptions, 9 expert rules, BFS/DFS path transitions, A* admissible optimality, and CSP backtracking solver.
- `backend/tests/test_api.py`: 9 integration tests verifying all 8 FastAPI routers and SQLite database transaction persistence.
- **Total Test Result**: **39 passed in 4.72s (100% pass rate)**.

---

## 11. Conclusion & Future Scope

VoltGuard AI successfully demonstrates the full lifecycle of Applied AI engineering for battery energy storage systems:
1. Theoretical formulation of knowledge-based and search agents (Practicals 1 and 2).
2. Grounded implementation of continuous regression from mathematical first principles (Practical 3).
3. Comparative evaluation of discrete multi-class algorithms and ensemble meta-learning (Practicals 4 and 5).
4. Unsupervised clustering of real-world electro-chemical degradation regimes (Practical 6).
5. Industrial deployment into an integrated, interactive web application (Practical 7).

### Future Research Directions:
- **Physics-Informed Neural Networks (PINNs)**: Combining equivalent circuit models (ECM) with deep neural networks.
- **Dynamic C-Rate Validation**: Expanding training distributions to variable high-rate fast-charging protocols ($2\text{C}$ to $4\text{C}$).
- **Edge Deployment**: Compiling trained models to ONNX and deploying on microcontrollers (STM32 / ESP32) for in-vehicle BMS integration.

---
*Report certified for submission to Third Year B.E. / B.Tech Computer Science Engineering (AIML) Examination Committee.*
