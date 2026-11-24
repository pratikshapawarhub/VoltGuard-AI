"""
VoltGuard AI - Practical 3: Scikit-learn Linear Regression Wrapper
Provides analytical Ordinary Least Squares (OLS) closed-form regression.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, Any, List


class SklearnLinearRegressor:
    """
    Standard Scikit-learn Linear Regression model wrapper.
    """
    def __init__(self, fit_intercept: bool = True):
        self.model = LinearRegression(fit_intercept=fit_intercept)
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'SklearnLinearRegressor':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet.")
        return self.model.predict(X)

    def get_params(self, feature_names: List[str] = None) -> Dict[str, Any]:
        if not self.is_fitted:
            return {}
        coefs = self.model.coef_.tolist()
        intercept = float(self.model.intercept_)
        feat_dict = {}
        if feature_names and len(feature_names) == len(coefs):
            feat_dict = dict(zip(feature_names, [round(c, 4) for c in coefs]))
        return {
            "intercept": round(intercept, 4),
            "coefficients": coefs,
            "feature_coefficients": feat_dict
        }
