"""
VoltGuard AI - Battery Asset, Alerts, and Maintenance Work Order Schemas
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, List, Optional
from datetime import datetime


class BatteryAssetBase(BaseModel):
    battery_id: str = Field(..., description="Unique battery identifier (e.g. B0005, PACK-102)")
    name: str = Field(..., description="Descriptive name of the battery pack")
    chemistry: str = Field(default="LiCoO2 / Graphite", description="Cell chemistry")
    nominal_capacity: float = Field(default=2.0, ge=0.1, le=1000.0, description="Rated nominal capacity in Ahr")
    nominal_voltage: float = Field(default=3.7, ge=1.0, le=1000.0, description="Nominal terminal voltage in V")
    installation_date: str = Field(default="2024-01-15", description="Installation or commissioning date")
    status: str = Field(default="ACTIVE", description="ACTIVE, MAINTENANCE, or DECOMMISSIONED")
    location: str = Field(default="Chamber Bay A", description="Physical bay, vehicle ID, or test bench")
    notes: Optional[str] = Field(None, description="Operational notes or special handling requirements")


class BatteryAssetCreate(BatteryAssetBase):
    pass


class BatteryAssetUpdate(BaseModel):
    name: Optional[str] = None
    chemistry: Optional[str] = None
    nominal_capacity: Optional[float] = None
    nominal_voltage: Optional[float] = None
    status: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class BatteryAssetResponse(BatteryAssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cycle_count: int
    current_soh: float
    current_rul: float
    health_condition: str
    operating_regime: str
    created_at: str
    updated_at: str


class AlertRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    battery_id: str
    alert_type: str
    severity: str
    title: str
    description: str
    action_code: str
    recommendation: str
    status: str
    created_at: str
    resolved_at: Optional[str] = None


class AlertStatusUpdate(BaseModel):
    status: str = Field(..., description="ACKNOWLEDGED or RESOLVED")


class MaintenanceTaskCreate(BaseModel):
    task_id: Optional[str] = None
    battery_id: str
    title: str
    priority: str = Field(default="ROUTINE", description="CRITICAL, MODERATE, ROUTINE")
    technician_name: str = Field(default="Unassigned")
    is_senior_required: bool = False
    scheduled_slot: str = "SLOT_0900"
    estimated_duration_hours: float = 1.0
    estimated_cost: float = 130.0
    search_algorithm_used: str = "A* Search"
    servicing_path: Optional[str] = None
    notes: Optional[str] = None


class MaintenanceTaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None  # SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED
    technician_name: Optional[str] = None
    scheduled_slot: Optional[str] = None
    notes: Optional[str] = None


class MaintenanceTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: str
    battery_id: str
    title: str
    priority: str
    status: str
    technician_name: str
    is_senior_required: bool
    scheduled_slot: str
    estimated_duration_hours: float
    estimated_cost: float
    search_algorithm_used: str
    servicing_path: Optional[str]
    notes: Optional[str]
    created_at: str
    completed_at: Optional[str]


class FleetOverviewKPIs(BaseModel):
    total_batteries: int
    active_batteries: int
    maintenance_batteries: int
    decommissioned_batteries: int
    average_soh: float
    average_rul: float
    critical_alerts_count: int
    active_maintenance_tasks: int
    health_distribution: Dict[str, int]
    operating_regimes_distribution: Dict[str, int]
