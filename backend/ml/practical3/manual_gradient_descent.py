"""
VoltGuard AI - Practical 3: Manual Gradient Descent Regressor
Implemented from first principles using pure NumPy.

Mathematical Formulation:
- Hypothesis Function:
    y_hat = X * w + b
- Mean Squared Error (MSE) Cost Function:
    J(w, b) = (1 / (2 * m)) * sum((y_hat_i - y_i)^2)
- Gradient with respect to weights:
    dJ/dw = (1 / m) * X.T * (y_hat - y)
- Gradient with respect to bias:
    dJ/db = (1 / m) * sum(y_hat - y)
- Parameter Update Rules:
    w = w - alpha * (dJ/dw)
    b = b - alpha * (dJ/db)
"""

import numpy as np
from typing import List, Tuple, Dict, Any


class ManualGradientDescentRegressor:
    """
    Linear Regression trained using Batch Gradient Descent from scratch.
    """
    def __init__(self, learning_rate: float = 0.01, n_iterations: int = 1500, tolerance: float = 1e-7):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.tolerance = tolerance
        self.weights_: np.ndarray = None
        self.bias_: float = 0.0
        self.cost_history_: List[float] = []

    def compute_cost(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculates the Mean Squared Error cost J(w, b) = 1/(2m) * sum((y_hat - y)^2).
        """
        m = len(y)
        y_hat = np.dot(X, self.weights_) + self.bias_
        cost = (1.0 / (2.0 * m)) * np.sum((y_hat - y) ** 2)
        return float(cost)

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'ManualGradientDescentRegressor':
        """
        Fits the linear model parameters (weights and bias) using gradient descent.
        """
        m, n_features = X.shape
        # 1. Parameter initialization (zeros or small random values)
        self.weights_ = np.zeros(n_features, dtype=np.float64)
        self.bias_ = 0.0
        self.cost_history_ = []

        for iteration in range(self.n_iterations):
            # 2. Prediction calculation (forward hypothesis)
            y_hat = np.dot(X, self.weights_) + self.bias_

            # 3. Error calculation
            error = y_hat - y

            # 4. Gradient calculation
            dw = (1.0 / m) * np.dot(X.T, error)
            db = (1.0 / m) * np.sum(error)

            # 5. Parameter updates
            self.weights_ -= self.learning_rate * dw
            self.bias_ -= self.learning_rate * db

            # 6. Cost computation & convergence tracking
            cost = self.compute_cost(X, y)
            self.cost_history_.append(cost)

            # Early stopping check if loss change is negligible
            if iteration > 0 and abs(self.cost_history_[-2] - cost) < self.tolerance:
                break

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Generates predictions using learned weights and bias: y_hat = X * w + b.
        """
        if self.weights_ is None:
            raise ValueError("Model has not been trained yet. Call fit() first.")
        return np.dot(X, self.weights_) + self.bias_

    def get_params(self) -> Dict[str, Any]:
        """
        Returns model parameters and training diagnostics.
        """
        return {
            "learning_rate": self.learning_rate,
            "n_iterations": self.n_iterations,
            "final_cost": self.cost_history_[-1] if self.cost_history_ else None,
            "iterations_trained": len(self.cost_history_),
            "weights": self.weights_.tolist() if self.weights_ is not None else [],
            "bias": float(self.bias_)
        }
