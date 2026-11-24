"""
VoltGuard AI - Practical 4: Classification Training & Evaluation Pipeline
Trains and benchmarks:
1. Support Vector Machine (SVM)
2. Decision Tree Classifier
3. K-Nearest Neighbors (KNN)
4. Gaussian Naive Bayes
predicting 4 battery condition categories (Healthy, Moderate, Degraded, Critical).
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

from backend.ml.preprocessing.data_loader import (
    get_train_test_split,
    HEALTH_CATEGORIES,
    CATEGORY_TO_LABEL,
    LABEL_TO_CATEGORY,
    FEATURE_COLUMNS
)
from backend.ml.practical4.classifiers import (
    BatterySVMClassifier,
    BatteryDecisionTreeClassifier,
    BatteryKNNClassifier,
    BatteryNaiveBayesClassifier
)

MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")
FIGURES_DIR = os.path.join(BASE_DIR, "docs", "figures")


def evaluate_classifier(model, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    prec_macro = float(precision_score(y_test, y_pred, average='macro', zero_division=0))
    prec_weighted = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average='macro', zero_division=0))
    rec_weighted = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average='macro', zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))
    
    try:
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
        "Log_Loss": round(loss, 4) if loss is not None else None,
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


def train_and_evaluate_classification() -> dict:
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    print("Loading preprocessed dataset for classification...")
    split = get_train_test_split(train_batteries=['B0005', 'B0006', 'B0007'], test_batteries=['B0018'])

    X_train = split['X_train']
    X_test = split['X_test']
    y_train = split['y_cat_train']
    y_test = split['y_cat_test']

    # 1. Train SVM Classifier
    print("Training Support Vector Machine (SVM)...")
    svm_model = BatterySVMClassifier(C=2.0, kernel='rbf', gamma='scale', random_state=42)
    svm_model.fit(X_train, y_train)
    svm_metrics = evaluate_classifier(svm_model, X_test, y_test)

    # 2. Train Decision Tree Classifier
    print("Training Decision Tree Classifier...")
    dt_model = BatteryDecisionTreeClassifier(criterion='gini', max_depth=6, random_state=42)
    dt_model.fit(X_train, y_train)
    dt_metrics = evaluate_classifier(dt_model, X_test, y_test)

    # 3. Train KNN Classifier
    print("Training K-Nearest Neighbors (KNN)...")
    knn_model = BatteryKNNClassifier(n_neighbors=5, weights='distance')
    knn_model.fit(X_train, y_train)
    knn_metrics = evaluate_classifier(knn_model, X_test, y_test)

    # 4. Train Gaussian Naive Bayes
    print("Training Gaussian Naive Bayes...")
    nb_model = BatteryNaiveBayesClassifier()
    nb_model.fit(X_train, y_train)
    nb_metrics = evaluate_classifier(nb_model, X_test, y_test)

    # Save trained models
    joblib.dump(svm_model, os.path.join(MODELS_DIR, "classification_svm.joblib"))
    joblib.dump(dt_model, os.path.join(MODELS_DIR, "classification_decision_tree.joblib"))
    joblib.dump(knn_model, os.path.join(MODELS_DIR, "classification_knn.joblib"))
    joblib.dump(nb_model, os.path.join(MODELS_DIR, "classification_naive_bayes.joblib"))

    results = {
        "Support_Vector_Machine": svm_metrics,
        "Decision_Tree": dt_metrics,
        "K_Nearest_Neighbors": knn_metrics,
        "Naive_Bayes": nb_metrics
    }

    metrics_file = os.path.join(MODELS_DIR, "classification_metrics.json")
    with open(metrics_file, "w") as f:
        json.dump(results, f, indent=2)

    # ==========================================
    # Generate Visualizations for Report
    # ==========================================
    plt.style.use('dark_background')

    # 1. Confusion Matrix 2x2 Subplot Grid
    fig, axes = plt.subplots(2, 2, figsize=(11, 9), dpi=150)
    model_names = [
        ("Support Vector Machine (SVM)", svm_metrics),
        ("Decision Tree", dt_metrics),
        ("K-Nearest Neighbors (KNN)", knn_metrics),
        ("Gaussian Naive Bayes", nb_metrics)
    ]

    for idx, (name, metrics) in enumerate(model_names):
        ax = axes[idx // 2, idx % 2]
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
        ax.set_title(f"{name}\nAccuracy: {metrics['Accuracy']*100:.1f}%, F1: {metrics['F1_Macro']:.3f}", fontsize=11, fontweight='bold', pad=8)
        ax.set_xlabel("Predicted Condition", fontsize=9)
        ax.set_ylabel("Actual Condition", fontsize=9)

    plt.suptitle("Battery Condition Classification: Confusion Matrices on Test Cell B0018", fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "confusion_matrices_all_classifiers.png"))
    plt.close()

    # 2. Overall Performance Comparison Chart
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    models = ["SVM", "Decision Tree", "KNN", "Naive Bayes"]
    accs = [svm_metrics['Accuracy'], dt_metrics['Accuracy'], knn_metrics['Accuracy'], nb_metrics['Accuracy']]
    f1s = [svm_metrics['F1_Macro'], dt_metrics['F1_Macro'], knn_metrics['F1_Macro'], nb_metrics['F1_Macro']]

    x = np.arange(len(models))
    w = 0.35
    b1 = ax.bar(x - w/2, accs, width=w, label="Accuracy", color="#38bdf8", edgecolor="#334155")
    b2 = ax.bar(x + w/2, f1s, width=w, label="Macro F1-Score", color="#10b981", edgecolor="#334155")

    for bar in b1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.015, f"{h*100:.1f}%", ha='center', va='bottom', fontsize=9)
    for bar in b2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.015, f"{h:.3f}", ha='center', va='bottom', fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.set_title("Classification Models Performance Benchmark (Test Cell B0018)", fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel("Score", fontsize=11)
    ax.legend(loc="upper right", framealpha=0.4)
    ax.grid(axis='y', linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "classification_models_comparison.png"))
    plt.close()

    # 3. Per-Class F1-Score Comparison
    fig, ax = plt.subplots(figsize=(11, 5), dpi=150)
    categories = HEALTH_CATEGORIES
    x = np.arange(len(categories))
    w = 0.18

    colors = ['#38bdf8', '#a855f7', '#fbbf24', '#f43f5e']
    for i, (name, metrics) in enumerate(model_names):
        f1_vals = [metrics['Per_Class_Metrics'][cat]['F1_Score'] for cat in categories]
        ax.bar(x + (i - 1.5) * w, f1_vals, width=w, label=name.split(' (')[0], color=colors[i], edgecolor="#334155")

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.set_title("Per-Category F1-Score Comparison across Classifiers", fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel("F1-Score", fontsize=11)
    ax.legend(loc="upper right", framealpha=0.4)
    ax.grid(axis='y', linestyle=":", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "per_class_f1_comparison.png"))
    plt.close()

    print("Classification training, evaluation, and plotting complete.")
    return results


if __name__ == "__main__":
    results = train_and_evaluate_classification()
    print("\n--- Practical 4 Classification Results on Test Cell B0018 ---")
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        print(f"  Accuracy:      {metrics['Accuracy']*100:.2f}%")
        print(f"  Macro F1:      {metrics['F1_Macro']:.4f}")
        print(f"  Weighted F1:   {metrics['F1_Weighted']:.4f}")
        print(f"  Log Loss:      {metrics['Log_Loss']}")
