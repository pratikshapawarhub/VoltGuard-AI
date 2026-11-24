"""
VoltGuard AI - Pydantic Request & Response Schemas
Provides data validation, typing, and OpenAPI documentation schemas.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime


class BatteryMeasurementInput(BaseModel):
    """
    Validated multi-dimensional operational battery measurement.
    """
    battery_id: str = Field(default="B_LIVE", description="Battery identifier or pack serial")
    cycle_number: int = Field(default=80, ge=1, le=1000, description="Aging cycle sequence number")
    voltage_mean: float = Field(default=3.50, ge=2.0, le=4.5, description="Mean discharge voltage (V)")
    voltage_max: float = Field(default=4.19, ge=3.0, le=4.5, description="Peak initial voltage (V)")
    voltage_min: float = Field(default=2.40, ge=1.8, le=3.5, description="End-of-discharge cut-off voltage (V)")
    voltage_std: float = Field(default=0.25, ge=0.0, le=1.0, description="Standard deviation of discharge voltage")
    current_mean: float = Field(default=1.85, ge=0.0, le=10.0, description="Mean load current magnitude (A)")
    current_std: float = Field(default=0.50, ge=0.0, le=5.0, description="Standard deviation of load current")
    temperature_mean: float = Field(default=32.5, ge=15.0, le=60.0, description="Average temperature (°C)")
    temperature_max: float = Field(default=39.5, ge=15.0, le=70.0, description="Peak temperature (°C)")
    temperature_min: float = Field(default=24.0, ge=15.0, le=40.0, description="Starting temperature (°C)")
    charge_duration: float = Field(default=10400.0, ge=500.0, le=50000.0, description="Preceding charge duration (s)")
    discharge_duration: float = Field(default=3100.0, ge=500.0, le=10000.0, description="Discharge duration (s)")
    internal_impedance: float = Field(default=0.140, ge=0.05, le=0.50, description="Internal impedance Re + Rct (Ohms)")
    recent_soh_drop: Optional[float] = Field(default=0.5, ge=0.0, le=20.0, description="Capacity drop over recent 5 cycles (%)")


class SOHPredictionResponse(BaseModel):
    soh_sklearn_lr: float
    soh_manual_gd: float
    soh_random_forest: float
    recommended_soh: float
    unit: str = "%"


class RULPredictionResponse(BaseModel):
    rul_manual_gd: float
    rul_sklearn_lr: float
    rul_random_forest: float
    recommended_rul: float
    unit: str = "cycles"


class ClassificationResponse(BaseModel):
    predicted_category: str
    predicted_label: int
    probabilities: Dict[str, float]
    model_used: str


class EnsembleResponse(BaseModel):
    stacking_category: str
    adaboost_category: str
    voting_category: str
    consensus_category: str
    stacking_probabilities: Dict[str, float]


class ClusteringResponse(BaseModel):
    cluster_id: int
    cluster_name: str
    description: str
    cluster_means: Dict[str, float]


class ExpertSystemResponse(BaseModel):
    overall_status: str
    condition_summary: str
    rules_evaluated_count: int
    triggered_rules_count: int
    triggered_rules: List[Dict[str, Any]]
    recommendations: List[str]
    disclaimer: str


class SearchMaintenanceResponse(BaseModel):
    algorithm: str
    path: List[str]
    total_cost: float
    steps: int
    nodes_explored: int
    execution_time_ms: float
    optimality: str


class IntegratedPredictionResponse(BaseModel):
    battery_id: str
    cycle_number: int
    timestamp: str
    soh_prediction: SOHPredictionResponse
    rul_prediction: RULPredictionResponse
    condition_classification: ClassificationResponse
    ensemble_classification: EnsembleResponse
    usage_clustering: ClusteringResponse
    expert_system: ExpertSystemResponse
    optimal_maintenance_plan: SearchMaintenanceResponse
    database_record_id: Optional[int] = None


class DatasetSummaryResponse(BaseModel):
    total_records: int
    batteries: List[str]
    features_count: int
    average_soh: float
    average_rul: float
    health_distribution: Dict[str, int]
    nominal_capacity: float
    eol_threshold_soh: float


class PredictionHistoryItem(BaseModel):
    id: int
    timestamp: str
    battery_id: str
    cycle_number: int
    predicted_soh: float
    predicted_rul: float
    predicted_condition: str
    ensemble_condition: str
    cluster_name: str
    expert_status: str
