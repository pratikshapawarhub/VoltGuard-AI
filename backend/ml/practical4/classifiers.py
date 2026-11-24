"""
VoltGuard AI - Practical 4: Battery Condition Classification Models
Implements all four compulsory classification algorithms:
1. Support Vector Machine (SVM / SVC)
2. Decision Tree Classifier
3. K-Nearest Neighbors (KNN)
4. Gaussian Naive Bayes

Predicts battery condition categories:
0: Healthy (SOH >= 90%)
1: Moderate (80% <= SOH < 90%)
2: Degraded (70% <= SOH < 80%)
3: Critical (SOH < 70%)
"""

import numpy as np
from typing import Dict, Any, List, Optional
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB


class BatterySVMClassifier:
    """
    Support Vector Machine Classifier with RBF kernel and Platt probability calibration.
    """
    def __init__(self, C: float = 1.0, kernel: str = 'rbf', gamma: str = 'scale', random_state: int = 42):
        self.C = C
        self.kernel = kernel
        self.gamma = gamma
        self.random_state = random_state
        self.model = SVC(
            C=self.C,
            kernel=self.kernel,
            gamma=self.gamma,
            probability=True,
            random_state=self.random_state
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BatterySVMClassifier':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict_proba(X)


class BatteryDecisionTreeClassifier:
    """
    Decision Tree Classifier with pruning to prevent overfitting.
    """
    def __init__(self, criterion: str = 'gini', max_depth: int = 6, min_samples_split: int = 4, random_state: int = 42):
        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.model = DecisionTreeClassifier(
            criterion=self.criterion,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            random_state=self.random_state
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BatteryDecisionTreeClassifier':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict_proba(X)

    def get_feature_importances(self, feature_names: List[str] = None) -> Dict[str, float]:
        if not self.is_fitted:
            return {}
        importances = self.model.feature_importances_
        if feature_names and len(feature_names) == len(importances):
            return dict(sorted(
                zip(feature_names, [round(float(v), 4) for v in importances]),
                key=lambda x: x[1],
                reverse=True
            ))
        return {f"feat_{i}": round(float(v), 4) for i, v in enumerate(importances)}


class BatteryKNNClassifier:
    """
    K-Nearest Neighbors Classifier using inverse-distance weighting.
    """
    def __init__(self, n_neighbors: int = 5, weights: str = 'distance', metric: str = 'euclidean'):
        self.n_neighbors = n_neighbors
        self.weights = weights
        self.metric = metric
        self.model = KNeighborsClassifier(
            n_neighbors=self.n_neighbors,
            weights=self.weights,
            metric=self.metric
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BatteryKNNClassifier':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict_proba(X)


class BatteryNaiveBayesClassifier:
    """
    Gaussian Naive Bayes Classifier assuming normal feature likelihood distributions.
    """
    def __init__(self, var_smoothing: float = 1e-9):
        self.var_smoothing = var_smoothing
        self.model = GaussianNB(var_smoothing=self.var_smoothing)
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BatteryNaiveBayesClassifier':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model is not fitted yet.")
        return self.model.predict_proba(X)
