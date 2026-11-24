"""
VoltGuard AI - Practical 5 API Router
Provides ensemble predictions (Stacking, AdaBoost, Hard Voting) and comparative benchmarks.
"""

import numpy as np
from fastapi import APIRouter
from backend.app.schemas.battery import BatteryMeasurementInput, EnsembleResponse
from backend.app.engine.model_loader import registry
from backend.ml.preprocessing.data_loader import LABEL_TO_CATEGORY, HEALTH_CATEGORIES

router = APIRouter(prefix="/api/practical5", tags=["Practical 5 - Ensemble Learning"])


@router.post("/predict", response_model=EnsembleResponse)
def predict_ensemble(input_data: BatteryMeasurementInput):
    """
    Generates combined predictions from Stacking, AdaBoost, and Hard Voting ensembles.
    """
    registry.load_all()
    raw = np.array([[
        input_data.cycle_number, input_data.voltage_mean, input_data.voltage_max,
        input_data.voltage_min, input_data.voltage_std, input_data.current_mean,
        input_data.current_std, input_data.temperature_mean, input_data.temperature_max,
        input_data.temperature_min, input_data.charge_duration, input_data.discharge_duration,
        input_data.internal_impedance
    ]])
    scaled = registry.get_model("regression_scaler").transform(raw)

    stack = registry.get_model("ensemble_stacking")
    ada = registry.get_model("ensemble_adaboost")
    vote = registry.get_model("ensemble_voting")

    stack_label = int(stack.predict(scaled)[0])
    ada_label = int(ada.predict(scaled)[0])
    vote_label = int(vote.predict(scaled)[0])

    stack_probs = stack.predict_proba(scaled)[0]

    return EnsembleResponse(
        stacking_category=LABEL_TO_CATEGORY.get(stack_label, "Moderate"),
        adaboost_category=LABEL_TO_CATEGORY.get(ada_label, "Moderate"),
        voting_category=LABEL_TO_CATEGORY.get(vote_label, "Moderate"),
        consensus_category=LABEL_TO_CATEGORY.get(stack_label, "Moderate"),
        stacking_probabilities={cat: round(float(stack_probs[i]), 4) for i, cat in enumerate(HEALTH_CATEGORIES)}
    )


@router.get("/metrics")
def get_ensemble_metrics():
    """
    Returns side-by-side 7-model benchmark comparison between base classifiers and ensemble models.
    """
    return registry.get_metrics("ensemble")
