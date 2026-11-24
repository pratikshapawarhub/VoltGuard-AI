"""
VoltGuard AI - Practical 3: Random Forest Regressor
Ensemble tree-based regression model for non-linear degradation tracking.
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from typing import Dict, Any, List


class BatteryRandomForestRegressor:
    """
    Random Forest Regressor wrapper for SOH & RUL prediction.
    """
    def __init__(self, n_estimators: int = 100, max_depth: int = 12, random_state: int = 42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            random_state=self.random_state,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BatteryRandomForestRegressor':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        return self.model.predict(X)

    def get_feature_importances(self, feature_names: List[str] = None) -> Dict[str, float]:
        if not self.is_fitted:
            return {}
        importances = self.model.feature_importances_
        if feature_names and len(feature_names) == len(importances):
            return dict(sorted(
                zip(feature_names, [round(float(v), 4) for v in importances]),
                key=lambda item: item[1],
                reverse=True
            ))
        return {f"feature_{i}": round(float(v), 4) for i, v in enumerate(importances)}
