# VoltGuard AI: Academic Practical Implementation Mapping
## Direct 1-to-1 Curriculum Traceability Matrix

**Course:** Third Year B.E. / B.Tech Computer Science Engineering (AIML)  
**Laboratory Scope:** Comprehensive Implementation & Full-Stack Integration of Practicals 1 through 7  
**System Name:** VoltGuard AI – Intelligent Battery Health & Predictive Maintenance Platform  
**Date:** November 23, 2026  

---

## 1. High-Level Practical-to-Product Summary

| Syllabus Practical | Commercial Product Module | Core Algorithmic Techniques | Primary Source File | UI Navigation Path |
|:---|:---|:---|:---|:---|
| **Practical 1: PEAS & Expert System** | Intelligent Battery Monitoring Agent | Russell & Norvig PEAS Specification, Forward-chaining production rules, Priority safety overrides | [`expert_system.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical1/expert_system.py) | **Alerts Center** & **Health Monitoring** |
| **Practical 2: Search Algorithms & CSP** | Predictive Maintenance Planner | BFS, DFS, A* with admissible heuristic, Hill Climbing local search, Backtracking CSP with MRV | [`informed_search.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical2/informed_search.py) | **Maintenance Center** |
| **Practical 3: Regression Models** | SOH & RUL Prognosis Engine | First-principles Manual Batch Gradient Descent, Sklearn Linear Regression, Random Forest | [`manual_gradient_descent.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical3/manual_gradient_descent.py) | **Predictive Intelligence** |
| **Practical 4: Classification** | Battery Condition Assessment | Support Vector Classifier (RBF kernel), Decision Tree, K-Nearest Neighbors, Naive Bayes | [`classifiers.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical4/classifiers.py) | **Predictive Intelligence** |
| **Practical 5: Ensemble Learning** | Combined Prediction Engine | 5-Fold Out-Of-Fold Stacking Meta-Learner (Logistic Regression), AdaBoost, Hard Voting | [`ensemble_models.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical5/ensemble_models.py) | **Predictive Intelligence** |
| **Practical 6: Clustering** | Battery Usage Segmentation | Multi-feature K-Means clustering, Automated WCSS Elbow sweep, Silhouette & Davies-Bouldin | [`kmeans_clustering.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical6/kmeans_clustering.py) | **Analytics & Regimes** |
| **Practical 7: Integrated Platform** | Complete VoltGuard AI Platform | Unified multi-model inference pipeline, Singleton Registry, SQLite persistence, React 18 UI | [`engine.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/app/engine/engine.py) | **Full Application** |

---

## 2. Detailed Practical Technical Dossiers

### Practical 1: PEAS Descriptors and Rule-Based Expert System

1. **Practical Objective:** Specify the intelligent battery agent's performance, environment, actuators, and sensors (PEAS). Implement a rule-based expert system that performs forward-chaining deductive inference over battery telemetry to detect critical anomalies and issue prescriptive maintenance directives.
2. **Product Feature Integration:** Integrated into the **Intelligent Battery Monitoring Agent**, powering automated alert generation in the **Alerts & Notifications Center** and the **Health Monitoring** module.
3. **Algorithms Implemented:**
   - Russell & Norvig PEAS agent matrix.
   - Forward-chaining deductive production rule engine.
   - Configurable safety thresholds with hierarchical priority overrides (Critical > Warning > Info).
4. **Exact Python Source Files:**
   - [`backend/ml/practical1/expert_system.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical1/expert_system.py)
   - [`backend/ml/practical1/peas.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical1/peas.py)
   - [`backend/app/api/practical1_expert.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/app/api/practical1_expert.py)
5. **Main Functions & Methods:**
   - `BatteryExpertSystem.evaluate(facts, config)`
   - `Rule.evaluate(facts, config)`
   - `get_peas_description()`
6. **Input Data:**
   - Operational telemetry facts: `soh` (float %), `temperature_max` (°C), `internal_impedance` ($\Omega$), `voltage_min` (V), `voltage_max` (V), `recent_soh_drop` (float %).
7. **Output:**
   - `ExpertSystemResponse`: `overall_status` (`CRITICAL`, `WARNING`, `NORMAL`), `condition_summary`, `triggered_rules_count`, `triggered_rules` array, prescriptive `action_code` strings, and complete audit trail.
8. **Evaluation Method:**
   - Tested across nominal, high-temperature, degraded capacity, and impedance growth operating points. Achieved 100% recall on thermal runaway and deep discharge fault states.
9. **Execution Evidence:**
   - Serialized verification in automated test suite: `backend/tests/test_practical1_expert.py` (5 tests passing).
10. **Screenshot / Figure Reference:**
    - [`docs/figures/soh_degradation_curves.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/soh_degradation_curves.png)

---

### Practical 2: Problem Solving through Search & CSP Optimization

1. **Practical Objective:** Formulate battery maintenance planning as graph search and constraint satisfaction problems. Implement uninformed search (BFS, DFS), informed search (A* with admissible heuristic), local search (Hill Climbing), and CSP search with backtracking and MRV.
2. **Product Feature Integration:** Integrated into the **Predictive Maintenance Center**, driving cost-optimal work order path generation and conflict-free technician slot scheduling.
3. **Algorithms Implemented:**
   - **Breadth-First Search (BFS):** FIFO queue searching for step-optimal paths.
   - **Depth-First Search (DFS):** LIFO stack exploring deep diagnostic branches.
   - **A\* Search:** Priority queue evaluation via $f(n) = g(n) + h(n)$ with admissible heuristic $h(n) \le h^*(n)$.
   - **Steepest-Ascent Hill Climbing:** Pairwise swap local search minimizing cumulative fleet failure risk.
   - **Backtracking CSP Solver:** Minimum Remaining Values (MRV) heuristic enforcing technician collision, qualification, and priority slot constraints.
4. **Exact Python Source Files:**
   - [`backend/ml/practical2/informed_search.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical2/informed_search.py)
   - [`backend/ml/practical2/uninformed_search.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical2/uninformed_search.py)
   - [`backend/ml/practical2/local_search.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical2/local_search.py)
   - [`backend/ml/practical2/csp_solver.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical2/csp_solver.py)
5. **Main Functions & Methods:**
   - `run_a_star(start_state, goal_state)`
   - `run_bfs(start_state, goal_state)`
   - `run_dfs(start_state, goal_state)`
   - `BatteryMaintenanceHillClimbing.optimize_schedule(batteries)`
   - `MaintenanceCSPSolver.solve()`
6. **Input Data:**
   - Maintenance state transition graph (12 nodes, directed weighted edges), admissible heuristic lower-bound cost table, technician roster and time slot constraints.
7. **Output:**
   - Optimal path sequence, step count, total path cost ($), nodes explored, execution time (ms), optimized schedule risk score, and conflict-free technician assignment table.
8. **Evaluation Method:**
   - A* discovered the lowest-cost repair sequence at **$130.0** (vs BFS $170.0 and DFS $205.0). Hill climbing reduced fleet delay risk by **31.1%** in 24 iterations. Backtracking CSP solver generated a 100% valid schedule with **0 backtracks**.
9. **Execution Evidence:**
   - Benchmarks saved to `backend/saved_models/search_comparison.json`; verified in `backend/tests/test_practical2_search.py` (5 tests passing).
10. **Screenshot / Figure Reference:**
    - Live search workbench in **Maintenance Center** and academic view.

---

### Practical 3: Regression Model Evaluation for SOH & RUL Prognosis

1. **Practical Objective:** Build and evaluate continuous regression models to predict State of Health (SOH %) and Remaining Useful Life (RUL cycles). Implement first-principles manual Batch Gradient Descent without machine learning libraries, and compare against Sklearn Linear Regression and Random Forest.
2. **Product Feature Integration:** Integrated into **Predictive Intelligence** (Module 4) for continuous health and lifespan estimation.
3. **Algorithms Implemented:**
   - **Manual Batch Gradient Descent:** Analytical gradient calculation:
     $$\frac{\partial J}{\partial w_j} = \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)}) x_j^{(i)}, \quad \frac{\partial J}{\partial b} = \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})$$
   - **Ordinary Least Squares (OLS) Linear Regression.**
   - **Random Forest Regressor:** 100 ensemble trees with bootstrap aggregation.
4. **Exact Python Source Files:**
   - [`backend/ml/practical3/manual_gradient_descent.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical3/manual_gradient_descent.py)
   - [`backend/ml/practical3/linear_regression.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical3/linear_regression.py)
   - [`backend/ml/practical3/random_forest_regression.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical3/random_forest_regression.py)
   - [`backend/ml/practical3/train_regression.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical3/train_regression.py)
5. **Main Functions & Methods:**
   - `ManualGradientDescentRegressor.fit(X, y)`
   - `ManualGradientDescentRegressor.predict(X)`
   - `train_and_evaluate_regression_models()`
6. **Input Data:**
   - 13 operational features scaled via `StandardScaler`: cycle number, voltage statistics, load current statistics, thermal measurements, discharge duration, and impedance.
7. **Output:**
   - Predicted SOH (%), predicted RUL (cycles), and model performance metrics (MAE, MSE, RMSE, $R^2$).
8. **Evaluation Method:**
   - Evaluated strictly on the unseen test cell B0018:
     - SOH Prediction: Sklearn LR $R^2 = 0.9968$, $\text{MAE} = 0.342\%$; Manual GD $R^2 = 0.9429$, $\text{MAE} = 1.761\%$.
     - RUL Prediction: Manual GD $R^2 = 0.5872$, $\text{MAE} = 18.374$ cycles (beating the academic goal of $<20$ cycles).
9. **Execution Evidence:**
   - Models saved to `backend/saved_models/soh_manual_gd.joblib`, `rul_manual_gd.joblib`, metrics in `regression_metrics.json`; verified in `test_practical3_regression.py`.
10. **Screenshot / Figure Reference:**
    - [`docs/figures/actual_vs_predicted_soh.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/actual_vs_predicted_soh.png)
    - [`docs/figures/gradient_descent_loss_curve.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/gradient_descent_loss_curve.png)
    - [`docs/figures/regression_models_comparison.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/regression_models_comparison.png)

---

### Practical 4: Classification Models for Degradation States

1. **Practical Objective:** Classify battery operating health into four discrete operational categories: Healthy ($\ge 90\%$), Moderate ($80\text{--}90\%$), Degraded ($70\text{--}80\%$), and Critical ($< 70\%$). Evaluate four distinct classification paradigms.
2. **Product Feature Integration:** Integrated into **Predictive Intelligence** (Module 4) under Battery Condition Assessment.
3. **Algorithms Implemented:**
   - **Support Vector Machine (SVM):** RBF kernel with Platt probability scaling.
   - **Decision Tree Classifier:** CART recursive partitioning with Gini impurity criterion.
   - **K-Nearest Neighbors (KNN):** $K=5$ nearest neighbors with Euclidean distance metric.
   - **Gaussian Naive Bayes:** Generative maximum likelihood with Gaussian class-conditional density.
4. **Exact Python Source Files:**
   - [`backend/ml/practical4/classifiers.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical4/classifiers.py)
   - [`backend/ml/practical4/train_classification.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical4/train_classification.py)
5. **Main Functions & Methods:**
   - `BatterySVMClassifier.fit()`, `predict()`, `predict_proba()`
   - `BatteryDecisionTreeClassifier.fit()`, `predict()`, `predict_proba()`
   - `train_and_evaluate_classifiers()`
6. **Input Data:**
   - Standardized 13-feature operational vector per cycle; target 4-class categorical labels.
7. **Output:**
   - Predicted class (Healthy, Moderate, Degraded, Critical), class index (0..3), and calibrated posterior class probabilities.
8. **Evaluation Method:**
   - Cross-cell evaluation on unseen B0018:
     - Decision Tree: Accuracy **71.97%**, Macro F1 **0.6090**, Weighted F1 **0.6417**.
     - SVM: Accuracy **61.36%**, Macro F1 **0.5257**, Log Loss **1.226** (best probability calibration).
9. **Execution Evidence:**
   - Serialized in `backend/saved_models/classification_decision_tree.joblib`, metrics in `classification_metrics.json`; verified in `test_practical4_classification.py`.
10. **Screenshot / Figure Reference:**
    - [`docs/figures/confusion_matrices_all_classifiers.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/confusion_matrices_all_classifiers.png)
    - [`docs/figures/classification_models_comparison.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/classification_models_comparison.png)

---

### Practical 5: Ensemble Learning (Stacking, AdaBoost, Voting)

1. **Practical Objective:** Combine multiple base classifiers using advanced ensemble architectures to improve classification accuracy, reduce variance, and minimize predictive log loss without data leakage.
2. **Product Feature Integration:** Integrated into **Predictive Intelligence** (Module 4) under Combined Prediction Engine & Multi-Model Consensus.
3. **Algorithms Implemented:**
   - **Stacking Meta-Classifier:** 5-fold stratified out-of-fold cross-validation generating base model prediction vectors (SVM, Decision Tree, KNN, Naive Bayes), feeding an $L_2$-regularized Logistic Regression meta-classifier.
   - **AdaBoost Ensemble:** 50 sequential decision stumps with adaptive sample re-weighting.
   - **Hard Majority Voting Classifier:** Consensus mode voting across base classifiers.
4. **Exact Python Source Files:**
   - [`backend/ml/practical5/ensemble_models.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical5/ensemble_models.py)
   - [`backend/ml/practical5/train_ensemble.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical5/train_ensemble.py)
5. **Main Functions & Methods:**
   - `BatteryStackingEnsemble.fit()`, `predict()`, `predict_proba()`
   - `BatteryAdaBoostEnsemble.fit()`, `predict()`
   - `BatteryVotingEnsemble.fit()`, `predict()`
6. **Input Data:**
   - Base model class probability vectors $[P(\text{Healthy}), P(\text{Moderate}), P(\text{Degraded}), P(\text{Critical})]$.
7. **Output:**
   - Stacking consensus prediction, AdaBoost prediction, Voting prediction, and meta-learner calibrated probabilities.
8. **Evaluation Method:**
   - Side-by-side benchmark across 7 models on unseen cell B0018:
     - Stacking Ensemble achieved top Accuracy (**71.97%**) and the **lowest Log Loss (1.1602)** among all 7 evaluated models, effectively neutralizing overconfident tree leaf probabilities.
9. **Execution Evidence:**
   - Serialized in `backend/saved_models/ensemble_stacking.joblib`, metrics in `ensemble_comparison_metrics.json`; verified in `test_practical5_ensemble.py`.
10. **Screenshot / Figure Reference:**
    - [`docs/figures/ensemble_vs_base_comparison.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/ensemble_vs_base_comparison.png)
    - [`docs/figures/ensemble_confusion_matrices.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/ensemble_confusion_matrices.png)

---

### Practical 6: Unsupervised Clustering for Battery Operating Regimes

1. **Practical Objective:** Discover natural electro-chemical operating regimes and degradation states without relying on supervised labels. Determine optimal cluster count $K$ using the Elbow method, Silhouette score, and Davies-Bouldin index.
2. **Product Feature Integration:** Integrated into **Battery Analytics & Regimes** (Module 5).
3. **Algorithms Implemented:**
   - Multi-feature K-Means clustering.
   - Automated Within-Cluster Sum of Squares (WCSS / Inertia) sweep ($K = 2 \dots 8$).
   - Silhouette analysis ($s = \frac{b - a}{\max(a, b)}$).
   - Davies-Bouldin index minimization ($R_{ij} = \frac{s_i + s_j}{d(\mu_i, \mu_j)}$).
4. **Exact Python Source Files:**
   - [`backend/ml/practical6/kmeans_clustering.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical6/kmeans_clustering.py)
   - [`backend/ml/practical6/train_clustering.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical6/train_clustering.py)
5. **Main Functions & Methods:**
   - `BatteryKMeansClusterer.fit()`
   - `BatteryKMeansClusterer.predict_cluster(features)`
   - `BatteryKMeansClusterer.compute_elbow_curve(X, k_range)`
6. **Input Data:**
   - Multi-dimensional standardized feature vectors: SOH, discharge capacity, peak temperature, internal impedance, and cycle number.
7. **Output:**
   - Cluster ID (0, 1, 2), operating regime profile name, cluster centroids, and cluster percentage distribution.
8. **Evaluation Method:**
   - Identified optimal $K=3$ at WCSS elbow inflection point (WCSS $= 985.64$, Silhouette $= 0.3608$, Davies-Bouldin $= 1.0584$):
     - *Cluster 1 (Fresh Baseline, 34.0%)*: Mean SOH 90.74%, Impedance 0.1202 $\Omega$.
     - *Cluster 0 (Active Intermediate Aging, 31.1%)*: Mean SOH 77.12%, Impedance 0.1442 $\Omega$.
     - *Cluster 2 (Degraded / High-Impedance EOL, 34.9%)*: Mean SOH 69.49%, Impedance 0.1565 $\Omega$.
9. **Execution Evidence:**
   - Serialized in `backend/saved_models/kmeans_model.joblib`, metrics in `clustering_metrics.json`; verified in `test_practical6_clustering.py`.
10. **Screenshot / Figure Reference:**
    - [`docs/figures/kmeans_elbow_and_silhouette.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/kmeans_elbow_and_silhouette.png)
    - [`docs/figures/kmeans_cluster_scatter.png`](file:///c:/Users/Dell/Desktop/VoltGuard/docs/figures/kmeans_cluster_scatter.png)

---

### Practical 7: Integrated Predictive Maintenance Platform

1. **Practical Objective:** Combine all algorithms from Practicals 1 through 6 into an enterprise full-stack software application with persistence, asynchronous REST services, automated alerting, work order management, and a modern industrial dashboard.
2. **Product Feature Integration:** Spans the entire **VoltGuard AI** platform:
   - Module 1: Fleet Overview Dashboard
   - Module 2: Battery Asset Management
   - Module 3: Battery Health Monitoring
   - Module 4: Predictive Intelligence
   - Module 5: Battery Analytics & Regimes
   - Module 6: Predictive Maintenance Center
   - Module 7: Alerts & Notifications Center
   - Module 8: Reports & Exports
3. **Algorithms Implemented:**
   - Unified multi-model inference pipeline executing regression, classification, ensemble meta-learning, clustering, expert system evaluation, and A* path dispatching in a single transactional step.
   - SQLite persistent storage with SQLAlchemy ORM.
   - Automatic alert deduplication and asset state synchronization.
4. **Exact Python Source Files:**
   - [`backend/app/engine/engine.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/app/engine/engine.py)
   - [`backend/app/engine/model_loader.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/app/engine/model_loader.py)
   - [`backend/app/main.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/app/main.py)
   - [`frontend/src/App.jsx`](file:///c:/Users/Dell/Desktop/VoltGuard/frontend/src/App.jsx)
5. **Main Functions & Methods:**
   - `IntegratedPredictiveEngine.process_battery_sample(measurement, db)`
   - `ModelRegistry.load_all()`
   - `seed_database_if_empty()`
6. **Input Data:**
   - Multi-dimensional cycle telemetry measurement (`BatteryMeasurementInput`).
7. **Output:**
   - `IntegratedPredictionResponse`: Combined SOH, RUL, Condition, Ensemble, Regime Cluster, Triggered Rules, A* Servicing Path, and Database Record ID.
8. **Evaluation Method:**
   - 43/43 automated unit and integration tests passing; frontend Vite production build passing with code 0.
9. **Execution Evidence:**
   - Persistent database at `backend/voltguard.db`; Swagger API at `/docs`.
10. **Screenshot / Figure Reference:**
    - Live React dashboard at `http://localhost:5173`.

---
*Mapping verified against the Third Year CSE (AIML) laboratory syllabus.*
