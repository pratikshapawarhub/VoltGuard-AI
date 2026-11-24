/**
 * VoltGuard AI - Enterprise API Client Service
 * Communicates with FastAPI backend for Fleet Management, Predictive Intelligence,
 * Maintenance Operations, and AIML Core Engines.
 */

const BASE_URL = import.meta.env.VITE_API_URL || '';

async function handleResponse(response) {
  if (!response.ok) {
    let errorDetail = 'API request failed';
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || JSON.stringify(errorJson);
    } catch {
      errorDetail = await response.text();
    }
    throw new Error(errorDetail);
  }
  return response.json();
}

export const api = {
  // System root & health
  getHealth: () => fetch(`${BASE_URL}/`).then(handleResponse),

  // Module 1 & 2: Battery Asset Management
  getFleetOverview: () => fetch(`${BASE_URL}/api/batteries/overview`).then(handleResponse),
  listBatteries: (search = null, status = null, chemistry = null) => {
    let url = `${BASE_URL}/api/batteries?`;
    const params = [];
    if (search) params.push(`search=${encodeURIComponent(search)}`);
    if (status) params.push(`status=${encodeURIComponent(status)}`);
    if (chemistry) params.push(`chemistry=${encodeURIComponent(chemistry)}`);
    url += params.join('&');
    return fetch(url).then(handleResponse);
  },
  getBattery: (batteryId) => fetch(`${BASE_URL}/api/batteries/${batteryId}`).then(handleResponse),
  registerBattery: (data) => fetch(`${BASE_URL}/api/batteries`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  updateBattery: (batteryId, data) => fetch(`${BASE_URL}/api/batteries/${batteryId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  deleteBattery: (batteryId) => fetch(`${BASE_URL}/api/batteries/${batteryId}`, {
    method: 'DELETE'
  }).then((res) => {
    if (!res.ok) throw new Error('Failed to delete battery');
    return true;
  }),
  getBatteryHistory: (batteryId, limit = 50) => fetch(`${BASE_URL}/api/batteries/${batteryId}/history?limit=${limit}`).then(handleResponse),

  // Module 7: Alerts & Notifications
  listAlerts: (status = null, severity = null, batteryId = null, limit = 50) => {
    let url = `${BASE_URL}/api/alerts?limit=${limit}`;
    if (status) url += `&status=${encodeURIComponent(status)}`;
    if (severity) url += `&severity=${encodeURIComponent(severity)}`;
    if (batteryId) url += `&battery_id=${encodeURIComponent(batteryId)}`;
    return fetch(url).then(handleResponse);
  },
  getAlertStats: () => fetch(`${BASE_URL}/api/alerts/stats`).then(handleResponse),
  updateAlertStatus: (alertId, status) => fetch(`${BASE_URL}/api/alerts/${alertId}/status`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status })
  }).then(handleResponse),

  // Module 6: Predictive Maintenance Operations
  listMaintenanceTasks: (status = null, priority = null, batteryId = null) => {
    let url = `${BASE_URL}/api/maintenance/tasks?`;
    const params = [];
    if (status) params.push(`status=${encodeURIComponent(status)}`);
    if (priority) params.push(`priority=${encodeURIComponent(priority)}`);
    if (batteryId) params.push(`battery_id=${encodeURIComponent(batteryId)}`);
    url += params.join('&');
    return fetch(url).then(handleResponse);
  },
  createMaintenanceTask: (data) => fetch(`${BASE_URL}/api/maintenance/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  updateMaintenanceTask: (taskId, data) => fetch(`${BASE_URL}/api/maintenance/tasks/${taskId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  deleteMaintenanceTask: (taskId) => fetch(`${BASE_URL}/api/maintenance/tasks/${taskId}`, {
    method: 'DELETE'
  }).then((res) => {
    if (!res.ok) throw new Error('Failed to delete task');
    return true;
  }),

  // Module 8: Reporting & Data Export
  getReportSummary: () => fetch(`${BASE_URL}/api/reports/summary`).then(handleResponse),
  getExportCsvUrl: (reportType = 'assets') => `${BASE_URL}/api/reports/export-csv?report_type=${reportType}`,

  // Dataset & Cycle Telemetry
  getDatasetSummary: () => fetch(`${BASE_URL}/api/dataset/summary`).then(handleResponse),
  getDatasetRecords: (batteryId = null, limit = 50, offset = 0) => {
    let url = `${BASE_URL}/api/dataset/records?limit=${limit}&offset=${offset}`;
    if (batteryId) url += `&battery_id=${batteryId}`;
    return fetch(url).then(handleResponse);
  },
  uploadCsv: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return fetch(`${BASE_URL}/api/dataset/upload-csv`, {
      method: 'POST',
      body: formData
    }).then(handleResponse);
  },

  // Practical 1: PEAS & Rule-Based Expert System (Intelligent Monitoring Agent)
  getPeasMatrix: () => fetch(`${BASE_URL}/api/practical1/peas`).then(handleResponse),
  evaluateExpertRules: (data) => fetch(`${BASE_URL}/api/practical1/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),

  // Practical 2: Search Algorithms & CSP (Maintenance Planner)
  getBfsPlan: (start, goal) => {
    let url = `${BASE_URL}/api/practical2/bfs`;
    if (start && goal) url += `?start_state=${start}&goal_state=${goal}`;
    return fetch(url).then(handleResponse);
  },
  getDfsPlan: (start, goal) => {
    let url = `${BASE_URL}/api/practical2/dfs`;
    if (start && goal) url += `?start_state=${start}&goal_state=${goal}`;
    return fetch(url).then(handleResponse);
  },
  getAStarPlan: (start, goal) => {
    let url = `${BASE_URL}/api/practical2/a-star`;
    if (start && goal) url += `?start_state=${start}&goal_state=${goal}`;
    return fetch(url).then(handleResponse);
  },
  getHillClimbingSchedule: () => fetch(`${BASE_URL}/api/practical2/hill-climbing`).then(handleResponse),
  getCspSchedule: () => fetch(`${BASE_URL}/api/practical2/csp`).then(handleResponse),
  getSearchComparison: () => fetch(`${BASE_URL}/api/practical2/compare`).then(handleResponse),

  // Practical 3: Regression Models (SOH & RUL Prognosis)
  predictSoh: (data) => fetch(`${BASE_URL}/api/practical3/predict-soh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  predictRul: (data) => fetch(`${BASE_URL}/api/practical3/predict-rul`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  getRegressionMetrics: () => fetch(`${BASE_URL}/api/practical3/metrics`).then(handleResponse),

  // Practical 4: Classification (Condition Assessment)
  classifyCondition: (data) => fetch(`${BASE_URL}/api/practical4/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  getClassificationMetrics: () => fetch(`${BASE_URL}/api/practical4/metrics`).then(handleResponse),

  // Practical 5: Ensemble Learning (Combined Prediction Engine)
  predictEnsemble: (data) => fetch(`${BASE_URL}/api/practical5/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  getEnsembleMetrics: () => fetch(`${BASE_URL}/api/practical5/metrics`).then(handleResponse),

  // Practical 6: Clustering (Battery Usage Segmentation)
  assignCluster: (data) => fetch(`${BASE_URL}/api/practical6/cluster`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  getElbowCurve: () => fetch(`${BASE_URL}/api/practical6/elbow`).then(handleResponse),
  getClusteringMetrics: () => fetch(`${BASE_URL}/api/practical6/metrics`).then(handleResponse),

  // Practical 7: Integrated Predictive Maintenance Engine & History
  runIntegratedEngine: (data) => fetch(`${BASE_URL}/api/practical7/predict-all`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(handleResponse),
  getPredictionHistory: (limit = 50) => fetch(`${BASE_URL}/api/practical7/history?limit=${limit}`).then(handleResponse)
};
