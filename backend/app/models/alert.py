"""
VoltGuard AI - Alert & Notification Database Model
Tracks operational anomalies, threshold violations, and predictive warnings.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from backend.app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class AlertRecord(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    battery_id = Column(String(50), index=True, nullable=False)
    alert_type = Column(String(50), nullable=False)  # THERMAL_RISK, CRITICAL_SOH, SEVERE_IMPEDANCE, ACCELERATED_FADE, UNDER_VOLTAGE
    severity = Column(String(20), nullable=False)    # CRITICAL, WARNING, INFO
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    action_code = Column(String(100), nullable=False)
    recommendation = Column(Text, nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)  # ACTIVE, ACKNOWLEDGED, RESOLVED

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
