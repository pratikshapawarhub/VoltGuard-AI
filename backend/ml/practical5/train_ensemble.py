"""
VoltGuard AI - Practical 5: Ensemble Training, Evaluation & Benchmarking Pipeline
Trains:
1. Stacking Ensemble
2. AdaBoost Ensemble
3. Hard Voting Ensemble
And benchmarks them side-by-side against the 4 base classifiers (SVM, DT, KNN, Naive Bayes).
Saves models, metrics summary, and comparison visualizations.
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
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    log_loss,
    confusion_matrix,
    classification_report
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.ml.preprocessing.data_loader import get_train_test_split, HEALTH_CATEGORIES
from backend.ml.practical5.ensemble_models import (
    BatteryStackingEnsemble,
    BatteryAdaBoostEnsemble,
    BatteryVotingEnsemble
)

MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")
FIGURES_DIR = os.path.join(BASE_DIR, "docs", "figures")


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray, has_proba: bool = True) -> dict:
    y_pred = model.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    prec_macro = float(precision_score(y_test, y_pred, average='macro', zero_division=0))
    prec_weighted = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average='macro', zero_division=0))
    rec_weighted = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average='macro', zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))

    loss = None
    if has_proba:
        try:
            y_prob = model.predict_proba(X_test)
            loss = float(log_loss(y_test, y_prob, labels=[0, 1, 2, 3]))
        except Exception:
            loss = None

    cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2, 3]).tolist()
    report = classification_report(y_test, y_pred, target_names=HEALTH_CATEGORIES, output_dict=True, zero_division=0)

    return {
        "Accuracy": round(acc, 4),
        "Precision_Macro": round(prec_macro, 4),
        "Precision_Weighted": round(prec_weighted, 4),
        "Recall_Macro": round(rec_macro, 4),
        "Recall_Weighted": round(rec_weighted, 4),
        "F1_Macro": round(f1_macro, 4),
        "F1_Weighted": round(f1_weighted, 4),
        "Log_Loss": round(loss, 4) if loss is not None else "N/A (Hard Voting)",
        "Confusion_Matrix": cm,
        "Per_Class_Metrics": {
            cat: {
                "Precision": round(report[cat]['precision'], 4),
                "Recall": round(report[cat]['recall'], 4),
                "F1_Score": round(report[cat]['f1-score'], 4),
                "Support": int(report[cat]['support'])
            } for cat in HEALTH_CATEGORIES if cat in report
        }
    }


def train_and_evaluate_ensembles() -> dict:
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    print("Loading preprocessed dataset for ensemble training...")
    split = get_train_test_split(train_batteries=['B0005', 'B0006', 'B0007'], test_batteries=['B0018'])

    X_train = split['X_train']
    X_test = split['X_test']
    y_train = split['y_cat_train']
    y_test = split['y_cat_test']

    # 1. Train Stacking Ensemble
    print("Training Stacking Ensemble (Base: SVM, DT, KNN | Meta: Logistic Regression with 5-Fold OOF)...")
    stacking_model = BatteryStackingEnsemble(cv=5, random_state=42)
    stacking_model.fit(X_train, y_train)
    stacking_metrics = evaluate_model(stacking_model, X_test, y_test, has_proba=True)

    # 2. Train AdaBoost Ensemble
    print("Training AdaBoost Ensemble...")
    adaboost_model = BatteryAdaBoostEnsemble(n_estimators=50, learning_rate=0.8, random_state=42)
    adaboost_model.fit(X_train, y_train)
    adaboost_metrics = evaluate_model(adaboost_model, X_test, y_test, has_proba=True)

    # 3. Train Hard Voting Ensemble
    print("Training Hard Voting Ensemble (Majority vote: SVM, DT, KNN)...")
    voting_model = BatteryVotingEnsemble(random_state=42)
    voting_model.fit(X_train, y_train)
    voting_metrics = evaluate_model(voting_model, X_test, y_test, has_proba=False)

    # Save trained ensemble models
    joblib.dump(stacking_model, os.path.join(MODELS_DIR, "ensemble_stacking.joblib"))
    joblib.dump(adaboost_model, os.path.join(MODELS_DIR, "ensemble_adaboost.joblib"))
    joblib.dump(voting_model, os.path.join(MODELS_DIR, "ensemble_voting.joblib"))

    # Load Practical 4 base metrics for side-by-side 7-model comparison
    base_metrics_path = os.path.join(MODELS_DIR, "classification_metrics.json")
    base_metrics = {}
    if os.path.exists(base_metrics_path):
        with open(base_metrics_path, "r") as f:
            base_metrics = json.load(f)

    all_models_comparison = {
        "Base_Models": {
            "SVM": base_metrics.get("Support_Vector_Machine", {}),
            "Decision_Tree": base_metrics.get("Decision_Tree", {}),
            "KNN": base_metrics.get("K_Nearest_Neighbors", {}),
            "Naive_Bayes": base_metrics.get("Naive_Bayes", {})
        },
        "Ensemble_Models": {
            "Stacking_Ensemble": stacking_metrics,
            "AdaBoost_Ensemble": adaboost_metrics,
            "Hard_Voting_Ensemble": voting_metrics
        }
    }

    # Identify best performing model across all 7
    candidates = [
        ("Decision Tree", base_metrics.get("Decision_Tree", {}).get("Accuracy", 0), base_metrics.get("Decision_Tree", {}).get("F1_Macro", 0)),
        ("SVM", base_metrics.get("Support_Vector_Machine", {}).get("Accuracy", 0), base_metrics.get("Support_Vector_Machine", {}).get("F1_Macro", 0)),
        ("KNN", base_metrics.get("K_Nearest_Neighbors", {}).get("Accuracy", 0), base_metrics.get("K_Nearest_Neighbors", {}).get("F1_Macro", 0)),
        ("Naive Bayes", base_metrics.get("Naive_Bayes", {}).get("Accuracy", 0), base_metrics.get("Naive_Bayes", {}).get("F1_Macro", 0)),
        ("Stacking Ensemble", stacking_metrics['Accuracy'], stacking_metrics['F1_Macro']),
        ("AdaBoost Ensemble", adaboost_metrics['Accuracy'], adaboost_metrics['F1_Macro']),
        ("Hard Voting Ensemble", voting_metrics['Accuracy'], voting_metrics['F1_Macro'])
    ]
    best_by_acc = max(candidates, key=lambda x: x[1])
    best_by_f1 = max(candidates, key=lambda x: x[2])

    all_models_comparison["Best_Model_By_Accuracy"] = {"name": best_by_acc[0], "accuracy": best_by_acc[1]}
    all_models_comparison["Best_Model_By_F1"] = {"name": best_by_f1[0], "f1_macro": best_by_f1[2]}

    metrics_file = os.path.join(MODELS_DIR, "ensemble_comparison_metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(all_models_comparison, f, indent=2)

    # ==========================================
    # Generate Visualizations for Report
    # ==========================================
    plt.style.use('dark_background')

    # 1. 7-Model Benchmark Bar Chart
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=150)
    model_labels = [c[0] for c in candidates]
    acc_scores = [c[1] for c in candidates]
    f1_scores = [c[2] for c in candidates]

    x = np.arange(len(model_labels))
    w = 0.35

    colors_acc = ['#38bdf8' if 'Ensemble' not in m else '#06b6d4' for m in model_labels]
    colors_f1 = ['#10b981' if 'Ensemble' not in m else '#34d399' for m in model_labels]

    b1 = ax.bar(x - w/2, acc_scores, width=w, label="Accuracy", color=colors_acc, edgecolor="#1e293b")
    b2 = ax.bar(x + w/2, f1_scores, width=w, label="Macro F1-Score", color=colors_f1, edgecolor="#1e293b")

    for bar in b1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.015, f"{h*100:.1f}%", ha='center', va='bottom', fontsize=8.5)
    for bar in b2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.015, f"{h:.3f}", ha='center', va='bottom', fontsize=8.5)

    ax.set_xticks(x)
    ax.set_xticklabels(model_labels, rotation=15, ha='right', fontsize=9.5)
    ax.set_ylim(0, 1.15)
    ax.set_title("Comprehensive Model Comparison: 4 Base Classifiers vs 3 Ensemble Methods (Test Cell B0018)", fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel("Score", fontsize=11)
    ax.legend(loc="upper right", framealpha=0.4)
    ax.grid(axis='y', linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "ensemble_vs_base_comparison.png"))
    plt.close()

    # 2. Ensemble Confusion Matrices (3 Subplots)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=150)
    ensembles_info = [
        ("Stacking Ensemble", stacking_metrics),
        ("AdaBoost Ensemble", adaboost_metrics),
        ("Hard Voting Ensemble", voting_metrics)
    ]

    for idx, (name, metrics) in enumerate(ensembles_info):
        ax = axes[idx]
        cm = np.array(metrics["Confusion_Matrix"])
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=HEALTH_CATEGORIES,
            yticklabels=HEALTH_CATEGORIES,
            cbar=False,
            ax=ax,
            linewidths=0.5,
            linecolor='#1e293b'
        )
        ax.set_title(f"{name}\nAcc: {metrics['Accuracy']*100:.1f}%, F1: {metrics['F1_Macro']:.3f}", fontsize=11, fontweight='bold', pad=8)
        ax.set_xlabel("Predicted Condition", fontsize=9)
        ax.set_ylabel("Actual Condition", fontsize=9)

    plt.suptitle("Ensemble Methods: Confusion Matrices on Unseen Cell B0018", fontsize=13, fontweight='bold', y=1.03)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "ensemble_confusion_matrices.png"))
    plt.close()

    print("Ensemble training, evaluation, benchmarking, and figures completed.")
    return all_models_comparison


if __name__ == "__main__":
    results = train_and_evaluate_ensembles()
    print("\n--- Practical 5 Ensemble Results ---")
    for ens_name, metrics in results["Ensemble_Models"].items():
        print(f"\n{ens_name}:")
        print(f"  Accuracy:      {metrics['Accuracy']*100:.2f}%")
        print(f"  Macro F1:      {metrics['F1_Macro']:.4f}")
        print(f"  Weighted F1:   {metrics['F1_Weighted']:.4f}")
        print(f"  Log Loss:      {metrics['Log_Loss']}")
    print(f"\nBest Model by Accuracy: {results['Best_Model_By_Accuracy']['name']} ({results['Best_Model_By_Accuracy']['accuracy']*100:.2f}%)")
    print(f"Best Model by Macro F1: {results['Best_Model_By_F1']['name']} ({results['Best_Model_By_F1']['f1_macro']:.4f})")
