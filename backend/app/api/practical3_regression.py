"""
VoltGuard AI - Practical 3 API Router
Provides SOH and RUL regression predictions and evaluation metrics.
"""

import numpy as np
from fastapi import APIRouter
from backend.app.schemas.battery import BatteryMeasurementInput, SOHPredictionResponse, RULPredictionResponse
from backend.app.engine.model_loader import registry

router = APIRouter(prefix="/api/practical3", tags=["Practical 3 - Regression Models"])


@router.post("/predict-soh", response_model=SOHPredictionResponse)
def predict_soh(input_data: BatteryMeasurementInput):
    """
    Predicts battery State of Health (SOH %) using:
    1. Scikit-learn Linear Regression
    2. Manual Gradient Descent (from scratch)
    3. Random Forest Regressor
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

    soh_lr = float(registry.get_model("soh_linear_regression").predict(scaled)[0])
    soh_gd = float(registry.get_model("soh_manual_gd").predict(scaled)[0])
    soh_rf = float(registry.get_model("soh_random_forest").predict(scaled)[0])

    rec_soh = max(40.0, min(110.0, soh_lr))
    return SOHPredictionResponse(
        soh_sklearn_lr=round(soh_lr, 2),
        soh_manual_gd=round(soh_gd, 2),
        soh_random_forest=round(soh_rf, 2),
        recommended_soh=round(rec_soh, 2)
    )


@router.post("/predict-rul", response_model=RULPredictionResponse)
def predict_rul(input_data: BatteryMeasurementInput):
    """
    Predicts Remaining Useful Life (RUL in cycles) using:
    1. Manual Gradient Descent
    2. Scikit-learn Linear Regression
    3. Random Forest Regressor
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

    rul_gd = max(0.0, float(registry.get_model("rul_manual_gd").predict(scaled)[0]))
    rul_lr = max(0.0, float(registry.get_model("rul_linear_regression").predict(scaled)[0]))
    rul_rf = max(0.0, float(registry.get_model("rul_random_forest").predict(scaled)[0]))

    return RULPredictionResponse(
        rul_manual_gd=round(rul_gd, 1),
        rul_sklearn_lr=round(rul_lr, 1),
        rul_random_forest=round(rul_rf, 1),
        recommended_rul=round(rul_gd, 1)
    )


@router.get("/metrics")
def get_regression_metrics():
    """
    Returns actual evaluation metrics (MAE, MSE, RMSE, R²) for all regression models on test cell B0018.
    """
    return registry.get_metrics("regression")
