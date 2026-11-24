"""
VoltGuard AI - Model Loader & Cache Registry
Singleton loader caching all serialized models, scalers, and metrics in memory.
Ensures zero-latency real-time inference without retraining on requests.
"""

import os
import json
import joblib
from typing import Dict, Any, Optional
from backend.app.config import SAVED_MODELS_DIR


class ModelRegistry:
    """
    In-memory registry of trained models and metadata.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
            cls._instance._is_loaded = False
            cls._instance.models = {}
            cls._instance.metrics = {}
        return cls._instance

    def load_all(self):
        if self._is_loaded:
            return

        print("Loading all serialized models and scalers into memory...")

        # Helper to load joblib safely
        def load_j(filename):
            path = os.path.join(SAVED_MODELS_DIR, filename)
            if os.path.exists(path):
                return joblib.load(path)
            print(f"Warning: Model file {filename} not found.")
            return None

        # Helper to load JSON safely
        def load_m(filename):
            path = os.path.join(SAVED_MODELS_DIR, filename)
            if os.path.exists(path):
                with open(path, "r") as f:
                    return json.load(f)
            return {}

        # 1. Regression Artifacts
        self.models["regression_scaler"] = load_j("regression_scaler.joblib")
        self.models["soh_linear_regression"] = load_j("soh_linear_regression.joblib")
        self.models["soh_manual_gd"] = load_j("soh_manual_gd.joblib")
        self.models["soh_random_forest"] = load_j("soh_random_forest.joblib")

        self.models["rul_linear_regression"] = load_j("rul_linear_regression.joblib")
        self.models["rul_manual_gd"] = load_j("rul_manual_gd.joblib")
        self.models["rul_random_forest"] = load_j("rul_random_forest.joblib")

        # 2. Classification Artifacts
        self.models["classification_svm"] = load_j("classification_svm.joblib")
        self.models["classification_decision_tree"] = load_j("classification_decision_tree.joblib")
        self.models["classification_knn"] = load_j("classification_knn.joblib")
        self.models["classification_naive_bayes"] = load_j("classification_naive_bayes.joblib")

        # 3. Ensemble Artifacts
        self.models["ensemble_stacking"] = load_j("ensemble_stacking.joblib")
        self.models["ensemble_adaboost"] = load_j("ensemble_adaboost.joblib")
        self.models["ensemble_voting"] = load_j("ensemble_voting.joblib")

        # 4. Clustering Artifacts
        self.models["kmeans_model"] = load_j("kmeans_model.joblib")
        self.models["kmeans_scaler"] = load_j("kmeans_scaler.joblib")

        # 5. Metrics Summaries
        self.metrics["regression"] = load_m("regression_metrics.json")
        self.metrics["classification"] = load_m("classification_metrics.json")
        self.metrics["ensemble"] = load_m("ensemble_comparison_metrics.json")
        self.metrics["clustering"] = load_m("clustering_metrics.json")
        self.metrics["search"] = load_m("search_comparison.json")

        self._is_loaded = True
        print("All machine learning models and metric registries successfully cached.")

    def get_model(self, name: str) -> Any:
        if not self._is_loaded:
            self.load_all()
        return self.models.get(name)

    def get_metrics(self, category: str) -> Dict[str, Any]:
        if not self._is_loaded:
            self.load_all()
        return self.metrics.get(category, {})


# Global Registry Instance
registry = ModelRegistry()
