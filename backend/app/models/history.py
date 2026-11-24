"""
VoltGuard AI - Prediction History Database Model
Stores full diagnostic and prognostic audit logs in SQLite.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from backend.app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    battery_id = Column(String(50), default="CUSTOM_INPUT")
    cycle_number = Column(Integer, default=1)

    # Input measurements
    voltage_mean = Column(Float, nullable=False)
    voltage_min = Column(Float, nullable=False)
    temperature_max = Column(Float, nullable=False)
    internal_impedance = Column(Float, nullable=False)
    discharge_duration = Column(Float, nullable=False)

    # Prognostic & Diagnostic predictions
    predicted_soh = Column(Float, nullable=False)
    predicted_rul = Column(Float, nullable=False)
    predicted_condition = Column(String(50), nullable=False)
    ensemble_condition = Column(String(50), nullable=False)
    cluster_id = Column(Integer, nullable=False)
    cluster_name = Column(String(100), nullable=False)
    expert_status = Column(String(50), nullable=False)

    # Serialized JSON audit trails
    triggered_rules_json = Column(Text, nullable=True)
    maintenance_path = Column(Text, nullable=True)
