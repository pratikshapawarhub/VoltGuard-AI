# VoltGuard AI: Academic Practical Mapping

This document provides a 1-to-1 mapping between the Third Year CSE (AIML) Laboratory syllabus practicals, the corresponding Python implementation modules, algorithms utilized, application features, and testing artifacts.

---

## Practical Mapping Summary Table

| Practical | Title | Core Algorithms | Python Implementation Files | Application UI Page | Output & Evidence |
|---|---|---|---|---|---|
| **Practical 1** | Intelligent Battery Monitoring Agent (PEAS & Expert System) | • PEAS Framework<br>• Forward-Chaining Rule-Based Expert System | `backend/ml/practical1/peas.py`<br>`backend/ml/practical1/expert_system.py`<br>`backend/app/api/practical1_expert.py` | **PEAS & Expert System** (`/expert-system`) | • Structured PEAS matrix<br>• Triggered rules audit trail<br>• Severity-graded recommendations |
| **Practical 2** | Intelligent Battery Maintenance Planner (Search Algorithms & CSP) | • BFS (Breadth-First Search)<br>• DFS (Depth-First Search)<br>• A* Search (Heuristic Cost)<br>• Hill Climbing (Local Optimization)<br>• Backtracking CSP Solver | `backend/ml/practical2/uninformed_search.py`<br>`backend/ml/practical2/informed_search.py`<br>`backend/ml/practical2/local_search.py`<br>`backend/ml/practical2/csp_solver.py`<br>`backend/app/api/practical2_search.py` | **Search Algorithm Laboratory** (`/search-lab`) | • State path transitions<br>• Nodes explored & runtimes<br>• Total path costs<br>• Conflict-free technician schedule |
| **Practical 3** | Battery Health & Remaining Useful Life Prediction (Regression) | • Scikit-learn Linear Regression<br>• Manual Gradient Descent Regressor<br>• Random Forest Regressor | `backend/ml/practical3/manual_gradient_descent.py`<br>`backend/ml/practical3/linear_regression.py`<br>`backend/ml/practical3/random_forest_regression.py`<br>`backend/ml/practical3/train_regression.py`<br>`backend/app/api/practical3_regression.py` | **Regression Analysis** (`/regression`) | • MAE, MSE, RMSE, R² metrics<br>• Actual vs Predicted SOH & RUL<br>• Manual GD cost convergence curve |
| **Practical 4** | Battery Condition Classification | • Support Vector Machine (SVM/SVC)<br>• Decision Tree Classifier<br>• K-Nearest Neighbors (KNN)<br>• Gaussian Naive Bayes | `backend/ml/practical4/classifiers.py`<br>`backend/ml/practical4/train_classification.py`<br>`backend/app/api/practical4_classification.py` | **Classification Analysis** (`/classification`) | • 4-class condition prediction (Healthy, Moderate, Degraded, Critical)<br>• Confusion matrices<br>• Precision, Recall, F1, Log Loss |
| **Practical 5** | Combined Battery Condition Prediction (Ensemble Learning) | • Stacking Classifier (Base: SVM, DT, KNN; Meta: Logistic Regression)<br>• AdaBoost Classifier<br>• Hard Voting Classifier | `backend/ml/practical5/ensemble_models.py`<br>`backend/ml/practical5/train_ensemble.py`<br>`backend/app/api/practical5_ensemble.py` | **Ensemble Analysis** (`/ensemble`) | • Base vs Ensemble comparison table<br>• Out-of-fold stacking performance<br>• Ensemble performance gain analysis |
| **Practical 6** | Intelligent Battery Usage Segmentation (Clustering) | • K-Means Clustering<br>• Elbow Method (WCSS / Inertia)<br>• Silhouette Analysis<br>• Davies-Bouldin Index | `backend/ml/practical6/kmeans_clustering.py`<br>`backend/ml/practical6/train_clustering.py`<br>`backend/app/api/practical6_clustering.py` | **Battery Clustering** (`/clustering`) | • Inertia vs K Elbow plot<br>• 2D/3D feature cluster scatter<br>• Cluster profiles (High Stress, Normal, Degraded) |
| **Practical 7** | Integrated Predictive Maintenance Platform | • End-to-End Pipeline integrating P1 through P6<br>• Multi-model inference engine<br>• Real-time rule evaluation & maintenance path search | `backend/app/engine/engine.py`<br>`backend/app/main.py`<br>`backend/app/api/practical7_integrated.py`<br>`frontend/src/` | **Overview Dashboard**, **Battery Monitoring**, **Health Prediction**, **Maintenance Center** | • Live SOH & RUL prediction<br>• Condition classification + Ensemble voting<br>• Segment cluster assignment<br>• Expert recommendations + Search plan |

---

## Verification & Academic Defense Notes

1. **No Mock Data**: Every algorithm is implemented in pure, mathematically grounded Python code.
2. **Modular Architecture**: Each practical can be independently executed and tested using `pytest` or directly through Python CLI scripts.
3. **NASA Battery Benchmark**: Uses the verified NASA Li-ion Battery Aging Dataset (B0005, B0006, B0007, B0018) with battery-wise train-test splits preventing data leakage.
