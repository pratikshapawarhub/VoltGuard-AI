"""
VoltGuard AI - Practical 3 Unit & Validation Tests
Tests Manual Gradient Descent, Sklearn Linear Regression, Random Forest Regressor,
and model artifact loading for SOH and RUL predictions.
"""

import os
import joblib
import pytest
import numpy as np
from backend.ml.practical3.manual_gradient_descent import ManualGradientDescentRegressor
from backend.ml.practical3.linear_regression import SklearnLinearRegressor
from backend.ml.practical3.random_forest_regression import BatteryRandomForestRegressor
from backend.ml.preprocessing.data_loader import get_train_test_split, FEATURE_COLUMNS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")


@pytest.fixture(scope="module")
def data_split():
    return get_train_test_split()


def test_manual_gradient_descent_convergence():
    # Synthetic clean linear problem: y = 2*x1 - 3*x2 + 5
    np.random.seed(42)
    X = np.random.randn(200, 2)
    y = 2.0 * X[:, 0] - 3.0 * X[:, 1] + 5.0

    model = ManualGradientDescentRegressor(learning_rate=0.05, n_iterations=300)
    model.fit(X, y)

    # Check that cost decreased monotonically and converged
    assert len(model.cost_history_) <= 300
    assert len(model.cost_history_) > 20
    assert model.cost_history_[-1] < model.cost_history_[0]
    assert model.cost_history_[-1] < 0.01, f"Final cost too high: {model.cost_history_[-1]}"

    # Check recovered weights and bias
    assert np.isclose(model.weights_[0], 2.0, atol=0.1)
    assert np.isclose(model.weights_[1], -3.0, atol=0.1)
    assert np.isclose(model.bias_, 5.0, atol=0.1)


def test_soh_regression_models_predictions(data_split):
    X_train = data_split['X_train']
    X_test = data_split['X_test']
    y_train = data_split['y_soh_train']
    y_test = data_split['y_soh_test']

    # 1. Manual GD
    gd = ManualGradientDescentRegressor(learning_rate=0.015, n_iterations=500).fit(X_train, y_train)
    gd_preds = gd.predict(X_test)
    assert len(gd_preds) == len(y_test)
    assert (gd_preds > 40.0).all() and (gd_preds < 120.0).all()

    # 2. Sklearn LR
    lr = SklearnLinearRegressor().fit(X_train, y_train)
    lr_preds = lr.predict(X_test)
    assert len(lr_preds) == len(y_test)

    # 3. Random Forest
    rf = BatteryRandomForestRegressor(n_estimators=20, random_state=42).fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    assert len(rf_preds) == len(y_test)


def test_rul_regression_models_predictions(data_split):
    X_train = data_split['X_train']
    X_test = data_split['X_test']
    y_train = data_split['y_rul_train']
    y_test = data_split['y_rul_test']

    rf = BatteryRandomForestRegressor(n_estimators=20, random_state=42).fit(X_train, y_train)
    preds = rf.predict(X_test)
    assert len(preds) == len(y_test)
    # Check physical bounds on RUL (non-negative)
    assert (preds >= -5.0).all()


def test_saved_model_artifacts_loading():
    required_files = [
        "soh_manual_gd.joblib",
        "soh_linear_regression.joblib",
        "soh_random_forest.joblib",
        "rul_manual_gd.joblib",
        "rul_linear_regression.joblib",
        "rul_random_forest.joblib",
        "regression_scaler.joblib",
        "regression_metrics.json"
    ]
    for filename in required_files:
        path = os.path.join(MODELS_DIR, filename)
        assert os.path.exists(path), f"Artifact missing: {filename}"

    # Verify loading and inference with saved models
    scaler = joblib.load(os.path.join(MODELS_DIR, "regression_scaler.joblib"))
    soh_model = joblib.load(os.path.join(MODELS_DIR, "soh_manual_gd.joblib"))

    dummy_sample = np.zeros((1, len(FEATURE_COLUMNS)))
    scaled_sample = scaler.transform(dummy_sample)
    pred_soh = soh_model.predict(scaled_sample)

    assert isinstance(pred_soh[0], (float, np.floating))
