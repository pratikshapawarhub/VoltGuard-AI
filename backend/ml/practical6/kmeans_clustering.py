"""
VoltGuard AI - Practical 6: Intelligent Battery Usage Segmentation
Implements unsupervised K-Means Clustering on multi-dimensional electro-thermal features:
- State of Health (SOH)
- Discharge Capacity (Ahr)
- Peak Discharge Temperature (°C)
- Internal Impedance (Ohms)
- Cycle Count

Features are discovered purely unsupervised without predefined labels.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score

CLUSTERING_FEATURES = [
    'soh',
    'discharge_capacity',
    'temperature_max',
    'internal_impedance',
    'cycle_number'
]


class BatteryKMeansClusterer:
    """
    Unsupervised K-Means clustering engine with automated Elbow,
    Silhouette, and Davies-Bouldin evaluation.
    """
    def __init__(self, n_clusters: int = 3, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.model = KMeans(
            n_clusters=self.n_clusters,
            init='k-means++',
            n_init=10,
            max_iter=300,
            random_state=self.random_state
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        self.cluster_profiles: Dict[int, Dict[str, Any]] = {}

    @staticmethod
    def compute_elbow_and_metrics(X_scaled: np.ndarray, k_range: range = range(2, 9)) -> Dict[str, List[Any]]:
        """
        Computes WCSS (Inertia), Silhouette Score, and Davies-Bouldin Index across a range of K.
        """
        wcss_list = []
        silhouette_list = []
        db_list = []
        k_values = list(k_range)

        for k in k_values:
            km = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, random_state=42)
            labels = km.fit_predict(X_scaled)

            wcss_list.append(float(km.inertia_))
            silhouette_list.append(float(silhouette_score(X_scaled, labels)))
            db_list.append(float(davies_bouldin_score(X_scaled, labels)))

        return {
            "k_values": k_values,
            "wcss": [round(w, 2) for w in wcss_list],
            "silhouette_scores": [round(s, 4) for s in silhouette_list],
            "davies_bouldin_scores": [round(d, 4) for d in db_list]
        }

    def fit(self, X: np.ndarray) -> 'BatteryKMeansClusterer':
        """
        Fits scaler and K-Means clustering model.
        """
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Clusterer is not fitted yet.")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)

    def evaluate(self, X: np.ndarray) -> Dict[str, float]:
        if not self.is_fitted:
            raise ValueError("Clusterer is not fitted yet.")
        X_scaled = self.scaler.transform(X)
        labels = self.model.labels_

        return {
            "inertia": round(float(self.model.inertia_), 2),
            "silhouette_score": round(float(silhouette_score(X_scaled, labels)), 4),
            "davies_bouldin_index": round(float(davies_bouldin_score(X_scaled, labels)), 4)
        }

    def characterize_clusters(self, df_raw: pd.DataFrame, labels: np.ndarray) -> Dict[int, Dict[str, Any]]:
        """
        Computes mean values and operational names for each discovered cluster.
        """
        df_copy = df_raw.copy()
        df_copy['cluster'] = labels
        total_samples = len(df_copy)

        profiles = {}
        for c in range(self.n_clusters):
            c_df = df_copy[df_copy['cluster'] == c]
            count = len(c_df)
            mean_soh = float(c_df['soh'].mean())
            mean_cap = float(c_df['discharge_capacity'].mean())
            mean_temp = float(c_df['temperature_max'].mean())
            mean_imp = float(c_df['internal_impedance'].mean())
            mean_cycle = float(c_df['cycle_number'].mean())

            # Assign intuitive industrial cluster name based on SOH and Impedance
            if mean_soh >= 88.0:
                name = "Fresh / High-Capacity Baseline"
                desc = "Minimal electrochemical wear, low internal resistance, high energy retention."
            elif mean_soh >= 76.0:
                name = "Intermediate Aging / Thermal Active"
                desc = "Moderate capacity decline, steady impedance growth, active operational heating."
            else:
                name = "Degraded / High-Impedance EOL"
                desc = "Severe active material loss, elevated internal impedance, imminent replacement threshold."

            profiles[c] = {
                "cluster_id": c,
                "cluster_name": name,
                "description": desc,
                "sample_count": count,
                "percentage": round(count / total_samples * 100.0, 1),
                "means": {
                    "soh": round(mean_soh, 2),
                    "discharge_capacity": round(mean_cap, 4),
                    "temperature_max": round(mean_temp, 2),
                    "internal_impedance": round(mean_imp, 4),
                    "cycle_number": round(mean_cycle, 1)
                }
            }

        self.cluster_profiles = profiles
        return profiles
