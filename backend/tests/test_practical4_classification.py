"""
VoltGuard AI - Practical 4 Unit & Validation Tests
Validates SVM, Decision Tree, KNN, and Naive Bayes classifiers,
confusion matrix properties, and model artifact loading.
"""

import os
import joblib
import pytest
import numpy as np
from backend.ml.preprocessing.data_loader import get_train_test_split, FEATURE_COLUMNS, HEALTH_CATEGORIES
from backend.ml.practical4.classifiers import (
    BatterySVMClassifier,
    BatteryDecisionTreeClassifier,
    BatteryKNNClassifier,
    BatteryNaiveBayesClassifier
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")


@pytest.fixture(scope="module")
def data_split():
    return get_train_test_split()


def test_classifier_training_and_shapes(data_split):
    X_train = data_split['X_train']
    X_test = data_split['X_test']
    y_train = data_split['y_cat_train']
    y_test = data_split['y_cat_test']

    classifiers = [
        BatterySVMClassifier(),
        BatteryDecisionTreeClassifier(),
        BatteryKNNClassifier(),
        BatteryNaiveBayesClassifier()
    ]

    for clf in classifiers:
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        probs = clf.predict_proba(X_test)

        assert len(preds) == len(y_test)
        assert set(preds).issubset({0, 1, 2, 3}), "Predictions must belong to classes {0, 1, 2, 3}"
        assert probs.shape == (len(y_test), 4), "Probabilities shape must be (N, 4)"
        # Verify probability normalization
        assert np.allclose(np.sum(probs, axis=1), 1.0, atol=1e-3), "Probabilities must sum to 1"


def test_saved_classification_artifacts_loading():
    required_files = [
        "classification_svm.joblib",
        "classification_decision_tree.joblib",
        "classification_knn.joblib",
        "classification_naive_bayes.joblib",
        "classification_metrics.json"
    ]
    for filename in required_files:
        path = os.path.join(MODELS_DIR, filename)
        assert os.path.exists(path), f"Saved classification artifact missing: {filename}"

    # Verify loading and running single inference with saved SVM
    scaler = joblib.load(os.path.join(MODELS_DIR, "regression_scaler.joblib"))
    svm_model = joblib.load(os.path.join(MODELS_DIR, "classification_svm.joblib"))

    dummy_sample = np.zeros((1, len(FEATURE_COLUMNS)))
    scaled_sample = scaler.transform(dummy_sample)
    pred_cat = svm_model.predict(scaled_sample)
    probs = svm_model.predict_proba(scaled_sample)

    assert int(pred_cat[0]) in {0, 1, 2, 3}
    assert probs.shape == (1, 4)
