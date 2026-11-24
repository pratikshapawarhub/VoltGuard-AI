"""
VoltGuard AI - Enterprise Product API Tests
Tests Battery Asset CRUD, Alerts management, Maintenance Work Orders, and Reports endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_battery_assets_crud():
    # 1. Overview KPIs
    resp = client.get("/api/batteries/overview")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_batteries" in data
    assert data["total_batteries"] >= 4  # Seeded with B0005, B0006, B0007, B0018, EV-PACK-01

    # 2. List batteries
    resp = client.get("/api/batteries")
    assert resp.status_code == 200
    batteries = resp.json()
    assert len(batteries) >= 4
    battery_ids = [b["battery_id"] for b in batteries]
    assert "B0005" in battery_ids
    assert "B0018" in battery_ids

    # 3. Create a new test battery
    test_id = "TEST-BAT-99"
    create_payload = {
        "battery_id": test_id,
        "name": "Integration Test Battery Pack",
        "chemistry": "LFP / Graphite",
        "nominal_capacity": 50.0,
        "nominal_voltage": 48.0,
        "installation_date": "2024-03-01",
        "status": "ACTIVE",
        "location": "Test Rig Alpha",
        "notes": "Automated test battery"
    }
    resp = client.post("/api/batteries", json=create_payload)
    assert resp.status_code == 201
    created = resp.json()
    assert created["battery_id"] == test_id
    assert created["current_soh"] == 100.0

    # 4. Get by ID
    resp = client.get(f"/api/batteries/{test_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Integration Test Battery Pack"

    # 5. Update battery
    update_payload = {"name": "Updated Test Battery Pack", "status": "MAINTENANCE"}
    resp = client.put(f"/api/batteries/{test_id}", json=update_payload)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Test Battery Pack"
    assert resp.json()["status"] == "MAINTENANCE"

    # 6. Delete test battery
    resp = client.delete(f"/api/batteries/{test_id}")
    assert resp.status_code == 204

    # Verify deleted
    resp = client.get(f"/api/batteries/{test_id}")
    assert resp.status_code == 404


def test_alerts_lifecycle():
    # 1. List alerts
    resp = client.get("/api/alerts")
    assert resp.status_code == 200
    alerts = resp.json()
    assert len(alerts) >= 1

    first_alert = alerts[0]
    alert_id = first_alert["id"]

    # 2. Stats
    resp = client.get("/api/alerts/stats")
    assert resp.status_code == 200
    stats = resp.json()
    assert "active_alerts" in stats

    # 3. Acknowledge alert
    resp = client.put(f"/api/alerts/{alert_id}/status", json={"status": "ACKNOWLEDGED"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "ACKNOWLEDGED"

    # 4. Resolve alert
    resp = client.put(f"/api/alerts/{alert_id}/status", json={"status": "RESOLVED"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "RESOLVED"
    assert resp.json()["resolved_at"] is not None


def test_maintenance_tasks():
    # 1. List tasks
    resp = client.get("/api/maintenance/tasks")
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) >= 1

    # 2. Create task
    task_payload = {
        "battery_id": "B0005",
        "title": "Scheduled Capacity Re-verification",
        "priority": "ROUTINE",
        "technician_name": "Bob (Junior Tech)",
        "scheduled_slot": "SLOT_1400",
        "estimated_duration_hours": 1.0,
        "estimated_cost": 85.0,
        "search_algorithm_used": "A* Search",
        "servicing_path": "PRELIMINARY_SCAN -> CALIBRATION_TEST -> CERTIFIED_OPERATIONAL"
    }
    resp = client.post("/api/maintenance/tasks", json=task_payload)
    assert resp.status_code == 201
    created_task = resp.json()
    task_id = created_task["task_id"]
    assert created_task["status"] == "SCHEDULED"

    # 3. Update task to COMPLETED
    resp = client.put(f"/api/maintenance/tasks/{task_id}", json={"status": "COMPLETED"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "COMPLETED"
    assert resp.json()["completed_at"] is not None

    # 4. Delete task
    resp = client.delete(f"/api/maintenance/tasks/{task_id}")
    assert resp.status_code == 204


def test_reports_and_exports():
    # 1. Summary
    resp = client.get("/api/reports/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_assets" in data
    assert "assets_summary" in data

    # 2. CSV Exports
    for rtype in ["assets", "history", "maintenance", "alerts"]:
        resp = client.get(f"/api/reports/export-csv?report_type={rtype}")
        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]
        assert len(resp.text) > 0
