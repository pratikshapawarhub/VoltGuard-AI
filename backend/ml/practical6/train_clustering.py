"""
VoltGuard AI - Practical 6: Clustering Training & Evaluation Pipeline
Runs Elbow Method, Silhouette Analysis, Davies-Bouldin evaluation,
trains K-Means clustering, segments battery operating regimes,
and generates academic visualizations.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.ml.preprocessing.data_loader import load_cleaned_dataset
from backend.ml.practical6.kmeans_clustering import BatteryKMeansClusterer, CLUSTERING_FEATURES

MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")
FIGURES_DIR = os.path.join(BASE_DIR, "docs", "figures")


def train_and_evaluate_clustering() -> dict:
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    print("Loading cleaned NASA dataset for clustering...")
    df = load_cleaned_dataset()
    X = df[CLUSTERING_FEATURES].values

    # Fit a standard scaler for Elbow diagnostics
    scaler_diag = StandardScaler()
    X_scaled = scaler_diag.fit_transform(X)

    # 1. Compute Elbow & Diagnostic Metrics across K = 2 to 8
    print("Computing Elbow WCSS, Silhouette, and Davies-Bouldin metrics for K=2..8...")
    elbow_diagnostics = BatteryKMeansClusterer.compute_elbow_and_metrics(X_scaled, k_range=range(2, 9))

    # 2. Train Optimal K-Means Model (K=3 represents Fresh, Intermediate, and Degraded regimes)
    optimal_k = 3
    print(f"Training K-Means with optimal K = {optimal_k}...")
    clusterer = BatteryKMeansClusterer(n_clusters=optimal_k, random_state=42)
    clusterer.fit(X)

    eval_metrics = clusterer.evaluate(X)
    cluster_labels = clusterer.predict(X)
    profiles = clusterer.characterize_clusters(df[CLUSTERING_FEATURES], cluster_labels)

    # 3. Save Model Artifacts
    joblib.dump(clusterer.model, os.path.join(MODELS_DIR, "kmeans_model.joblib"))
    joblib.dump(clusterer.scaler, os.path.join(MODELS_DIR, "kmeans_scaler.joblib"))

    results = {
        "Optimal_K": optimal_k,
        "Evaluation": eval_metrics,
        "Elbow_Diagnostics": elbow_diagnostics,
        "Cluster_Profiles": profiles,
        "Clustering_Features": CLUSTERING_FEATURES
    }

    metrics_file = os.path.join(MODELS_DIR, "clustering_metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(results, f, indent=2)

    # ==========================================
    # Generate Visualizations for Report
    # ==========================================
    plt.style.use('dark_background')
    k_vals = elbow_diagnostics['k_values']

    # 1. Elbow (WCSS) & Silhouette Dual Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=150)
    
    # Elbow WCSS
    ax1.plot(k_vals, elbow_diagnostics['wcss'], marker='o', color='#38bdf8', linewidth=2, markersize=6)
    ax1.axvline(x=optimal_k, color='#f43f5e', linestyle='--', alpha=0.8, label=f'Optimal Elbow K={optimal_k}')
    ax1.set_title("Elbow Method: Within-Cluster Sum of Squares (WCSS)", fontsize=11, fontweight='bold')
    ax1.set_xlabel("Number of Clusters (K)")
    ax1.set_ylabel("Inertia / WCSS")
    ax1.legend(framealpha=0.3)
    ax1.grid(True, linestyle=":", alpha=0.3)

    # Silhouette Score
    ax2.plot(k_vals, elbow_diagnostics['silhouette_scores'], marker='s', color='#10b981', linewidth=2, markersize=6)
    ax2.axvline(x=optimal_k, color='#f43f5e', linestyle='--', alpha=0.8, label=f'Selected K={optimal_k} (Score: {eval_metrics["silhouette_score"]:.3f})')
    ax2.set_title("Silhouette Score vs Number of Clusters", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Number of Clusters (K)")
    ax2.set_ylabel("Silhouette Score")
    ax2.legend(framealpha=0.3)
    ax2.grid(True, linestyle=":", alpha=0.3)

    plt.suptitle("K-Means Cluster Diagnostics (Elbow & Silhouette)", fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "kmeans_elbow_and_silhouette.png"))
    plt.close()

    # 2. 2D Cluster Scatter Plot (SOH vs Internal Impedance)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    cluster_colors = ['#38bdf8', '#fbbf24', '#f43f5e']

    for c in range(optimal_k):
        mask = (cluster_labels == c)
        c_name = profiles[c]['cluster_name']
        ax.scatter(
            df.loc[mask, 'soh'],
            df.loc[mask, 'internal_impedance'],
            color=cluster_colors[c % len(cluster_colors)],
            label=f"Cluster {c}: {c_name} (n={np.sum(mask)})",
            alpha=0.7,
            s=45,
            edgecolors='none'
        )

    # Compute unscaled centroids for scatter plot
    centroids_scaled = clusterer.model.cluster_centers_
    centroids_unscaled = clusterer.scaler.inverse_transform(centroids_scaled)
    soh_idx = CLUSTERING_FEATURES.index('soh')
    imp_idx = CLUSTERING_FEATURES.index('internal_impedance')

    ax.scatter(
        centroids_unscaled[:, soh_idx],
        centroids_unscaled[:, imp_idx],
        color='white',
        s=140,
        marker='X',
        edgecolor='black',
        linewidth=1.5,
        label='Cluster Centroids',
        zorder=5
    )

    ax.set_title("Unsupervised Battery Usage Clusters: SOH vs Internal Impedance", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("State of Health (SOH %)", fontsize=11)
    ax.set_ylabel("Internal Impedance (Ohms, Re + Rct)", fontsize=11)
    ax.legend(loc='upper right', framealpha=0.4, fontsize=9)
    ax.grid(True, linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "kmeans_cluster_scatter.png"))
    plt.close()

    # 3. Cluster Distribution Bar Chart
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    c_names = [f"Cluster {c}\n{profiles[c]['cluster_name'].split(' / ')[0]}" for c in range(optimal_k)]
    counts = [profiles[c]['sample_count'] for c in range(optimal_k)]
    pcts = [profiles[c]['percentage'] for c in range(optimal_k)]

    bars = ax.bar(c_names, counts, color=cluster_colors, width=0.5, edgecolor='#1e293b')
    for idx, bar in enumerate(bars):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 5, f"{h} ({pcts[idx]}%)", ha='center', va='bottom', fontsize=10)

    ax.set_title(f"Cluster Sample Distribution (Total Cycles: {len(df)})", fontsize=12, fontweight='bold', pad=12)
    ax.set_ylabel("Cycle Count")
    ax.set_ylim(0, max(counts) + 40)
    ax.grid(axis='y', linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "kmeans_cluster_distribution.png"))
    plt.close()

    # 4. Cluster Characteristics Grouped Bar Chart
    fig, ax = plt.subplots(figsize=(11, 5), dpi=150)
    # Normalize feature means (0 to 1 scale across clusters) for comparison
    feat_display = ['soh', 'temperature_max', 'internal_impedance', 'cycle_number']
    feat_labels = ['SOH (%)', 'Max Temp (°C)', 'Impedance (Ω)', 'Cycle Number']
    
    x = np.arange(len(feat_display))
    w = 0.25

    for c in range(optimal_k):
        raw_vals = [profiles[c]['means'][f] for f in feat_display]
        ax.bar(x + (c - 1) * w, raw_vals, width=w, label=f"Cluster {c}: {profiles[c]['cluster_name'].split(' / ')[0]}", color=cluster_colors[c], edgecolor='#1e293b')

    ax.set_xticks(x)
    ax.set_xticklabels(feat_labels, fontsize=10)
    ax.set_title("Cluster Centroid Profiles across Physical Features", fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel("Mean Feature Value", fontsize=11)
    ax.legend(loc="upper right", framealpha=0.4)
    ax.grid(axis='y', linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "kmeans_cluster_characteristics.png"))
    plt.close()

    print("K-Means training, diagnostics, evaluation, and figures completed.")
    return results


if __name__ == "__main__":
    results = train_and_evaluate_clustering()
    print("\n--- Practical 6 Clustering Results ---")
    print(f"Optimal K: {results['Optimal_K']}")
    print(f"Inertia (WCSS): {results['Evaluation']['inertia']}")
    print(f"Silhouette Score: {results['Evaluation']['silhouette_score']}")
    print(f"Davies-Bouldin Index: {results['Evaluation']['davies_bouldin_index']}")
    print("\nDiscovered Cluster Characteristics:")
    for c_id, prof in results["Cluster_Profiles"].items():
        print(f"\nCluster {c_id}: {prof['cluster_name']}")
        print(f"  Cycles: {prof['sample_count']} ({prof['percentage']}%)")
        print(f"  Description: {prof['description']}")
        print(f"  Mean SOH: {prof['means']['soh']}%, Impedance: {prof['means']['internal_impedance']} Ω, Cycle: {prof['means']['cycle_number']}")
