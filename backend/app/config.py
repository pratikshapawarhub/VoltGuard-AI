"""
VoltGuard AI - Backend Configuration
Defines file system paths, model artifact directories, and runtime thresholds.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
CLEANED_CSV_PATH = os.path.join(PROCESSED_DATA_DIR, "nasa_battery_cleaned.csv")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
DOCS_FIGURES_DIR = os.path.join(PROJECT_ROOT, "docs", "figures")
DB_PATH = os.path.join(BASE_DIR, "voltguard.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"
]
