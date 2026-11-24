# VoltGuard AI: REST API Technical Specification

**Document ID:** `API-VG-2026-V1`  
**System Name:** VoltGuard AI – Intelligent Battery Health & Predictive Maintenance Platform  
**Base URL:** `http://localhost:8000`  
**Protocol:** HTTP/1.1 RESTful JSON  
**OpenAPI Spec:** Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)  
**Date:** November 23, 2026  

---

## 1. Global API Standards

- **Request Encoding:** `application/json` (or `multipart/form-data` for CSV file uploads).
- **Response Format:** UTF-8 encoded JSON.
- **Error Standard:** Standard HTTP status codes with structured `{ "detail": "<error explanation>" }` bodies.
- **CORS:** Enabled for local dev and frontend clients (`http://localhost:5173`, `http://127.0.0.1:5173`).

---

## 2. API Endpoints Directory

### 2.1 System & Root
- **`GET /`**
  - **Description:** Returns platform status, branding tagline, active modules, and integrated practicals.
  - **Status Code:** `200 OK`
  - **Response Payload:**
    ```json
    {
      "platform": "VoltGuard AI",
      "tagline": "Intelligent Battery Health. Predictive Maintenance. Smarter Decisions.",
      "status": "OPERATIONAL",
      "documentation": "/docs",
      "modules": [...],
      "practicals_available": [...]
    }
    ```

---

### 2.2 Battery Asset Management (`/api/batteries`)

- **`GET /api/batteries`**
  - **Description:** List registered battery assets with optional search and filtering.
  - **Query Parameters:**
    - `search` (string, optional): Search by battery ID, name, or location.
    - `status` (string, optional): `ACTIVE`, `MAINTENANCE`, `DECOMMISSIONED`.
    - `chemistry` (string, optional): Filter by chemistry.
  - **Status Code:** `200 OK`
  - **Response:** Array of `BatteryAssetResponse` objects.

- **`GET /api/batteries/overview`**
  - **Description:** Returns aggregate fleet KPIs for the overview dashboard.
  - **Status Code:** `200 OK`
  - **Response Payload:**
    ```json
    {
      "total_batteries": 5,
      "active_batteries": 4,
      "maintenance_batteries": 1,
      "decommissioned_batteries": 0,
      "average_soh": 72.6,
      "average_rul": 39.8,
      "critical_alerts_count": 3,
      "active_maintenance_tasks": 1,
      "health_distribution": { "Healthy": 1, "Moderate": 0, "Degraded": 1, "Critical": 3 },
      "operating_regimes_distribution": { ... }
    }
    ```

- **`POST /api/batteries`**
  - **Description:** Registers a new physical or virtual battery pack.
  - **Status Code:** `201 Created`
  - **Request Body (`BatteryAssetCreate`):**
    ```json
    {
      "battery_id": "EV-PACK-05",
      "name": "Fleet Delivery Van 05",
      "chemistry": "NMC 811 / Silicon",
      "nominal_capacity": 60.0,
      "nominal_voltage": 48.0,
      "installation_date": "2024-03-01",
      "status": "ACTIVE",
      "location": "Bay C - Depot 2",
      "notes": "Commissioned for logistics route."
    }
    ```

- **`GET /api/batteries/{battery_id}`**
  - **Description:** Fetches detailed specifications and current status for a single battery.
  - **Status Code:** `200 OK` (or `404 Not Found`).

- **`PUT /api/batteries/{battery_id}`**
  - **Description:** Updates battery metadata (name, status, location, notes).
  - **Status Code:** `200 OK`.

- **`DELETE /api/batteries/{battery_id}`**
  - **Description:** Decommissions and deletes a battery asset from the registry.
  - **Status Code:** `204 No Content`.

- **`GET /api/batteries/{battery_id}/history`**
  - **Description:** Returns paginated diagnostic prediction history and cycle records for the asset.
  - **Status Code:** `200 OK`.

---

### 2.3 Alerts & Notifications Management (`/api/alerts`)

- **`GET /api/alerts`**
  - **Description:** Returns operational anomaly alerts with optional filters.
  - **Query Parameters:** `status` (`ACTIVE`, `ACKNOWLEDGED`, `RESOLVED`), `severity` (`CRITICAL`, `WARNING`, `INFO`), `battery_id`, `limit`.
  - **Status Code:** `200 OK`.

- **`GET /api/alerts/stats`**
  - **Description:** Returns counts of active, critical, warning, and resolved alerts.
  - **Status Code:** `200 OK`.

- **`PUT /api/alerts/{alert_id}/status`**
  - **Description:** Updates alert lifecycle state (e.g. mark `ACKNOWLEDGED` or `RESOLVED`).
  - **Request Body:** `{ "status": "RESOLVED" }`
  - **Status Code:** `200 OK`.

---

### 2.4 Predictive Maintenance Operations (`/api/maintenance`)

- **`GET /api/maintenance/tasks`**
  - **Description:** Returns maintenance work orders with optional filtering by status or priority.
  - **Status Code:** `200 OK`.

- **`POST /api/maintenance/tasks`**
  - **Description:** Dispatches a new maintenance work order.
  - **Status Code:** `201 Created`.
  - **Request Body:**
    ```json
    {
      "battery_id": "B0006",
      "title": "Emergency Cell Decommission & Replacement",
      "priority": "CRITICAL",
      "technician_name": "Alice (Senior Specialist)",
      "is_senior_required": true,
      "scheduled_slot": "SLOT_0900",
      "estimated_duration_hours": 1.5,
      "estimated_cost": 130.0,
      "search_algorithm_used": "A* Search",
      "servicing_path": "CRITICAL_FAULT -> ISOLATION -> CELL_REPLACEMENT"
    }
    ```

- **`PUT /api/maintenance/tasks/{task_id}`**
  - **Description:** Updates work order status (e.g. to `IN_PROGRESS` or `COMPLETED`) and notes.
  - **Status Code:** `200 OK`.

- **`DELETE /api/maintenance/tasks/{task_id}`**
  - **Description:** Cancels and deletes a maintenance task.
  - **Status Code:** `204 No Content`.

---

### 2.5 Reporting & CSV Data Exports (`/api/reports`)

- **`GET /api/reports/summary`**
  - **Description:** Generates a system-wide diagnostic intelligence summary.
  - **Status Code:** `200 OK`.

- **`GET /api/reports/export-csv`**
  - **Description:** Streams a dynamically generated CSV export file.
  - **Query Parameters:** `report_type` (`assets`, `history`, `maintenance`, or `alerts`).
  - **Headers:** `Content-Type: text/csv`, `Content-Disposition: attachment; filename=...`
  - **Status Code:** `200 OK`.

---

### 2.6 Integrated Predictive Engine (`/api/practical7`)

- **`POST /api/practical7/predict-all`**
  - **Description:** End-to-end multi-model inference pipeline executing SOH/RUL regression, 4-class classification, ensemble consensus, K-Means clustering, expert rule evaluation, A* search planning, asset state synchronization, and alert logging in a single transactional call.
  - **Status Code:** `200 OK`.
  - **Request Body (`BatteryMeasurementInput`):**
    ```json
    {
      "battery_id": "B0006",
      "cycle_number": 85,
      "voltage_mean": 3.42,
      "voltage_max": 4.19,
      "voltage_min": 2.35,
      "voltage_std": 0.28,
      "current_mean": 1.95,
      "current_std": 0.55,
      "temperature_mean": 35.0,
      "temperature_max": 48.5,
      "temperature_min": 24.0,
      "charge_duration": 10400.0,
      "discharge_duration": 2800.0,
      "internal_impedance": 0.175,
      "recent_soh_drop": 1.5
    }
    ```
  - **Response Payload:** Contains complete prediction results, probabilities, cluster name, triggered rules array, A* path, and database record ID.

---
*API Specification certified for integration.*
