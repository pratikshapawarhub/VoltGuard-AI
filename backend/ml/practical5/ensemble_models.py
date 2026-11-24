"""
VoltGuard AI - Practical 5: Ensemble Classification Models
Implements all three compulsory ensemble paradigms:
1. Stacking Ensemble (Base: SVM, Decision Tree, KNN; Meta: Logistic Regression with Out-of-Fold CV)
2. AdaBoost Ensemble (Boosting with multi-class SAMME)
3. Hard Voting Ensemble (Majority voting across base estimators)
"""

import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from sklearn.ensemble import StackingClassifier, AdaBoostClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression


class BatteryStackingEnsemble:
    """
    Stacking Classifier combining diverse base estimators (SVM, DT, KNN)
    with a Logistic Regression meta-classifier.
    Uses 5-fold cross-validation to generate out-of-fold probability features,
    strictly preventing data leakage.
    """
    def __init__(self, cv: int = 5, random_state: int = 42):
        self.cv = cv
        self.random_state = random_state

        base_estimators = [
            ('svm', SVC(C=2.0, kernel='rbf', probability=True, random_state=self.random_state)),
            ('dt', DecisionTreeClassifier(max_depth=6, random_state=self.random_state)),
            ('knn', KNeighborsClassifier(n_neighbors=5, weights='distance'))
        ]
        meta_classifier = LogisticRegression(max_iter=1000, random_state=self.random_state)

        self.model = StackingClassifier(
            estimators=base_estimators,
            final_estimator=meta_classifier,
            cv=self.cv,
            stack_method='predict_proba',
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BatteryStackingEnsemble':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Stacking model is not fitted yet.")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Stacking model is not fitted yet.")
        return self.model.predict_proba(X)


class BatteryAdaBoostEnsemble:
    """
    AdaBoost Ensemble using shallow decision trees as weak learners.
    Iteratively focuses on misclassified battery cycles.
    """
    def __init__(self, n_estimators: int = 50, learning_rate: float = 0.8, random_state: int = 42):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.random_state = random_state

        base_tree = DecisionTreeClassifier(max_depth=3, random_state=self.random_state)

        # Scikit-learn 1.3+ uses 'estimator'
        self.model = AdaBoostClassifier(
            estimator=base_tree,
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            random_state=self.random_state
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BatteryAdaBoostEnsemble':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("AdaBoost model is not fitted yet.")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("AdaBoost model is not fitted yet.")
        return self.model.predict_proba(X)


class BatteryVotingEnsemble:
    """
    Hard Voting Ensemble combining predictions from SVM, Decision Tree, and KNN.
    Selects final predicted class via strict majority vote.
    """
    def __init__(self, random_state: int = 42):
        self.random_state = random_state

        estimators = [
            ('svm', SVC(C=2.0, kernel='rbf', probability=True, random_state=self.random_state)),
            ('dt', DecisionTreeClassifier(max_depth=6, random_state=self.random_state)),
            ('knn', KNeighborsClassifier(n_neighbors=5, weights='distance'))
        ]

        self.model = VotingClassifier(
            estimators=estimators,
            voting='hard',
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'BatteryVotingEnsemble':
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Voting model is not fitted yet.")
        return self.model.predict(X)
