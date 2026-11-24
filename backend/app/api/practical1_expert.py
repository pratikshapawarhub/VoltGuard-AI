"""
VoltGuard AI - Practical 1 API Router
Exposes PEAS framework matrix and Rule-Based Expert System evaluation.
"""

from fastapi import APIRouter
from typing import Dict, Any

from backend.app.schemas.battery import BatteryMeasurementInput, ExpertSystemResponse
from backend.ml.practical1.peas import get_peas_description
from backend.ml.practical1.expert_system import BatteryExpertSystem

router = APIRouter(prefix="/api/practical1", tags=["Practical 1 - PEAS & Expert System"])
expert_system = BatteryExpertSystem()


@router.get("/peas")
def get_peas_matrix():
    """
    Returns the formal PEAS (Performance, Environment, Actuators, Sensors) framework descriptor matrix.
    """
    return get_peas_description()


@router.post("/evaluate", response_model=ExpertSystemResponse)
def evaluate_expert_rules(input_data: BatteryMeasurementInput):
    """
    Evaluates battery telemetry against forward-chaining IF-THEN rules and returns triggered alerts.
    """
    # Estimate SOH if not given directly
    soh_est = 80.0
    facts = {
        "soh": soh_est,
        "temperature_max": input_data.temperature_max,
        "internal_impedance": input_data.internal_impedance,
        "voltage_min": input_data.voltage_min,
        "voltage_max": input_data.voltage_max,
        "recent_soh_drop": input_data.recent_soh_drop or 0.0
    }

    result = expert_system.evaluate(facts)
    return ExpertSystemResponse(
        overall_status=result["overall_status"],
        condition_summary=result["condition_summary"],
        rules_evaluated_count=result["rules_evaluated_count"],
        triggered_rules_count=result["triggered_rules_count"],
        triggered_rules=result["triggered_rules"],
        recommendations=result["recommendations"],
        disclaimer=result["disclaimer"]
    )
