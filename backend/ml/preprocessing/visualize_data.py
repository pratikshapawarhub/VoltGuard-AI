"""
VoltGuard AI - Dataset Visualization & EDA Generator
Generates academic report figures from the cleaned NASA battery dataset.
Saves high-resolution plots to docs/figures/.
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from backend.ml.preprocessing.data_loader import load_cleaned_dataset, CLEANED_CSV_PATH

FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "docs", "figures")

def generate_eda_plots():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    df = load_cleaned_dataset()

    # Set dark aesthetic matching VoltGuard theme
    plt.style.use('dark_background')
    palette = {'B0005': '#38bdf8', 'B0006': '#f43f5e', 'B0007': '#10b981', 'B0018': '#fbbf24'}

    # 1. SOH Degradation vs Cycle
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    for b_id, grp in df.groupby('battery_id'):
        ax.plot(grp['cycle_number'], grp['soh'], label=f"Battery {b_id}", color=palette.get(b_id, '#38bdf8'), linewidth=2)
    ax.axhline(y=90, color='#10b981', linestyle='--', alpha=0.7, label='Healthy Threshold (90%)')
    ax.axhline(y=80, color='#38bdf8', linestyle='--', alpha=0.7, label='Moderate Threshold (80%)')
    ax.axhline(y=70, color='#f43f5e', linestyle='--', alpha=0.7, label='EOL Threshold (70%)')
    ax.set_title("NASA Li-ion Battery SOH Degradation Trajectory", fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel("Discharge Cycle Number", fontsize=11)
    ax.set_ylabel("State of Health (SOH %)", fontsize=11)
    ax.legend(loc='lower left', framealpha=0.3)
    ax.grid(True, linestyle=':', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "soh_degradation_curves.png"))
    plt.close()

    # 2. Health Category Distribution
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    cat_counts = df['health_category'].value_counts()[['Healthy', 'Moderate', 'Degraded', 'Critical']]
    colors = ['#10b981', '#38bdf8', '#fbbf24', '#f43f5e']
    bars = ax.bar(cat_counts.index, cat_counts.values, color=colors, width=0.55, edgecolor='#334155', linewidth=1.2)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 3, f"{h} ({h/len(df)*100:.1f}%)", ha='center', va='bottom', fontsize=10, color='white')
    ax.set_title("NASA Dataset Health Category Distribution (636 Cycles)", fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel("Cycle Count", fontsize=11)
    ax.set_ylim(0, max(cat_counts.values) + 30)
    ax.grid(axis='y', linestyle=':', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "health_category_distribution.png"))
    plt.close()

    # 3. Feature Correlation Matrix
    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    corr_cols = ['cycle_number', 'voltage_mean', 'voltage_min', 'temperature_max', 'charge_duration', 'discharge_duration', 'internal_impedance', 'soh', 'rul']
    corr = df[corr_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, cbar=True, linewidths=0.5, linecolor='#0f172a')
    ax.set_title("Feature Correlation Matrix (Pearson r)", fontsize=14, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "correlation_heatmap.png"))
    plt.close()

    # 4. Internal Impedance Growth vs Cycle
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    for b_id, grp in df.groupby('battery_id'):
        ax.plot(grp['cycle_number'], grp['internal_impedance'], label=f"Battery {b_id}", color=palette.get(b_id, '#38bdf8'), linewidth=1.8)
    ax.set_title("Internal Impedance Growth across Aging Cycles", fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel("Discharge Cycle Number", fontsize=11)
    ax.set_ylabel("Impedance (Ohms, Re + Rct)", fontsize=11)
    ax.legend(loc='upper left', framealpha=0.3)
    ax.grid(True, linestyle=':', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "impedance_growth_curve.png"))
    plt.close()

    print(f"Generated 4 EDA plots in {FIGURES_DIR}")

if __name__ == "__main__":
    generate_eda_plots()
