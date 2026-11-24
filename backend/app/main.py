"""
VoltGuard AI - FastAPI Application Entrypoint
Configures CORS, registers all Enterprise SaaS and AIML Practical routers,
mounts static figures, and bootstraps the database with seed assets.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.config import CORS_ORIGINS, DOCS_FIGURES_DIR
from backend.app.database import engine, Base
from backend.app.database_seeder import seed_database_if_empty
from backend.app.engine.model_loader import registry

# Ensure tables and seed data are created immediately upon module import
Base.metadata.create_all(bind=engine)
seed_database_if_empty()

# Import all API routers
from backend.app.api.dataset import router as dataset_router
from backend.app.api.batteries import router as batteries_router
from backend.app.api.alerts import router as alerts_router
from backend.app.api.maintenance import router as maintenance_router
from backend.app.api.reports import router as reports_router
from backend.app.api.practical1_expert import router as p1_router
from backend.app.api.practical2_search import router as p2_router
from backend.app.api.practical3_regression import router as p3_router
from backend.app.api.practical4_classification import router as p4_router
from backend.app.api.practical5_ensemble import router as p5_router
from backend.app.api.practical6_clustering import router as p6_router
from backend.app.api.practical7_integrated import router as p7_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern FastAPI lifespan handler:
    1. Bootstraps SQLite database tables
    2. Seeds benchmark battery assets, active alerts, and initial maintenance tasks
    3. Pre-loads all 14 ML models into memory
    """
    Base.metadata.create_all(bind=engine)
    seed_database_if_empty()
    registry.load_all()
    yield


# Create FastAPI application
app = FastAPI(
    title="VoltGuard AI API",
    description="Intelligent Battery Health & Predictive Maintenance Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS for frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Product & Enterprise API Routers
app.include_router(batteries_router)
app.include_router(alerts_router)
app.include_router(maintenance_router)
app.include_router(reports_router)

# Register Machine Learning Core & Practical Routers (Backward-Compatible)
app.include_router(dataset_router)
app.include_router(p1_router)
app.include_router(p2_router)
app.include_router(p3_router)
app.include_router(p4_router)
app.include_router(p5_router)
app.include_router(p6_router)
app.include_router(p7_router)

# Mount docs figures directory to serve diagnostic plots
if os.path.exists(DOCS_FIGURES_DIR):
    app.mount("/figures", StaticFiles(directory=DOCS_FIGURES_DIR), name="figures")


@app.get("/")
def root():
    return {
        "platform": "VoltGuard AI",
        "tagline": "Intelligent Battery Health. Predictive Maintenance. Smarter Decisions.",
        "status": "OPERATIONAL",
        "documentation": "/docs",
        "modules": [
            "Module 1: Fleet Overview Dashboard",
            "Module 2: Battery Asset Management",
            "Module 3: Battery Health Monitoring",
            "Module 4: Predictive Intelligence (SOH, RUL, Condition)",
            "Module 5: Battery Analytics & Segmentation",
            "Module 6: Predictive Maintenance Center",
            "Module 7: Alerts & Notifications Center",
            "Module 8: Reporting & Intelligence Dossier"
        ],
        "practicals_available": [
            "Practical 1: PEAS Descriptors and Expert System",
            "Practical 2: Problem Solving through Search (BFS, DFS, A*, Hill Climbing, CSP)",
            "Practical 3: Regression Models (Manual GD, Sklearn, Random Forest)",
            "Practical 4: Classification Models (SVM, Decision Tree, KNN, Naive Bayes)",
            "Practical 5: Ensemble Learning (Stacking, AdaBoost, Hard Voting)",
            "Practical 6: Clustering Algorithms (K-Means, Elbow Method)",
            "Practical 7: Integrated Predictive Maintenance Platform"
        ],
        "academic_practicals_integrated": [
            "Practical 1: PEAS Descriptors and Expert System",
            "Practical 2: Problem Solving through Search (BFS, DFS, A*, Hill Climbing, CSP)",
            "Practical 3: Regression Models (Manual GD, Sklearn, Random Forest)",
            "Practical 4: Classification Models (SVM, Decision Tree, KNN, Naive Bayes)",
            "Practical 5: Ensemble Learning (Stacking, AdaBoost, Hard Voting)",
            "Practical 6: Clustering Algorithms (K-Means, Elbow Method)",
            "Practical 7: Integrated Predictive Maintenance Platform"
        ]
    }
