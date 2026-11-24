"""
VoltGuard AI - Maintenance Work Orders API Router
Tracks predictive maintenance assignments, technician scheduling, and status.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

from backend.app.database import get_db
from backend.app.models.maintenance_task import MaintenanceTask
from backend.app.schemas.asset_schemas import (
    MaintenanceTaskCreate,
    MaintenanceTaskUpdate,
    MaintenanceTaskResponse
)

router = APIRouter(prefix="/api/maintenance", tags=["Predictive Maintenance Operations"])


@router.get("/tasks", response_model=List[MaintenanceTaskResponse])
def list_maintenance_tasks(
    status: Optional[str] = Query(None, description="SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED"),
    priority: Optional[str] = Query(None, description="CRITICAL, MODERATE, ROUTINE"),
    battery_id: Optional[str] = Query(None, description="Filter by battery ID"),
    db: Session = Depends(get_db)
):
    """
    Returns maintenance tasks with optional status and priority filtering.
    """
    query = db.query(MaintenanceTask)
    if status:
        query = query.filter(MaintenanceTask.status == status.upper())
    if priority:
        query = query.filter(MaintenanceTask.priority == priority.upper())
    if battery_id:
        query = query.filter(MaintenanceTask.battery_id == battery_id)

    tasks = query.order_by(MaintenanceTask.created_at.desc()).all()
    return [
        MaintenanceTaskResponse(
            id=t.id,
            task_id=t.task_id,
            battery_id=t.battery_id,
            title=t.title,
            priority=t.priority,
            status=t.status,
            technician_name=t.technician_name,
            is_senior_required=t.is_senior_required,
            scheduled_slot=t.scheduled_slot,
            estimated_duration_hours=t.estimated_duration_hours,
            estimated_cost=t.estimated_cost,
            search_algorithm_used=t.search_algorithm_used,
            servicing_path=t.servicing_path,
            notes=t.notes,
            created_at=t.created_at.isoformat() if t.created_at else "",
            completed_at=t.completed_at.isoformat() if t.completed_at else None
        )
        for t in tasks
    ]


@router.post("/tasks", response_model=MaintenanceTaskResponse, status_code=201)
def create_maintenance_task(task_in: MaintenanceTaskCreate, db: Session = Depends(get_db)):
    """
    Creates a new maintenance task (e.g. dispatched from A* Search plan or CSP schedule).
    """
    tid = task_in.task_id or f"TASK-{task_in.battery_id}-{str(uuid.uuid4())[:6].upper()}"

    new_task = MaintenanceTask(
        task_id=tid,
        battery_id=task_in.battery_id,
        title=task_in.title,
        priority=task_in.priority.upper(),
        status="SCHEDULED",
        technician_name=task_in.technician_name,
        is_senior_required=task_in.is_senior_required,
        scheduled_slot=task_in.scheduled_slot,
        estimated_duration_hours=task_in.estimated_duration_hours,
        estimated_cost=task_in.estimated_cost,
        search_algorithm_used=task_in.search_algorithm_used,
        servicing_path=task_in.servicing_path,
        notes=task_in.notes
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return MaintenanceTaskResponse(
        id=new_task.id,
        task_id=new_task.task_id,
        battery_id=new_task.battery_id,
        title=new_task.title,
        priority=new_task.priority,
        status=new_task.status,
        technician_name=new_task.technician_name,
        is_senior_required=new_task.is_senior_required,
        scheduled_slot=new_task.scheduled_slot,
        estimated_duration_hours=new_task.estimated_duration_hours,
        estimated_cost=new_task.estimated_cost,
        search_algorithm_used=new_task.search_algorithm_used,
        servicing_path=new_task.servicing_path,
        notes=new_task.notes,
        created_at=new_task.created_at.isoformat() if new_task.created_at else "",
        completed_at=None
    )


@router.put("/tasks/{task_id}", response_model=MaintenanceTaskResponse)
def update_maintenance_task(task_id: str, update_in: MaintenanceTaskUpdate, db: Session = Depends(get_db)):
    """
    Updates maintenance task status (e.g. to IN_PROGRESS or COMPLETED) or assigned technician.
    """
    task = db.query(MaintenanceTask).filter(MaintenanceTask.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found.")

    if update_in.title is not None:
        task.title = update_in.title
    if update_in.priority is not None:
        task.priority = update_in.priority.upper()
    if update_in.technician_name is not None:
        task.technician_name = update_in.technician_name
    if update_in.scheduled_slot is not None:
        task.scheduled_slot = update_in.scheduled_slot
    if update_in.notes is not None:
        task.notes = update_in.notes

    if update_in.status is not None:
        target_status = update_in.status.upper()
        task.status = target_status
        if target_status == "COMPLETED":
            task.completed_at = datetime.now(timezone.utc)
        else:
            task.completed_at = None

    db.commit()
    db.refresh(task)

    return MaintenanceTaskResponse(
        id=task.id,
        task_id=task.task_id,
        battery_id=task.battery_id,
        title=task.title,
        priority=task.priority,
        status=task.status,
        technician_name=task.technician_name,
        is_senior_required=task.is_senior_required,
        scheduled_slot=task.scheduled_slot,
        estimated_duration_hours=task.estimated_duration_hours,
        estimated_cost=task.estimated_cost,
        search_algorithm_used=task.search_algorithm_used,
        servicing_path=task.servicing_path,
        notes=task.notes,
        created_at=task.created_at.isoformat() if task.created_at else "",
        completed_at=task.completed_at.isoformat() if task.completed_at else None
    )


@router.delete("/tasks/{task_id}", status_code=204)
def delete_maintenance_task(task_id: str, db: Session = Depends(get_db)):
    """
    Cancels and deletes a maintenance task.
    """
    task = db.query(MaintenanceTask).filter(MaintenanceTask.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found.")

    db.delete(task)
    db.commit()
    return None
