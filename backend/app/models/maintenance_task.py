"""
VoltGuard AI - Maintenance Task Work Order Database Model
Tracks predictive and corrective maintenance assignments, technician scheduling, and status.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, Text, Boolean
from backend.app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(String(50), unique=True, index=True, nullable=False)
    battery_id = Column(String(50), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    priority = Column(String(20), default="ROUTINE", nullable=False)  # CRITICAL, MODERATE, ROUTINE
    status = Column(String(20), default="SCHEDULED", nullable=False)  # SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED
    technician_name = Column(String(100), default="Unassigned", nullable=False)
    is_senior_required = Column(Boolean, default=False, nullable=False)
    scheduled_slot = Column(String(50), default="SLOT_0900", nullable=False)
    estimated_duration_hours = Column(Float, default=1.0, nullable=False)
    estimated_cost = Column(Float, default=130.0, nullable=False)
    search_algorithm_used = Column(String(50), default="A* Search", nullable=False)
    servicing_path = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
