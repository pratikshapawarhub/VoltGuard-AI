"""
VoltGuard AI - Practical 6 API Router
Provides K-Means clustering assignment, Elbow diagnostics, and cluster profiles.
"""

import numpy as np
from fastapi import APIRouter
from backend.app.schemas.battery import BatteryMeasurementInput, ClusteringResponse
from backend.app.engine.model_loader import registry

router = APIRouter(prefix="/api/practical6", tags=["Practical 6 - Battery Clustering"])


@router.post("/cluster", response_model=ClusteringResponse)
def assign_cluster(input_data: BatteryMeasurementInput):
    """
    Assigns battery measurement to an unsupervised usage cluster based on:
    SOH, Capacity, Temperature, Impedance, and Cycle Number.
    """
    registry.load_all()

    # Estimate SOH for clustering
    raw_reg = np.array([[
        input_data.cycle_number, input_data.voltage_mean, input_data.voltage_max,
        input_data.voltage_min, input_data.voltage_std, input_data.current_mean,
        input_data.current_std, input_data.temperature_mean, input_data.temperature_max,
        input_data.temperature_min, input_data.charge_duration, input_data.discharge_duration,
        input_data.internal_impedance
    ]])
    scaled_reg = registry.get_model("regression_scaler").transform(raw_reg)
    soh_est = float(registry.get_model("soh_linear_regression").predict(scaled_reg)[0])
    cap_est = (soh_est / 100.0) * 2.0

    cluster_raw = np.array([[
        soh_est, cap_est, input_data.temperature_max,
        input_data.internal_impedance, input_data.cycle_number
    ]])

    kmeans_scaler = registry.get_model("kmeans_scaler")
    kmeans_model = registry.get_model("kmeans_model")
    scaled_c = kmeans_scaler.transform(cluster_raw)
    c_id = int(kmeans_model.predict(scaled_c)[0])

    cluster_meta = registry.get_metrics("clustering").get("Cluster_Profiles", {}).get(str(c_id), {})
    return ClusteringResponse(
        cluster_id=c_id,
        cluster_name=cluster_meta.get("cluster_name", f"Cluster {c_id}"),
        description=cluster_meta.get("description", "Learned operating cluster"),
        cluster_means=cluster_meta.get("means", {})
    )


@router.get("/elbow")
def get_elbow_curve():
    """
    Returns WCSS (Inertia), Silhouette scores, and Davies-Bouldin index for K=2 to 8.
    """
    return registry.get_metrics("clustering").get("Elbow_Diagnostics", {})


@router.get("/metrics")
def get_clustering_metrics():
    """
    Returns complete K-Means evaluation metrics and cluster centroid profiles.
    """
    return registry.get_metrics("clustering")
