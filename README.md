# VoltGuard AI: Intelligent Battery Health & Predictive Maintenance Platform

[![Python 3.14](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB.svg)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC.svg)](https://tailwindcss.com/)
[![Automated Tests](https://img.shields.io/badge/Pytest-43%20Passed%20(100%25)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **"Intelligent Battery Health. Predictive Maintenance. Smarter Decisions."**  
> An enterprise-grade B2B SaaS platform for Lithium-ion battery asset management, continuous prognostics, and automated maintenance dispatch.  
> Built as an integrated **Third Year B.E. / B.Tech Computer Science Engineering (AIML) Mini-Project**, seamlessly integrating **Practicals 1 through 7**.

---

## ⚡ What is VoltGuard AI?

**VoltGuard AI** bridges electrochemical physics and commercial battery operations. While conventional Battery Management Systems (BMS) rely on static voltage cutoffs, VoltGuard AI combines **knowledge-based reasoning**, **heuristic graph search**, **constraint satisfaction**, **supervised continuous regression**, **multi-class classification**, **ensemble meta-learning**, and **unsupervised clustering** into a unified, commercial-grade web platform.

The platform is trained and evaluated on the **NASA Ames Prognostics Center of Excellence (PCoE) Li-ion Battery Aging Dataset** (Cells `B0005`, `B0006`, `B0007`, `B0018`), enforcing strict **battery-grouped train/test splits** (504 training cycles vs 132 held-out test cycles) to ensure zero data leakage across physical cells.

---

## 🏢 Commercial Product Modules

VoltGuard AI is designed with clean, professional SaaS navigation without intrusive academic labels in customer workflows:

- **Module 1: Fleet Overview Dashboard**  
  Real-time rollups of registered battery assets, active online units, mean fleet SOH (%), average RUL (cycles), critical degradation alerts, SOH degradation curves, and scheduled maintenance tasks.
- **Module 2: Battery Asset Management**  
  Enterprise asset registry supporting full CRUD operations, chemistry specifications, rated capacities, locations, and interactive inspection drawers with historical cycle records.
- **Module 3: Battery Health Monitoring**  
  Interactive multi-parameter telemetry feeds (voltage, current, temperature, impedance), manual measurement ingestion form with calibrated scenario presets, and CSV data stream upload parser.
- **Module 4: Predictive Intelligence Engine**  
  Multi-model continuous regression (SOH % and RUL cycles), discrete 4-class degradation assessment (Healthy, Moderate, Degraded, Critical), and ensemble consensus.
- **Module 5: Battery Analytics & Regimes**  
  Unsupervised operational regime discovery via K-Means ($K=3$), automated WCSS elbow sweeps, Silhouette validation, and multi-dimensional cluster profiles.
- **Module 6: Predictive Maintenance Center**  
  A* informed search for cost-optimal repair sequence dispatch ($130.0), Backtracking CSP technician scheduling (0 backtracks), and fleet failure risk minimization via Hill Climbing (-31.1% risk).
- **Module 7: Alerts & Notifications Center**  
  Real-time operational anomaly detection, thermal runaway warnings, deduplicated alerts, and interactive acknowledgement/resolution lifecycles.
- **Module 8: Reports & Intelligence Dossier**  
  Consolidated system health audits and streaming CSV data exports (`assets`, `history`, `maintenance`, `alerts`).
- **Academic Implementation & Curriculum Traceability**  
  A dedicated secondary view accessible via the navbar and sidebar footer, providing examiners and professors with 1-to-1 traceability from syllabus practicals to source code and execution evidence.

---

## 📚 Curriculum Practical Traceability Matrix

Every required laboratory syllabus practical is genuinely implemented and verified:

| Practical | Academic Title | Integrated Product Feature | Implemented Algorithms | Source Code |
|:---:|:---|:---|:---|:---|
| **Practical 1** | PEAS & Rule-Based Expert System | Intelligent Battery Monitoring Agent | Russell & Norvig PEAS Framework, 9 forward-chaining rules with priority safety overrides | [`backend/ml/practical1/expert_system.py`](backend/ml/practical1/expert_system.py) |
| **Practical 2** | Problem Solving through Search & CSP | Predictive Maintenance Planner | BFS, DFS, A* with admissible heuristic, Hill Climbing local search, Backtracking CSP with MRV | [`backend/ml/practical2/informed_search.py`](backend/ml/practical2/informed_search.py) |
| **Practical 3** | Regression Models for SOH & RUL | Continuous Prognostics Engine | First-principles Manual Batch GD ($w, b, \nabla J$, MSE), Sklearn Linear Regression, Random Forest | [`backend/ml/practical3/manual_gradient_descent.py`](backend/ml/practical3/manual_gradient_descent.py) |
| **Practical 4** | Battery Degradation Classification | Battery Condition Assessment | Support Vector Classifier (RBF kernel), Decision Tree (Gini), K-Nearest Neighbors, Naive Bayes | [`backend/ml/practical4/classifiers.py`](backend/ml/practical4/classifiers.py) |
| **Practical 5** | Ensemble Learning | Combined Prediction Engine | Stacking Meta-Classifier (5-fold out-of-fold CV + Logistic Regression), AdaBoost, Hard Voting | [`backend/ml/practical5/ensemble_models.py`](backend/ml/practical5/ensemble_models.py) |
| **Practical 6** | Unsupervised Clustering | Battery Usage Segmentation | Multi-feature K-Means, Automated WCSS Elbow method sweep ($K=2..8$), Silhouette & Davies-Bouldin | [`backend/ml/practical6/kmeans_clustering.py`](backend/ml/practical6/kmeans_clustering.py) |
| **Practical 7** | Integrated Predictive Platform | Complete VoltGuard AI Platform | Unified multi-model inference pipeline, Singleton Model Registry, SQLite persistence, React UI | [`backend/app/engine/engine.py`](backend/app/engine/engine.py) |

---

## 🔬 Empirical Benchmarks (Evaluated on Unseen NASA Test Cell B0018)

- **SOH Regression:** Sklearn Linear Regression achieved **$R^2 = 0.9968$, $\text{MAE} = 0.34\%$**; Manual Batch Gradient Descent achieved **$R^2 = 0.9429$, $\text{MAE} = 1.76\%$**.
- **RUL Prognosis:** Manual Gradient Descent achieved top cross-cell generalization with **$R^2 = 0.5872$, $\text{MAE} = 18.37$ cycles** (beating the syllabus target of $<20$ cycles).
- **Condition Classification:** Decision Tree achieved **71.97% Accuracy** ($\text{Macro F1} = 0.6090$); SVM achieved optimal probability calibration ($\text{Log Loss} = 1.226$).
- **Ensemble Meta-Learning:** Stacking Meta-Classifier achieved **71.97% Accuracy** with the lowest Log Loss (**1.1602**) across all 7 evaluated models.
- **Search Optimization:** A* discovered the lowest-cost repair sequence at **$130.0** (vs BFS $170.0 and DFS $205.0). Hill Climbing reduced fleet failure risk by **31.1%**. CSP achieved **0 backtracks**.
- **Unsupervised Clustering:** Optimal $K=3$ identified at WCSS elbow inflection point ($\text{Silhouette} = 0.3608$, $\text{Davies-Bouldin} = 1.0584$).

---

## 📁 Repository Structure

```text
VoltGuard/
├── backend/
│   ├── app/
│   │   ├── api/                     # Enterprise SaaS & Practical API Routers
│   │   │   ├── batteries.py         # Battery Asset CRUD & history
│   │   │   ├── alerts.py            # Alerts management & resolution
│   │   │   ├── maintenance.py       # Work orders & task scheduling
│   │   │   ├── reports.py           # Consolidated dossiers & CSV exports
│   │   │   ├── dataset.py           # NASA dataset exploration
│   │   │   └── practical1_expert.py to practical7_integrated.py
│   │   ├── engine/                  # Singleton model registry & unified P7 pipeline
│   │   ├── models/                  # SQLAlchemy SQLite models (assets, alerts, tasks, history)
│   │   ├── schemas/                 # Pydantic v2 validation contracts
│   │   ├── config.py                # Environment & directory configuration
│   │   ├── database.py              # SQLite session management
│   │   ├── database_seeder.py       # Benchmark assets auto-seeder
│   │   └── main.py                  # FastAPI entrypoint with lifespan
│   ├── data/
│   │   ├── raw/                     # Raw NASA .mat archives (B0005, B0006, B0007, B0018)
│   │   └── processed/               # Cleaned master CSV (636 cycles, zero NaNs)
│   ├── ml/                          # Core ML algorithms (Practicals 1 to 6)
│   ├── saved_models/                # 14 serialized joblib models & metrics JSONs
│   ├── tests/                       # 43 automated unit & integration tests
│   └── requirements.txt
├── docs/                            # Complete Technical Documentation Suite
│   ├── PROJECT_AUDIT.md             # Baseline diagnostics & audit ledger
│   ├── ERROR_RESOLUTION_REPORT.md   # Bug resolution & root-cause report
│   ├── PRACTICAL_IMPLEMENTATION_MAPPING.md # Curriculum practicals matrix
│   ├── DEMONSTRATION_GUIDE.md       # Step-by-step viva & demo guide
│   ├── SYSTEM_ARCHITECTURE.md       # Multi-tier technical architecture
│   ├── DATASET_DOCUMENTATION.md     # NASA PCoE dataset specification
│   ├── MODEL_EVALUATION.md          # Complete empirical benchmarks
│   ├── API_DOCUMENTATION.md         # REST API reference & schemas
│   ├── TESTING_REPORT.md            # Test coverage & acceptance checklist
│   └── figures/                     # 13 diagnostic evaluation plots
├── frontend/
│   ├── src/
│   │   ├── components/              # Navbar, Sidebar, KPICard, BatteryInputForm
│   │   ├── pages/                   # 8 B2B modules + Academic Traceability
│   │   ├── services/api.js          # Centralized API service
│   │   └── App.jsx                  # Main routing container
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

---

## 🚀 Quickstart & Local Execution

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Node.js 18+ & npm
- Git

### 2. Backend Startup
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Run automated test suite (verifying all 43 tests)
python -m pytest backend/tests/ -v

# 3. Start FastAPI server
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
- Swagger UI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Interactive ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Frontend Startup
In a separate terminal:
```bash
# 1. Navigate to frontend
cd frontend

# 2. Install npm packages
npm install

# 3. Start Vite development server
npm run dev
```
- Open your browser at [http://localhost:5173](http://localhost:5173).

---

## 🧪 Testing Verification

Run the full pytest suite:
```bash
python -m pytest backend/tests/ -v
```
Output:
```text
======================== 43 passed in 69.78s (100% pass rate) ========================
```

Run frontend production build verification:
```bash
cd frontend && npm run build
```
Output:
```text
✓ 2023 modules transformed.
dist/index.html                   0.58 kB │ gzip:   0.39 kB
dist/assets/index-CTKqzP3C.css   31.13 kB │ gzip:   6.16 kB
dist/assets/index-C5Dueinu.js   751.99 kB │ gzip: 197.03 kB
✓ built in 17.36s
```

---

## 📖 Technical Documentation Index

All 10 required technical specification documents are located in [`docs/`](docs/):
1. [`docs/PROJECT_AUDIT.md`](docs/PROJECT_AUDIT.md) – Baseline system audit and issue catalogue.
2. [`docs/ERROR_RESOLUTION_REPORT.md`](docs/ERROR_RESOLUTION_REPORT.md) – Detailed debugging and resolution ledger.
3. [`docs/PRACTICAL_IMPLEMENTATION_MAPPING.md`](docs/PRACTICAL_IMPLEMENTATION_MAPPING.md) – 1-to-1 syllabus practical mapping.
4. [`docs/DEMONSTRATION_GUIDE.md`](docs/DEMONSTRATION_GUIDE.md) – Step-by-step viva & examiner demonstration guide.
5. [`docs/SYSTEM_ARCHITECTURE.md`](docs/SYSTEM_ARCHITECTURE.md) – Decoupled multi-tier technical architecture.
6. [`docs/DATASET_DOCUMENTATION.md`](docs/DATASET_DOCUMENTATION.md) – NASA battery dataset specification & split discipline.
7. [`docs/MODEL_EVALUATION.md`](docs/MODEL_EVALUATION.md) – Cross-cell empirical benchmarks and statistical analysis.
8. [`docs/API_DOCUMENTATION.md`](docs/API_DOCUMENTATION.md) – RESTful API endpoints, request schemas, and responses.
9. [`docs/TESTING_REPORT.md`](docs/TESTING_REPORT.md) – Comprehensive QA test plan and acceptance criteria verification.
10. [`README.md`](README.md) – Master platform documentation.

---

## 📜 License
Developed for academic and industrial research under the **MIT License**.
