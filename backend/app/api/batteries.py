"""
VoltGuard AI - Battery Asset Management API Router
Provides comprehensive CRUD, search, filtering, and history endpoints for battery assets.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from backend.app.database import get_db
from backend.app.models.battery_asset import BatteryAsset
from backend.app.models.history import PredictionHistory
from backend.app.schemas.asset_schemas import (
    BatteryAssetCreate,
    BatteryAssetUpdate,
    BatteryAssetResponse,
    FleetOverviewKPIs
)

router = APIRouter(prefix="/api/batteries", tags=["Battery Asset Management"])


@router.get("", response_model=List[BatteryAssetResponse])
def list_batteries(
    search: Optional[str] = Query(None, description="Search by battery ID, name, or location"),
    status: Optional[str] = Query(None, description="Filter by status: ACTIVE, MAINTENANCE, DECOMMISSIONED"),
    chemistry: Optional[str] = Query(None, description="Filter by chemistry"),
    db: Session = Depends(get_db)
):
    """
    Returns all registered battery assets with optional search and filter criteria.
    """
    query = db.query(BatteryAsset)
    if search:
        search_fmt = f"%{search.strip()}%"
        query = query.filter(
            (BatteryAsset.battery_id.ilike(search_fmt)) |
            (BatteryAsset.name.ilike(search_fmt)) |
            (BatteryAsset.location.ilike(search_fmt))
        )
    if status:
        query = query.filter(BatteryAsset.status == status.upper())
    if chemistry:
        query = query.filter(BatteryAsset.chemistry.ilike(f"%{chemistry}%"))

    assets = query.order_by(BatteryAsset.id.asc()).all()
    return [
        BatteryAssetResponse(
            id=a.id,
            battery_id=a.battery_id,
            name=a.name,
            chemistry=a.chemistry,
            nominal_capacity=a.nominal_capacity,
            nominal_voltage=a.nominal_voltage,
            installation_date=a.installation_date,
            status=a.status,
            cycle_count=a.cycle_count,
            current_soh=a.current_soh,
            current_rul=a.current_rul,
            health_condition=a.health_condition,
            operating_regime=a.operating_regime,
            location=a.location,
            notes=a.notes,
            created_at=a.created_at.isoformat() if a.created_at else "",
            updated_at=a.updated_at.isoformat() if a.updated_at else ""
        )
        for a in assets
    ]


@router.get("/overview", response_model=FleetOverviewKPIs)
def get_fleet_overview(db: Session = Depends(get_db)):
    """
    Computes aggregate KPIs for the fleet overview dashboard.
    """
    assets = db.query(BatteryAsset).all()
    total = len(assets)
    if total == 0:
        return FleetOverviewKPIs(
            total_batteries=0,
            active_batteries=0,
            maintenance_batteries=0,
            decommissioned_batteries=0,
            average_soh=100.0,
            average_rul=150.0,
            critical_alerts_count=0,
            active_maintenance_tasks=0,
            health_distribution={"Healthy": 0, "Moderate": 0, "Degraded": 0, "Critical": 0},
            operating_regimes_distribution={}
        )

    active = sum(1 for a in assets if a.status == "ACTIVE")
    maint = sum(1 for a in assets if a.status == "MAINTENANCE")
    decom = sum(1 for a in assets if a.status == "DECOMMISSIONED")
    avg_soh = round(sum(a.current_soh for a in assets) / total, 2)
    avg_rul = round(sum(a.current_rul for a in assets) / total, 1)

    health_dist = {"Healthy": 0, "Moderate": 0, "Degraded": 0, "Critical": 0}
    regimes_dist = {}

    for a in assets:
        cond = a.health_condition or "Healthy"
        health_dist[cond] = health_dist.get(cond, 0) + 1
        reg = a.operating_regime or "Fresh Baseline"
        regimes_dist[reg] = regimes_dist.get(reg, 0) + 1

    return FleetOverviewKPIs(
        total_batteries=total,
        active_batteries=active,
        maintenance_batteries=maint,
        decommissioned_batteries=decom,
        average_soh=avg_soh,
        average_rul=avg_rul,
        critical_alerts_count=health_dist.get("Critical", 0),
        active_maintenance_tasks=maint,
        health_distribution=health_dist,
        operating_regimes_distribution=regimes_dist
    )


@router.post("", response_model=BatteryAssetResponse, status_code=201)
def register_battery(asset_in: BatteryAssetCreate, db: Session = Depends(get_db)):
    """
    Registers a new battery asset into the system.
    """
    existing = db.query(BatteryAsset).filter(BatteryAsset.battery_id == asset_in.battery_id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Battery asset '{asset_in.battery_id}' already exists.")

    new_asset = BatteryAsset(
        battery_id=asset_in.battery_id.strip().upper(),
        name=asset_in.name.strip(),
        chemistry=asset_in.chemistry,
        nominal_capacity=asset_in.nominal_capacity,
        nominal_voltage=asset_in.nominal_voltage,
        installation_date=asset_in.installation_date,
        status=asset_in.status.upper(),
        cycle_count=0,
        current_soh=100.0,
        current_rul=150.0,
        health_condition="Healthy",
        operating_regime="Fresh Baseline",
        location=asset_in.location,
        notes=asset_in.notes
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return BatteryAssetResponse(
        id=new_asset.id,
        battery_id=new_asset.battery_id,
        name=new_asset.name,
        chemistry=new_asset.chemistry,
        nominal_capacity=new_asset.nominal_capacity,
        nominal_voltage=new_asset.nominal_voltage,
        installation_date=new_asset.installation_date,
        status=new_asset.status,
        cycle_count=new_asset.cycle_count,
        current_soh=new_asset.current_soh,
        current_rul=new_asset.current_rul,
        health_condition=new_asset.health_condition,
        operating_regime=new_asset.operating_regime,
        location=new_asset.location,
        notes=new_asset.notes,
        created_at=new_asset.created_at.isoformat() if new_asset.created_at else "",
        updated_at=new_asset.updated_at.isoformat() if new_asset.updated_at else ""
    )


@router.get("/{battery_id}", response_model=BatteryAssetResponse)
def get_battery(battery_id: str, db: Session = Depends(get_db)):
    """
    Returns single battery asset details.
    """
    asset = db.query(BatteryAsset).filter(BatteryAsset.battery_id == battery_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail=f"Battery '{battery_id}' not found.")

    return BatteryAssetResponse(
        id=asset.id,
        battery_id=asset.battery_id,
        name=asset.name,
        chemistry=asset.chemistry,
        nominal_capacity=asset.nominal_capacity,
        nominal_voltage=asset.nominal_voltage,
        installation_date=asset.installation_date,
        status=asset.status,
        cycle_count=asset.cycle_count,
        current_soh=asset.current_soh,
        current_rul=asset.current_rul,
        health_condition=asset.health_condition,
        operating_regime=asset.operating_regime,
        location=asset.location,
        notes=asset.notes,
        created_at=asset.created_at.isoformat() if asset.created_at else "",
        updated_at=asset.updated_at.isoformat() if asset.updated_at else ""
    )


@router.put("/{battery_id}", response_model=BatteryAssetResponse)
def update_battery(battery_id: str, update_in: BatteryAssetUpdate, db: Session = Depends(get_db)):
    """
    Updates battery asset metadata.
    """
    asset = db.query(BatteryAsset).filter(BatteryAsset.battery_id == battery_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail=f"Battery '{battery_id}' not found.")

    if update_in.name is not None:
        asset.name = update_in.name.strip()
    if update_in.chemistry is not None:
        asset.chemistry = update_in.chemistry
    if update_in.nominal_capacity is not None:
        asset.nominal_capacity = update_in.nominal_capacity
    if update_in.nominal_voltage is not None:
        asset.nominal_voltage = update_in.nominal_voltage
    if update_in.status is not None:
        asset.status = update_in.status.upper()
    if update_in.location is not None:
        asset.location = update_in.location
    if update_in.notes is not None:
        asset.notes = update_in.notes

    asset.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(asset)

    return BatteryAssetResponse(
        id=asset.id,
        battery_id=asset.battery_id,
        name=asset.name,
        chemistry=asset.chemistry,
        nominal_capacity=asset.nominal_capacity,
        nominal_voltage=asset.nominal_voltage,
        installation_date=asset.installation_date,
        status=asset.status,
        cycle_count=asset.cycle_count,
        current_soh=asset.current_soh,
        current_rul=asset.current_rul,
        health_condition=asset.health_condition,
        operating_regime=asset.operating_regime,
        location=asset.location,
        notes=asset.notes,
        created_at=asset.created_at.isoformat() if asset.created_at else "",
        updated_at=asset.updated_at.isoformat() if asset.updated_at else ""
    )


@router.delete("/{battery_id}", status_code=204)
def delete_battery(battery_id: str, db: Session = Depends(get_db)):
    """
    Deletes a battery asset from registry.
    """
    asset = db.query(BatteryAsset).filter(BatteryAsset.battery_id == battery_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail=f"Battery '{battery_id}' not found.")

    db.delete(asset)
    db.commit()
    return None


@router.get("/{battery_id}/history")
def get_battery_history(
    battery_id: str,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Returns historical diagnostic predictions and measurements for a specific battery asset.
    """
    records = db.query(PredictionHistory)\
        .filter(PredictionHistory.battery_id == battery_id)\
        .order_by(PredictionHistory.id.desc())\
        .limit(limit)\
        .all()

    return {
        "battery_id": battery_id,
        "total_records": len(records),
        "history": [
            {
                "id": r.id,
                "timestamp": r.timestamp.isoformat() if r.timestamp else "",
                "cycle_number": r.cycle_number,
                "predicted_soh": r.predicted_soh,
                "predicted_rul": r.predicted_rul,
                "predicted_condition": r.predicted_condition,
                "ensemble_condition": r.ensemble_condition,
                "cluster_name": r.cluster_name,
                "expert_status": r.expert_status,
                "voltage_mean": r.voltage_mean,
                "temperature_max": r.temperature_max,
                "internal_impedance": r.internal_impedance
            }
            for r in records
        ]
    }
