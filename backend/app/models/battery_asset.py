"""
VoltGuard AI - Battery Asset Database Model
Represents a physical or virtual battery pack/cell in the asset registry.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, Text, Boolean
from backend.app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class BatteryAsset(Base):
    __tablename__ = "battery_assets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    battery_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    chemistry = Column(String(50), default="LiCoO2 / Graphite", nullable=False)
    nominal_capacity = Column(Float, default=2.0, nullable=False)
    nominal_voltage = Column(Float, default=3.7, nullable=False)
    installation_date = Column(String(50), default="2024-01-15", nullable=False)
    status = Column(String(50), default="ACTIVE", nullable=False)  # ACTIVE, MAINTENANCE, DECOMMISSIONED
    cycle_count = Column(Integer, default=0, nullable=False)
    current_soh = Column(Float, default=100.0, nullable=False)
    current_rul = Column(Float, default=150.0, nullable=False)
    health_condition = Column(String(50), default="Healthy", nullable=False)
    operating_regime = Column(String(100), default="Fresh Baseline", nullable=False)
    location = Column(String(100), default="Chamber Bay A", nullable=False)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
