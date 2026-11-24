"""
VoltGuard AI - Practical 4 API Router
Provides multi-class condition classification predictions and benchmark reports.
"""

import numpy as np
from fastapi import APIRouter
from backend.app.schemas.battery import BatteryMeasurementInput, ClassificationResponse
from backend.app.engine.model_loader import registry
from backend.ml.preprocessing.data_loader import LABEL_TO_CATEGORY, HEALTH_CATEGORIES

router = APIRouter(prefix="/api/practical4", tags=["Practical 4 - Classification Models"])


@router.post("/classify", response_model=ClassificationResponse)
def classify_battery_condition(input_data: BatteryMeasurementInput):
    """
    Classifies battery into Healthy, Moderate, Degraded, or Critical using Decision Tree Classifier.
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

    dt = registry.get_model("classification_decision_tree")
    label = int(dt.predict(scaled)[0])
    probs = dt.predict_proba(scaled)[0]

    return ClassificationResponse(
        predicted_category=LABEL_TO_CATEGORY.get(label, "Moderate"),
        predicted_label=label,
        probabilities={cat: round(float(probs[i]), 4) for i, cat in enumerate(HEALTH_CATEGORIES)},
        model_used="Decision Tree Classifier"
    )


@router.get("/metrics")
def get_classification_metrics():
    """
    Returns confusion matrices and classification reports for SVM, Decision Tree, KNN, and Naive Bayes.
    """
    return registry.get_metrics("classification")
