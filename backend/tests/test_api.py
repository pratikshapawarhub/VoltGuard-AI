"""
VoltGuard AI - FastAPI Integration Tests
Tests all REST endpoints across Practicals 1 to 7 using Starlette TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

SAMPLE_MEASUREMENT = {
    "battery_id": "TEST_CELL_01",
    "cycle_number": 85,
    "voltage_mean": 3.49,
    "voltage_max": 4.19,
    "voltage_min": 2.42,
    "voltage_std": 0.24,
    "current_mean": 1.84,
    "current_std": 0.52,
    "temperature_mean": 32.4,
    "temperature_max": 39.8,
    "temperature_min": 24.1,
    "charge_duration": 10500.0,
    "discharge_duration": 3080.0,
    "internal_impedance": 0.145,
    "recent_soh_drop": 0.6
}


def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OPERATIONAL"
    assert len(data["practicals_available"]) == 7


def test_dataset_endpoints():
    # Summary
    resp = client.get("/api/dataset/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_records"] == 636
    assert "B0005" in data["batteries"]
    assert data["average_soh"] > 70.0

    # Records pagination
    resp = client.get("/api/dataset/records?limit=10&offset=0")
    assert resp.status_code == 200
    assert len(resp.json()["records"]) == 10


def test_practical1_endpoints():
    # PEAS
    resp = client.get("/api/practical1/peas")
    assert resp.status_code == 200
    assert "Performance_Measure" in resp.json()["dimensions"]

    # Expert System evaluation
    resp = client.post("/api/practical1/evaluate", json=SAMPLE_MEASUREMENT)
    assert resp.status_code == 200
    assert resp.json()["overall_status"] in ["HEALTHY", "WARNING", "CRITICAL"]


def test_practical2_endpoints():
    for algo in ["bfs", "dfs", "a-star", "hill-climbing", "csp", "compare"]:
        resp = client.get(f"/api/practical2/{algo}")
        assert resp.status_code == 200, f"Failed on endpoint /api/practical2/{algo}"


def test_practical3_endpoints():
    # SOH Prediction
    resp = client.post("/api/practical3/predict-soh", json=SAMPLE_MEASUREMENT)
    assert resp.status_code == 200
    soh_data = resp.json()
    assert 40.0 <= soh_data["recommended_soh"] <= 110.0

    # RUL Prediction
    resp = client.post("/api/practical3/predict-rul", json=SAMPLE_MEASUREMENT)
    assert resp.status_code == 200
    rul_data = resp.json()
    assert rul_data["recommended_rul"] >= 0.0

    # Metrics
    resp = client.get("/api/practical3/metrics")
    assert resp.status_code == 200


def test_practical4_endpoints():
    # Classify
    resp = client.post("/api/practical4/classify", json=SAMPLE_MEASUREMENT)
    assert resp.status_code == 200
    assert resp.json()["predicted_category"] in ["Healthy", "Moderate", "Degraded", "Critical"]

    # Metrics
    resp = client.get("/api/practical4/metrics")
    assert resp.status_code == 200


def test_practical5_endpoints():
    # Ensemble predict
    resp = client.post("/api/practical5/predict", json=SAMPLE_MEASUREMENT)
    assert resp.status_code == 200
    data = resp.json()
    assert data["consensus_category"] in ["Healthy", "Moderate", "Degraded", "Critical"]

    # Metrics
    resp = client.get("/api/practical5/metrics")
    assert resp.status_code == 200


def test_practical6_endpoints():
    # Clustering
    resp = client.post("/api/practical6/cluster", json=SAMPLE_MEASUREMENT)
    assert resp.status_code == 200
    assert resp.json()["cluster_id"] in [0, 1, 2]

    # Elbow
    resp = client.get("/api/practical6/elbow")
    assert resp.status_code == 200

    # Metrics
    resp = client.get("/api/practical6/metrics")
    assert resp.status_code == 200


def test_practical7_integrated_and_history():
    # Run full integrated pipeline
    resp = client.post("/api/practical7/predict-all", json=SAMPLE_MEASUREMENT)
    assert resp.status_code == 200
    data = resp.json()

    assert data["soh_prediction"]["recommended_soh"] > 0
    assert data["rul_prediction"]["recommended_rul"] >= 0
    assert data["condition_classification"]["predicted_category"] in ["Healthy", "Moderate", "Degraded", "Critical"]
    assert data["ensemble_classification"]["consensus_category"] in ["Healthy", "Moderate", "Degraded", "Critical"]
    assert data["usage_clustering"]["cluster_id"] in [0, 1, 2]
    assert data["optimal_maintenance_plan"]["total_cost"] > 0
    assert data["database_record_id"] is not None

    # Verify history retrieval
    resp = client.get("/api/practical7/history?limit=10")
    assert resp.status_code == 200
    history = resp.json()
    assert len(history) >= 1
    assert history[0]["battery_id"] == "TEST_CELL_01"
