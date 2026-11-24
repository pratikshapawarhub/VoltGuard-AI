"""
VoltGuard AI - Alerts & Notifications API Router
Provides endpoints to list, filter, acknowledge, and resolve operational battery alerts.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from backend.app.database import get_db
from backend.app.models.alert import AlertRecord
from backend.app.schemas.asset_schemas import (
    AlertRecordResponse,
    AlertStatusUpdate
)

router = APIRouter(prefix="/api/alerts", tags=["Alerts & Notifications"])


@router.get("", response_model=List[AlertRecordResponse])
def list_alerts(
    status: Optional[str] = Query(None, description="Filter by status: ACTIVE, ACKNOWLEDGED, RESOLVED"),
    severity: Optional[str] = Query(None, description="Filter by severity: CRITICAL, WARNING, INFO"),
    battery_id: Optional[str] = Query(None, description="Filter by battery ID"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Returns operational alerts with optional status, severity, and battery filters.
    """
    query = db.query(AlertRecord)
    if status:
        query = query.filter(AlertRecord.status == status.upper())
    if severity:
        query = query.filter(AlertRecord.severity == severity.upper())
    if battery_id:
        query = query.filter(AlertRecord.battery_id == battery_id)

    alerts = query.order_by(AlertRecord.created_at.desc()).limit(limit).all()
    return [
        AlertRecordResponse(
            id=a.id,
            battery_id=a.battery_id,
            alert_type=a.alert_type,
            severity=a.severity,
            title=a.title,
            description=a.description,
            action_code=a.action_code,
            recommendation=a.recommendation,
            status=a.status,
            created_at=a.created_at.isoformat() if a.created_at else "",
            resolved_at=a.resolved_at.isoformat() if a.resolved_at else None
        )
        for a in alerts
    ]


@router.get("/stats")
def get_alert_stats(db: Session = Depends(get_db)):
    """
    Returns aggregate counts of active, critical, and warning alerts.
    """
    total = db.query(AlertRecord).count()
    active = db.query(AlertRecord).filter(AlertRecord.status == "ACTIVE").count()
    critical = db.query(AlertRecord).filter(AlertRecord.status == "ACTIVE", AlertRecord.severity == "CRITICAL").count()
    warning = db.query(AlertRecord).filter(AlertRecord.status == "ACTIVE", AlertRecord.severity == "WARNING").count()
    resolved = db.query(AlertRecord).filter(AlertRecord.status == "RESOLVED").count()

    return {
        "total_alerts": total,
        "active_alerts": active,
        "critical_alerts": critical,
        "warning_alerts": warning,
        "resolved_alerts": resolved
    }


@router.put("/{alert_id}/status", response_model=AlertRecordResponse)
def update_alert_status(alert_id: int, status_update: AlertStatusUpdate, db: Session = Depends(get_db)):
    """
    Updates the status of an alert (ACKNOWLEDGED or RESOLVED).
    """
    alert = db.query(AlertRecord).filter(AlertRecord.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found.")

    target_status = status_update.status.upper()
    if target_status not in ["ACTIVE", "ACKNOWLEDGED", "RESOLVED"]:
        raise HTTPException(status_code=400, detail="Status must be ACTIVE, ACKNOWLEDGED, or RESOLVED.")

    alert.status = target_status
    if target_status == "RESOLVED":
        alert.resolved_at = datetime.now(timezone.utc)
    else:
        alert.resolved_at = None

    db.commit()
    db.refresh(alert)

    return AlertRecordResponse(
        id=alert.id,
        battery_id=alert.battery_id,
        alert_type=alert.alert_type,
        severity=alert.severity,
        title=alert.title,
        description=alert.description,
        action_code=alert.action_code,
        recommendation=alert.recommendation,
        status=alert.status,
        created_at=alert.created_at.isoformat() if alert.created_at else "",
        resolved_at=alert.resolved_at.isoformat() if alert.resolved_at else None
    )
