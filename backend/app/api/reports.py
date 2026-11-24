"""
VoltGuard AI - Reporting & Export API Router
Generates consolidated battery health reports and CSV data exports.
"""

import io
import csv
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from backend.app.database import get_db
from backend.app.models.battery_asset import BatteryAsset
from backend.app.models.history import PredictionHistory
from backend.app.models.alert import AlertRecord
from backend.app.models.maintenance_task import MaintenanceTask

router = APIRouter(prefix="/api/reports", tags=["Reporting & Intelligence Dossier"])


@router.get("/summary")
def get_report_summary(db: Session = Depends(get_db)):
    """
    Compiles a comprehensive system-wide diagnostic intelligence report.
    """
    assets = db.query(BatteryAsset).all()
    alerts = db.query(AlertRecord).filter(AlertRecord.status == "ACTIVE").all()
    tasks = db.query(MaintenanceTask).all()
    predictions = db.query(PredictionHistory).order_by(PredictionHistory.id.desc()).limit(10).all()

    return {
        "report_generated_at": datetime.now(timezone.utc).isoformat(),
        "platform": "VoltGuard AI Enterprise Platform",
        "total_assets": len(assets),
        "active_critical_alerts": sum(1 for a in alerts if a.severity == "CRITICAL"),
        "total_scheduled_maintenance_tasks": sum(1 for t in tasks if t.status == "SCHEDULED"),
        "assets_summary": [
            {
                "battery_id": a.battery_id,
                "name": a.name,
                "chemistry": a.chemistry,
                "status": a.status,
                "current_soh": a.current_soh,
                "current_rul": a.current_rul,
                "health_condition": a.health_condition,
                "operating_regime": a.operating_regime,
                "location": a.location
            }
            for a in assets
        ],
        "recent_predictions": [
            {
                "id": p.id,
                "battery_id": p.battery_id,
                "cycle": p.cycle_number,
                "soh": p.predicted_soh,
                "rul": p.predicted_rul,
                "condition": p.predicted_condition,
                "ensemble": p.ensemble_condition,
                "regime": p.cluster_name,
                "timestamp": p.timestamp.isoformat() if p.timestamp else ""
            }
            for p in predictions
        ]
    }


@router.get("/export-csv")
def export_csv(
    report_type: str = Query("assets", description="Type of export: 'assets', 'history', 'maintenance', or 'alerts'"),
    db: Session = Depends(get_db)
):
    """
    Streams a CSV file export for the requested report type.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    if report_type == "assets":
        writer.writerow([
            "Battery ID", "Name", "Chemistry", "Nominal Capacity (Ahr)", 
            "Nominal Voltage (V)", "Installation Date", "Status", "Cycle Count", 
            "Current SOH (%)", "Current RUL (cycles)", "Condition", "Operating Regime", "Location"
        ])
        assets = db.query(BatteryAsset).order_by(BatteryAsset.id.asc()).all()
        for a in assets:
            writer.writerow([
                a.battery_id, a.name, a.chemistry, a.nominal_capacity,
                a.nominal_voltage, a.installation_date, a.status, a.cycle_count,
                a.current_soh, a.current_rul, a.health_condition, a.operating_regime, a.location
            ])
        filename = f"voltguard_battery_assets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    elif report_type == "history":
        writer.writerow([
            "ID", "Timestamp", "Battery ID", "Cycle Number", 
            "Mean Voltage (V)", "Cutoff Voltage (V)", "Max Temp (C)", 
            "Internal Impedance (Ohms)", "Predicted SOH (%)", "Predicted RUL (cycles)", 
            "Condition (Classification)", "Ensemble Consensus", "Operating Regime Cluster", "Expert Status"
        ])
        records = db.query(PredictionHistory).order_by(PredictionHistory.id.desc()).all()
        for r in records:
            writer.writerow([
                r.id, r.timestamp.isoformat() if r.timestamp else "", r.battery_id, r.cycle_number,
                r.voltage_mean, r.voltage_min, r.temperature_max,
                r.internal_impedance, r.predicted_soh, r.predicted_rul,
                r.predicted_condition, r.ensemble_condition, r.cluster_name, r.expert_status
            ])
        filename = f"voltguard_prediction_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    elif report_type == "maintenance":
        writer.writerow([
            "Task ID", "Battery ID", "Title", "Priority", "Status", 
            "Technician", "Senior Required", "Scheduled Slot", "Duration (hrs)", 
            "Cost ($)", "Algorithm", "Servicing Path", "Created At"
        ])
        tasks = db.query(MaintenanceTask).order_by(MaintenanceTask.id.desc()).all()
        for t in tasks:
            writer.writerow([
                t.task_id, t.battery_id, t.title, t.priority, t.status,
                t.technician_name, t.is_senior_required, t.scheduled_slot,
                t.estimated_duration_hours, t.estimated_cost, t.search_algorithm_used,
                t.servicing_path, t.created_at.isoformat() if t.created_at else ""
            ])
        filename = f"voltguard_maintenance_tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    elif report_type == "alerts":
        writer.writerow([
            "Alert ID", "Battery ID", "Type", "Severity", "Title", 
            "Description", "Action Code", "Recommendation", "Status", "Created At"
        ])
        alerts = db.query(AlertRecord).order_by(AlertRecord.id.desc()).all()
        for a in alerts:
            writer.writerow([
                a.id, a.battery_id, a.alert_type, a.severity, a.title,
                a.description, a.action_code, a.recommendation, a.status,
                a.created_at.isoformat() if a.created_at else ""
            ])
        filename = f"voltguard_alerts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    else:
        raise HTTPException(status_code=400, detail="Invalid report_type. Choose 'assets', 'history', 'maintenance', or 'alerts'.")

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
