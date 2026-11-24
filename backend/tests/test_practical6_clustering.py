"""
VoltGuard AI - Practical 6 Unit & Validation Tests
Validates K-Means clustering, Elbow method diagnostics, Silhouette and
Davies-Bouldin evaluation metrics, and serialized model loading.
"""

import os
import joblib
import pytest
import numpy as np
from backend.ml.preprocessing.data_loader import load_cleaned_dataset
from backend.ml.practical6.kmeans_clustering import BatteryKMeansClusterer, CLUSTERING_FEATURES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")


@pytest.fixture(scope="module")
def clustering_data():
    df = load_cleaned_dataset()
    return df[CLUSTERING_FEATURES].values


def test_elbow_metrics_computation(clustering_data):
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(clustering_data)

    k_range = range(2, 6)
    diagnostics = BatteryKMeansClusterer.compute_elbow_and_metrics(X_scaled, k_range=k_range)

    assert diagnostics["k_values"] == [2, 3, 4, 5]
    wcss = diagnostics["wcss"]
    # Inertia must decrease or stay equal as K increases
    for i in range(len(wcss) - 1):
        assert wcss[i] >= wcss[i + 1], "WCSS must decrease monotonically as K increases"

    # Verify Silhouette score bounds [-1, 1]
    for s in diagnostics["silhouette_scores"]:
        assert -1.0 <= s <= 1.0


def test_kmeans_fitting_and_evaluation(clustering_data):
    clusterer = BatteryKMeansClusterer(n_clusters=3, random_state=42)
    clusterer.fit(clustering_data)

    eval_results = clusterer.evaluate(clustering_data)
    assert eval_results["silhouette_score"] > 0.20
    assert eval_results["davies_bouldin_index"] > 0.0

    preds = clusterer.predict(clustering_data)
    assert len(preds) == len(clustering_data)
    assert set(preds) == {0, 1, 2}


def test_saved_clustering_artifacts_loading(clustering_data):
    required_files = [
        "kmeans_model.joblib",
        "kmeans_scaler.joblib",
        "clustering_metrics.json"
    ]
    for filename in required_files:
        path = os.path.join(MODELS_DIR, filename)
        assert os.path.exists(path), f"Saved clustering artifact missing: {filename}"

    # Load artifacts and run prediction
    kmeans = joblib.load(os.path.join(MODELS_DIR, "kmeans_model.joblib"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "kmeans_scaler.joblib"))

    dummy_sample = np.mean(clustering_data, axis=0, keepdims=True)
    scaled_sample = scaler.transform(dummy_sample)
    cluster_pred = kmeans.predict(scaled_sample)

    assert int(cluster_pred[0]) in {0, 1, 2}
