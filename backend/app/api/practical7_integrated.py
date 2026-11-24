"""
VoltGuard AI - Practical 7 API Router
Exposes the Integrated Predictive Maintenance Engine and SQLite prediction history.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.schemas.battery import (
    BatteryMeasurementInput,
    IntegratedPredictionResponse,
    PredictionHistoryItem
)
from backend.app.engine.engine import integrated_engine
from backend.app.models.history import PredictionHistory

router = APIRouter(prefix="/api/practical7", tags=["Practical 7 - Integrated Engine"])


@router.post("/predict-all", response_model=IntegratedPredictionResponse)
def run_integrated_pipeline(
    measurement: BatteryMeasurementInput,
    db: Session = Depends(get_db)
):
    """
    Executes the full end-to-end predictive maintenance engine:
    1. SOH & RUL Regression (Practical 3)
    2. Condition Classification (Practical 4)
    3. Stacking, AdaBoost, Voting Ensemble (Practical 5)
    4. Usage Segmentation Clustering (Practical 6)
    5. Rule-Based Expert System (Practical 1)
    6. A* Optimal Maintenance Path Planning (Practical 2)
    7. Persists transaction to SQLite database.
    """
    return integrated_engine.process_battery_sample(measurement, db=db)


@router.get("/history", response_model=List[PredictionHistoryItem])
def get_prediction_history(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Retrieves stored prediction audit logs from SQLite database.
    """
    records = db.query(PredictionHistory).order_by(PredictionHistory.timestamp.desc()).limit(limit).all()
    return [
        PredictionHistoryItem(
            id=r.id,
            timestamp=r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            battery_id=r.battery_id,
            cycle_number=r.cycle_number,
            predicted_soh=round(r.predicted_soh, 2),
            predicted_rul=round(r.predicted_rul, 1),
            predicted_condition=r.predicted_condition,
            ensemble_condition=r.ensemble_condition,
            cluster_name=r.cluster_name,
            expert_status=r.expert_status
        )
        for r in records
    ]
