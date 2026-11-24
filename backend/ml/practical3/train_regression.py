"""
VoltGuard AI - Practical 3: Regression Training & Evaluation Pipeline
Trains and compares:
1. Manual Gradient Descent
2. Scikit-learn Linear Regression
3. Random Forest Regressor
for predicting Battery SOH (%) and RUL (Cycles).
Saves trained models, evaluation metrics, and comparison plots.
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
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Ensure project root is in path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.ml.preprocessing.data_loader import get_train_test_split, FEATURE_COLUMNS
from backend.ml.practical3.manual_gradient_descent import ManualGradientDescentRegressor
from backend.ml.practical3.linear_regression import SklearnLinearRegressor
from backend.ml.practical3.random_forest_regression import BatteryRandomForestRegressor

MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")
FIGURES_DIR = os.path.join(BASE_DIR, "docs", "figures")


def calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true, y_pred))
    return {
        "MAE": round(mae, 4),
        "MSE": round(mse, 4),
        "RMSE": round(rmse, 4),
        "R2_Score": round(r2, 4)
    }


def train_and_evaluate_regression() -> dict:
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    print("Loading preprocessed NASA battery dataset with grouped split...")
    split = get_train_test_split(train_batteries=['B0005', 'B0006', 'B0007'], test_batteries=['B0018'])

    X_train = split['X_train']
    X_test = split['X_test']
    y_soh_train = split['y_soh_train']
    y_soh_test = split['y_soh_test']
    y_rul_train = split['y_rul_train']
    y_rul_test = split['y_rul_test']
    scaler = split['scaler']
    test_df = split['test_df']

    # Save feature scaler
    joblib.dump(scaler, os.path.join(MODELS_DIR, "regression_scaler.joblib"))

    # ==========================================
    # 1. State of Health (SOH) Models Training
    # ==========================================
    print("\n--- Training SOH Regression Models ---")
    
    # A. Manual Gradient Descent for SOH
    # Using alpha=0.015, 2000 iterations for smooth convergence
    soh_manual_gd = ManualGradientDescentRegressor(learning_rate=0.015, n_iterations=2000)
    soh_manual_gd.fit(X_train, y_soh_train)
    soh_manual_gd_pred = soh_manual_gd.predict(X_test)
    soh_manual_gd_metrics = calculate_regression_metrics(y_soh_test, soh_manual_gd_pred)

    # B. Scikit-learn Linear Regression for SOH
    soh_sklearn_lr = SklearnLinearRegressor()
    soh_sklearn_lr.fit(X_train, y_soh_train)
    soh_sklearn_lr_pred = soh_sklearn_lr.predict(X_test)
    soh_sklearn_lr_metrics = calculate_regression_metrics(y_soh_test, soh_sklearn_lr_pred)

    # C. Random Forest Regressor for SOH
    soh_rf = BatteryRandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    soh_rf.fit(X_train, y_soh_train)
    soh_rf_pred = soh_rf.predict(X_test)
    soh_rf_metrics = calculate_regression_metrics(y_soh_test, soh_rf_pred)

    # ==========================================
    # 2. Remaining Useful Life (RUL) Models Training
    # ==========================================
    print("\n--- Training RUL Regression Models ---")

    # A. Manual Gradient Descent for RUL
    rul_manual_gd = ManualGradientDescentRegressor(learning_rate=0.01, n_iterations=2500)
    rul_manual_gd.fit(X_train, y_rul_train)
    rul_manual_gd_pred = rul_manual_gd.predict(X_test)
    rul_manual_gd_metrics = calculate_regression_metrics(y_rul_test, rul_manual_gd_pred)

    # B. Scikit-learn Linear Regression for RUL
    rul_sklearn_lr = SklearnLinearRegressor()
    rul_sklearn_lr.fit(X_train, y_rul_train)
    rul_sklearn_lr_pred = rul_sklearn_lr.predict(X_test)
    rul_sklearn_lr_metrics = calculate_regression_metrics(y_rul_test, rul_sklearn_lr_pred)

    # C. Random Forest Regressor for RUL
    rul_rf = BatteryRandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rul_rf.fit(X_train, y_rul_train)
    rul_rf_pred = rul_rf.predict(X_test)
    rul_rf_metrics = calculate_regression_metrics(y_rul_test, rul_rf_pred)

    # ==========================================
    # Save Model Artifacts
    # ==========================================
    joblib.dump(soh_manual_gd, os.path.join(MODELS_DIR, "soh_manual_gd.joblib"))
    joblib.dump(soh_sklearn_lr, os.path.join(MODELS_DIR, "soh_linear_regression.joblib"))
    joblib.dump(soh_rf, os.path.join(MODELS_DIR, "soh_random_forest.joblib"))

    joblib.dump(rul_manual_gd, os.path.join(MODELS_DIR, "rul_manual_gd.joblib"))
    joblib.dump(rul_sklearn_lr, os.path.join(MODELS_DIR, "rul_linear_regression.joblib"))
    joblib.dump(rul_rf, os.path.join(MODELS_DIR, "rul_random_forest.joblib"))

    metrics_summary = {
        "SOH_Prediction": {
            "Manual_Gradient_Descent": soh_manual_gd_metrics,
            "Sklearn_Linear_Regression": soh_sklearn_lr_metrics,
            "Random_Forest_Regressor": soh_rf_metrics
        },
        "RUL_Prediction": {
            "Manual_Gradient_Descent": rul_manual_gd_metrics,
            "Sklearn_Linear_Regression": rul_sklearn_lr_metrics,
            "Random_Forest_Regressor": rul_rf_metrics
        },
        "Feature_Importance_SOH": soh_rf.get_feature_importances(FEATURE_COLUMNS),
        "Feature_Importance_RUL": rul_rf.get_feature_importances(FEATURE_COLUMNS)
    }

    metrics_file = os.path.join(MODELS_DIR, "regression_metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(metrics_summary, f, indent=2)

    # ==========================================
    # Generate Visualizations for Report
    # ==========================================
    plt.style.use('dark_background')
    cycles = test_df['cycle_number'].values

    # 1. Actual vs Predicted SOH for Test Cell B0018
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.plot(cycles, y_soh_test, label="Actual Ground Truth (B0018)", color="#38bdf8", linewidth=2.5)
    ax.plot(cycles, soh_manual_gd_pred, label=f"Manual GD (R²: {soh_manual_gd_metrics['R2_Score']:.3f})", color="#fbbf24", linestyle="--", linewidth=1.8)
    ax.plot(cycles, soh_sklearn_lr_pred, label=f"Sklearn Linear Reg (R²: {soh_sklearn_lr_metrics['R2_Score']:.3f})", color="#a855f7", linestyle=":", linewidth=1.8)
    ax.plot(cycles, soh_rf_pred, label=f"Random Forest (R²: {soh_rf_metrics['R2_Score']:.3f})", color="#10b981", linewidth=2.0)
    ax.set_title("Test Cell B0018: Actual vs Predicted State of Health (SOH %)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Cycle Number", fontsize=11)
    ax.set_ylabel("SOH (%)", fontsize=11)
    ax.legend(loc="lower left", framealpha=0.4)
    ax.grid(True, linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "actual_vs_predicted_soh.png"))
    plt.close()

    # 2. Actual vs Predicted RUL for Test Cell B0018
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.plot(cycles, y_rul_test, label="Actual Ground Truth RUL", color="#38bdf8", linewidth=2.5)
    ax.plot(cycles, rul_manual_gd_pred, label=f"Manual GD (MAE: {rul_manual_gd_metrics['MAE']:.1f})", color="#fbbf24", linestyle="--", linewidth=1.8)
    ax.plot(cycles, rul_sklearn_lr_pred, label=f"Sklearn Linear Reg (MAE: {rul_sklearn_lr_metrics['MAE']:.1f})", color="#a855f7", linestyle=":", linewidth=1.8)
    ax.plot(cycles, rul_rf_pred, label=f"Random Forest (MAE: {rul_rf_metrics['MAE']:.1f})", color="#10b981", linewidth=2.0)
    ax.set_title("Test Cell B0018: Actual vs Predicted Remaining Useful Life (RUL)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Cycle Number", fontsize=11)
    ax.set_ylabel("Remaining Useful Cycles", fontsize=11)
    ax.legend(loc="upper right", framealpha=0.4)
    ax.grid(True, linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "actual_vs_predicted_rul.png"))
    plt.close()

    # 3. Manual Gradient Descent Loss Convergence Curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=150)
    ax1.plot(soh_manual_gd.cost_history_, color="#38bdf8", linewidth=2)
    ax1.set_title("SOH Cost J(w,b) Convergence", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Iteration", fontsize=10)
    ax1.set_ylabel("Mean Squared Error Cost", fontsize=10)
    ax1.grid(True, linestyle=":", alpha=0.3)

    ax2.plot(rul_manual_gd.cost_history_, color="#fbbf24", linewidth=2)
    ax2.set_title("RUL Cost J(w,b) Convergence", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Iteration", fontsize=10)
    ax2.set_ylabel("Mean Squared Error Cost", fontsize=10)
    ax2.grid(True, linestyle=":", alpha=0.3)

    plt.suptitle("Manual Gradient Descent Training Convergence History", fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "gradient_descent_loss_curve.png"))
    plt.close()

    # 4. Regression Models Performance Comparison Bar Chart
    models = ["Manual GD", "Sklearn LR", "Random Forest"]
    soh_r2s = [soh_manual_gd_metrics['R2_Score'], soh_sklearn_lr_metrics['R2_Score'], soh_rf_metrics['R2_Score']]
    soh_rmses = [soh_manual_gd_metrics['RMSE'], soh_sklearn_lr_metrics['RMSE'], soh_rf_metrics['RMSE']]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=150)
    x = np.arange(len(models))
    w = 0.45

    bars1 = ax1.bar(x, soh_r2s, width=w, color=['#fbbf24', '#a855f7', '#10b981'], edgecolor='#334155')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models)
    ax1.set_title("SOH Model Comparison: R² Score (Higher is Better)", fontsize=11, fontweight='bold')
    ax1.set_ylabel("R² Score")
    for b in bars1:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2., h + 0.02, f"{h:.3f}", ha='center', va='bottom', fontsize=9)
    ax1.grid(axis='y', linestyle=":", alpha=0.3)

    bars2 = ax2.bar(x, soh_rmses, width=w, color=['#fbbf24', '#a855f7', '#10b981'], edgecolor='#334155')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models)
    ax2.set_title("SOH Model Comparison: RMSE (Lower is Better)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("RMSE (%)")
    for b in bars2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2., h + 0.08, f"{h:.2f}%", ha='center', va='bottom', fontsize=9)
    ax2.grid(axis='y', linestyle=":", alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "regression_models_comparison.png"))
    plt.close()

    print("\nRegression training and evaluation complete.")
    return metrics_summary


if __name__ == "__main__":
    results = train_and_evaluate_regression()
    print("\n--- Model Evaluation Results on Unseen Test Cell B0018 ---")
    print(json.dumps(results, indent=2))
