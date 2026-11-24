"""
VoltGuard AI - Practical 5 Unit & Validation Tests
Validates Stacking, AdaBoost, and Hard Voting ensembles,
out-of-fold probability outputs, and serialized ensemble model loading.
"""

import os
import joblib
import pytest
import numpy as np
from backend.ml.preprocessing.data_loader import get_train_test_split, FEATURE_COLUMNS, HEALTH_CATEGORIES
from backend.ml.practical5.ensemble_models import (
    BatteryStackingEnsemble,
    BatteryAdaBoostEnsemble,
    BatteryVotingEnsemble
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")


@pytest.fixture(scope="module")
def data_split():
    return get_train_test_split()


def test_stacking_ensemble_fit_and_predict(data_split):
    X_train = data_split['X_train']
    X_test = data_split['X_test']
    y_train = data_split['y_cat_train']
    y_test = data_split['y_cat_test']

    stacking = BatteryStackingEnsemble(cv=3, random_state=42)
    stacking.fit(X_train, y_train)

    preds = stacking.predict(X_test)
    probs = stacking.predict_proba(X_test)

    assert len(preds) == len(y_test)
    assert set(preds).issubset({0, 1, 2, 3})
    assert probs.shape == (len(y_test), 4)
    assert np.allclose(np.sum(probs, axis=1), 1.0, atol=1e-3)


def test_adaboost_ensemble_fit_and_predict(data_split):
    X_train = data_split['X_train']
    X_test = data_split['X_test']
    y_train = data_split['y_cat_train']
    y_test = data_split['y_cat_test']

    adaboost = BatteryAdaBoostEnsemble(n_estimators=10, random_state=42)
    adaboost.fit(X_train, y_train)

    preds = adaboost.predict(X_test)
    probs = adaboost.predict_proba(X_test)

    assert len(preds) == len(y_test)
    assert set(preds).issubset({0, 1, 2, 3})
    assert probs.shape == (len(y_test), 4)
    assert np.allclose(np.sum(probs, axis=1), 1.0, atol=1e-3)


def test_voting_ensemble_fit_and_predict(data_split):
    X_train = data_split['X_train']
    X_test = data_split['X_test']
    y_train = data_split['y_cat_train']
    y_test = data_split['y_cat_test']

    voting = BatteryVotingEnsemble(random_state=42)
    voting.fit(X_train, y_train)

    preds = voting.predict(X_test)
    assert len(preds) == len(y_test)
    assert set(preds).issubset({0, 1, 2, 3})


def test_saved_ensemble_artifacts_loading():
    required_files = [
        "ensemble_stacking.joblib",
        "ensemble_adaboost.joblib",
        "ensemble_voting.joblib",
        "ensemble_comparison_metrics.json"
    ]
    for filename in required_files:
        path = os.path.join(MODELS_DIR, filename)
        assert os.path.exists(path), f"Saved ensemble artifact missing: {filename}"

    scaler = joblib.load(os.path.join(MODELS_DIR, "regression_scaler.joblib"))
    stacking_loaded = joblib.load(os.path.join(MODELS_DIR, "ensemble_stacking.joblib"))

    dummy_sample = np.zeros((1, len(FEATURE_COLUMNS)))
    scaled_sample = scaler.transform(dummy_sample)

    pred = stacking_loaded.predict(scaled_sample)
    probs = stacking_loaded.predict_proba(scaled_sample)

    assert int(pred[0]) in {0, 1, 2, 3}
    assert probs.shape == (1, 4)
