# VoltGuard AI: System Architecture & Technical Design Document

**Document ID:** `ARCH-VG-2026-V1`  
**System Name:** VoltGuard AI – Intelligent Battery Health & Predictive Maintenance Platform  
**Target Architecture:** Multi-Tier Asynchronous Microservice & Industrial Analytics Platform  
**Date:** November 23, 2026  

---

## 1. System Overview & Architectural Paradigm

VoltGuard AI is architected as an industrial-grade, decoupled multi-tier predictive intelligence platform. It bridges laboratory electro-chemical prognostics and commercial battery operations through four core layers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PRESENTATION LAYER (React 18 SPA)                     │
│  - Industrial Dark SaaS Theme (Tailwind CSS 3)                              │
│  - 8 Customer Modules: Overview, Assets, Monitoring, Predictions, Analytics, │
│    Maintenance Center, Alerts Center, Reports & CSV Exports                 │
│  - Dedicated Academic Traceability & Syllabus Mapping View                  │
│  - Interactive Visualizations (Recharts Responsive Charts)                  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / JSON REST APIs
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                        API & ROUTING LAYER (FastAPI)                        │
│  - Asynchronous Web Framework on Python 3.14                                │
│  - Strict Pydantic v2 Boundary Validation Contracts                         │
│  - Enterprise Routers: /api/batteries, /api/alerts, /api/maintenance,       │
│    /api/reports, /api/dataset, /api/practical1..7                          │
│  - OpenAPI Swagger & ReDoc Documentation                                    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                   INTEGRATED PREDICTIVE ENGINE & MLOps                      │
│  - Singleton Model Registry (`model_loader.py` caching 14 serialized models)│
│  - Pipeline Orchestration (`engine.py` coordinating P1 through P6)          │
│  - Forward-Chaining Deductive Expert System (`expert_system.py`)            │
│  - A* Heuristic Graph Search & Backtracking CSP Solver                      │
│  - Automated Alert Deduplication & Asset State Synchronization              │
└───────────────────┬─────────────────────────────────────┬───────────────────┘
                    │                                     │
┌───────────────────▼──────────────────┐ ┌────────────────▼───────────────────┐
│     PERSISTENCE LAYER (SQLite)       │ │     MACHINE LEARNING ARTIFACTS      │
│  - SQLAlchemy 2.0 ORM                │ │  - 14 Serialized Joblib Artifacts   │
│  - Tables: battery_assets, alerts,   │ │  - StandardScaler Pipelines         │
│    maintenance_tasks, prediction_hist│ │  - 5 Evaluated Benchmark JSONs      │
│  - Automated Database Seeder         │ │  - NASA Benchmark Processed CSV     │
└──────────────────────────────────────┘ └─────────────────────────────────────┘
```

---

## 2. Layer-by-Layer Architectural Decomposition

### 2.1 Presentation Layer (Frontend Client)
- **Framework:** React 18 with Vite 6 high-performance bundler.
- **Styling:** Tailwind CSS 3 utilizing an industrial dark palette (`navy-950`, `navy-900`, `slate-100`, `cyan-400`, `emerald-400`, `amber-400`, `rose-400`).
- **State Management & Communication:** Centralized API client service (`frontend/src/services/api.js`) utilizing native asynchronous fetch with error boundary interception.
- **Data Visualization Engine:** Recharts SVG charting library providing responsive line charts (loss curves, degradation kinetics), bar charts (confusion matrices, health distributions), and scatter plots.
- **Component Architecture:**
  - `Navbar.jsx`: Global branding, system operational indicator, active critical alerts badge, and secondary access to Academic Traceability.
  - `Sidebar.jsx`: 8 primary commercial modules with active route indicators and footer access to curriculum documentation.
  - `BatteryInputForm.jsx`: Multi-parameter telemetry input form with pre-calibrated scenario presets and CSV file upload parser.
  - `KPICard.jsx`: Reusable operational telemetry metric cards with trend indicators.

### 2.2 Application & Service Layer (FastAPI Backend)
- **Framework:** FastAPI on Python 3.14.
- **Lifespan Lifecycle:** Managed via `@asynccontextmanager async def lifespan(app: FastAPI)` ensuring database tables are initialized, benchmark assets seeded, and models loaded into memory on startup.
- **API Routers:**
  1. `/api/batteries`: Full CRUD for battery assets, search, chemistry/status filtering, and asset-specific history.
  2. `/api/alerts`: Operational alerts ledger, severity filtering, stats, and acknowledgement/resolution lifecycle.
  3. `/api/maintenance`: Work order tracking, technician assignment, status progression, and cancellation.
  4. `/api/reports`: Consolidated health dossiers and streaming CSV data exports.
  5. `/api/dataset`: Benchmark NASA cycle inspection, summary statistics, and CSV upload validation.
  6. `/api/practical1` to `/api/practical7`: Backward-compatible endpoints exposing individual AIML practical algorithms.

### 2.3 Integrated Predictive Maintenance Engine
- **Class:** `IntegratedPredictiveEngine` (`backend/app/engine/engine.py`).
- **Design Pattern:** Singleton Pipeline Coordinator.
- **Inference Lifecycle:**
  1. Receives raw 13-feature operational measurement (`BatteryMeasurementInput`).
  2. Scales features using pre-fitted `regression_scaler.joblib`.
  3. Predicts continuous SOH (%) and RUL (cycles) using regression ensemble.
  4. Dispatches to base classifiers and Stacking meta-learner for 4-class condition assessment.
  5. Assigns operational regime cluster ID via K-Means cluster centroids.
  6. Evaluates 9 forward-chaining expert rules against physical telemetry facts.
  7. If maintenance is mandated, executes A* search to generate the cost-optimal servicing path.
  8. Synchronizes the battery asset's state in the database.
  9. Evaluates rule severities and logs deduplicated alerts to the active alerts ledger.
  10. Writes comprehensive diagnostic audit record to `prediction_history` table.

### 2.4 Model Registry (`model_loader.py`)
- Caches all trained scikit-learn, manual gradient descent, and ensemble model instances in memory to eliminate disk I/O latency during high-frequency API inference.
- Provides thread-safe lazy loading and standardized error reporting.

### 2.5 Data Persistence Layer
- **Engine:** SQLite 3 via SQLAlchemy 2.0 ORM.
- **Database File:** `backend/voltguard.db`.
- **Entity Relationship Model:**
  - `BatteryAsset`: Primary asset entity (`battery_id` unique indexed key).
  - `AlertRecord`: Operational anomaly logs linked by `battery_id`.
  - `MaintenanceTask`: Dispatched work orders linked by `battery_id`.
  - `PredictionHistory`: Complete diagnostic audit records linked by `battery_id`.

---

## 3. Data Flow & Transaction Lifecycle

```
[Telemetry Sensor Ingestion / Manual Input / CSV]
                     │
                     ▼
       FastAPI Pydantic Input Validation
                     │
                     ▼
         StandardScaler Normalization
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
   Regression Core      Classification Core
   (SOH % & RUL cyc)    (4-Class Condition)
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         Stacking Meta-Classifier
         (Probability Calibration)
                     │
                     ▼
         K-Means Clustering
         (Operational Regime ID)
                     │
                     ▼
       Forward-Chaining Expert Rules
       (Safety Thresholds & Directives)
                     │
                     ▼
          A* Search Path Planner
         (Cost-Optimal Servicing)
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
  Update Battery Asset    Deduplicate & Persist
  Current SOH & Status    Active Alert Record
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
    Log Transaction to PredictionHistory
                     │
                     ▼
  Return IntegratedPredictionResponse (JSON)
```

---

## 4. Reliability, Security & Error Handling

1. **Input Validation:** Pydantic v2 schemas strictly validate numeric bounds (e.g. voltage within $1.8\text{--}4.5\,\text{V}$, temperature within $15\text{--}70^\circ\text{C}$).
2. **Alert Deduplication:** Active alerts for the same battery and rule are updated rather than duplicated, preventing notification spam.
3. **Data Leakage Isolation:** Preprocessing and training scripts strictly enforce battery-grouped splits, ensuring test cells remain isolated.
4. **Timezone Standardization:** All timestamps use timezone-aware UTC objects (`datetime.now(timezone.utc)`).

---
*System Architecture certified for production deployment and academic audit.*
