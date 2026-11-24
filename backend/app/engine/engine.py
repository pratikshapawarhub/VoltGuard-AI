"""
VoltGuard AI - Practical 7: Integrated Predictive Maintenance Engine
Coordinates and integrates all models and algorithms from Practical 1 to Practical 6:
1. Regression (SOH & RUL)
2. Classification (Condition assessment)
3. Ensemble Learning (Stacking, AdaBoost, Voting)
4. Unsupervised Clustering (Operating regime assignment)
5. Rule-Based Expert System (Explainable rules & alerts)
6. Search Algorithm (A* optimal maintenance path)
7. SQLite History Persistence
"""

import json
from datetime import datetime, timezone
import numpy as np
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.app.schemas.battery import (
    BatteryMeasurementInput,
    SOHPredictionResponse,
    RULPredictionResponse,
    ClassificationResponse,
    EnsembleResponse,
    ClusteringResponse,
    ExpertSystemResponse,
    SearchMaintenanceResponse,
    IntegratedPredictionResponse
)
from backend.app.engine.model_loader import registry
from backend.app.models.history import PredictionHistory
from backend.app.models.battery_asset import BatteryAsset
from backend.app.models.alert import AlertRecord
from backend.ml.preprocessing.data_loader import (
    FEATURE_COLUMNS,
    LABEL_TO_CATEGORY,
    HEALTH_CATEGORIES
)
from backend.ml.practical1.expert_system import BatteryExpertSystem
from backend.ml.practical2.informed_search import run_a_star
from backend.ml.practical6.kmeans_clustering import CLUSTERING_FEATURES


class IntegratedPredictiveEngine:
    """
    Unified multi-model diagnostic and prognostic engine.
    """
    def __init__(self):
        self.expert_system = BatteryExpertSystem()

    def process_battery_sample(
        self,
        measurement: BatteryMeasurementInput,
        db: Optional[Session] = None
    ) -> IntegratedPredictionResponse:
        """
        Executes end-to-end multi-model inference for a single battery cycle measurement.
        """
        # Ensure models are loaded in memory
        registry.load_all()

        # 1. Prepare and scale feature vector for regression & classification
        raw_feat_vector = np.array([[
            measurement.cycle_number,
            measurement.voltage_mean,
            measurement.voltage_max,
            measurement.voltage_min,
            measurement.voltage_std,
            measurement.current_mean,
            measurement.current_std,
            measurement.temperature_mean,
            measurement.temperature_max,
            measurement.temperature_min,
            measurement.charge_duration,
            measurement.discharge_duration,
            measurement.internal_impedance
        ]], dtype=np.float64)

        scaler = registry.get_model("regression_scaler")
        scaled_feat = scaler.transform(raw_feat_vector)

        # 2. Practical 3: Regression Predictions (SOH & RUL)
        # SOH models
        soh_lr = registry.get_model("soh_linear_regression")
        soh_gd = registry.get_model("soh_manual_gd")
        soh_rf = registry.get_model("soh_random_forest")

        soh_val_lr = float(soh_lr.predict(scaled_feat)[0])
        soh_val_gd = float(soh_gd.predict(scaled_feat)[0])
        soh_val_rf = float(soh_rf.predict(scaled_feat)[0])

        # Recommended SOH uses best validated model (Linear Regression R² = 0.9968)
        # Clamped to physical bounds (40% to 110%)
        rec_soh = max(40.0, min(110.0, soh_val_lr))

        soh_resp = SOHPredictionResponse(
            soh_sklearn_lr=round(soh_val_lr, 2),
            soh_manual_gd=round(soh_val_gd, 2),
            soh_random_forest=round(soh_val_rf, 2),
            recommended_soh=round(rec_soh, 2)
        )

        # RUL models
        rul_gd = registry.get_model("rul_manual_gd")
        rul_lr = registry.get_model("rul_linear_regression")
        rul_rf = registry.get_model("rul_random_forest")

        rul_val_gd = max(0.0, float(rul_gd.predict(scaled_feat)[0]))
        rul_val_lr = max(0.0, float(rul_lr.predict(scaled_feat)[0]))
        rul_val_rf = max(0.0, float(rul_rf.predict(scaled_feat)[0]))

        # Recommended RUL uses best validated model (Manual Gradient Descent MAE 18.37)
        rec_rul = round(rul_val_gd, 1)

        rul_resp = RULPredictionResponse(
            rul_manual_gd=round(rul_val_gd, 1),
            rul_sklearn_lr=round(rul_val_lr, 1),
            rul_random_forest=round(rul_val_rf, 1),
            recommended_rul=rec_rul
        )

        # 3. Practical 4: Classification
        dt_model = registry.get_model("classification_decision_tree")
        cat_label = int(dt_model.predict(scaled_feat)[0])
        cat_name = LABEL_TO_CATEGORY.get(cat_label, "Moderate")
        cat_probs = dt_model.predict_proba(scaled_feat)[0]
        prob_dict = {cat: round(float(cat_probs[i]), 4) for i, cat in enumerate(HEALTH_CATEGORIES)}

        clf_resp = ClassificationResponse(
            predicted_category=cat_name,
            predicted_label=cat_label,
            probabilities=prob_dict,
            model_used="Decision Tree Classifier"
        )

        # 4. Practical 5: Ensemble Learning
        ens_stacking = registry.get_model("ensemble_stacking")
        ens_adaboost = registry.get_model("ensemble_adaboost")
        ens_voting = registry.get_model("ensemble_voting")

        stack_label = int(ens_stacking.predict(scaled_feat)[0])
        ada_label = int(ens_adaboost.predict(scaled_feat)[0])
        vote_label = int(ens_voting.predict(scaled_feat)[0])

        stack_probs = ens_stacking.predict_proba(scaled_feat)[0]
        stack_prob_dict = {cat: round(float(stack_probs[i]), 4) for i, cat in enumerate(HEALTH_CATEGORIES)}

        ens_resp = EnsembleResponse(
            stacking_category=LABEL_TO_CATEGORY.get(stack_label, "Moderate"),
            adaboost_category=LABEL_TO_CATEGORY.get(ada_label, "Moderate"),
            voting_category=LABEL_TO_CATEGORY.get(vote_label, "Moderate"),
            consensus_category=LABEL_TO_CATEGORY.get(stack_label, "Moderate"),
            stacking_probabilities=stack_prob_dict
        )

        # 5. Practical 6: Clustering
        # Estimated capacity from SOH
        est_capacity = (rec_soh / 100.0) * 2.0
        clustering_raw = np.array([[
            rec_soh,
            est_capacity,
            measurement.temperature_max,
            measurement.internal_impedance,
            measurement.cycle_number
        ]], dtype=np.float64)

        kmeans_scaler = registry.get_model("kmeans_scaler")
        kmeans_model = registry.get_model("kmeans_model")
        scaled_cluster_feat = kmeans_scaler.transform(clustering_raw)
        cluster_id = int(kmeans_model.predict(scaled_cluster_feat)[0])

        # Cluster metadata
        cluster_meta = registry.get_metrics("clustering").get("Cluster_Profiles", {}).get(str(cluster_id), {})
        cluster_name = cluster_meta.get("cluster_name", f"Cluster {cluster_id}")
        cluster_desc = cluster_meta.get("description", "Learned battery usage cluster")
        cluster_means = cluster_meta.get("means", {})

        cluster_resp = ClusteringResponse(
            cluster_id=cluster_id,
            cluster_name=cluster_name,
            description=cluster_desc,
            cluster_means=cluster_means
        )

        # 6. Practical 1: Expert System Evaluation
        expert_facts = {
            "soh": rec_soh,
            "temperature_max": measurement.temperature_max,
            "internal_impedance": measurement.internal_impedance,
            "voltage_min": measurement.voltage_min,
            "voltage_max": measurement.voltage_max,
            "recent_soh_drop": measurement.recent_soh_drop or 0.0
        }
        expert_eval = self.expert_system.evaluate(expert_facts)

        expert_resp = ExpertSystemResponse(
            overall_status=expert_eval["overall_status"],
            condition_summary=expert_eval["condition_summary"],
            rules_evaluated_count=expert_eval["rules_evaluated_count"],
            triggered_rules_count=expert_eval["triggered_rules_count"],
            triggered_rules=expert_eval["triggered_rules"],
            recommendations=expert_eval["recommendations"],
            disclaimer=expert_eval["disclaimer"]
        )

        # 7. Practical 2: A* Maintenance Trajectory Planning
        start_state = "CRITICAL_FAULT" if (rec_soh < 70.0 or expert_eval["overall_status"] == "CRITICAL") else "PRELIMINARY_SCAN"
        a_star_plan = run_a_star(start_state=start_state, goal_state="CERTIFIED_OPERATIONAL")

        search_resp = SearchMaintenanceResponse(
            algorithm=a_star_plan["algorithm"],
            path=a_star_plan["path"],
            total_cost=a_star_plan["total_cost"],
            steps=a_star_plan["steps"],
            nodes_explored=a_star_plan["nodes_explored"],
            execution_time_ms=a_star_plan["execution_time_ms"],
            optimality=a_star_plan.get("is_optimal_cost", True) and "Cost-Optimal (A* Minimum Cost)" or "Step-Optimal"
        )

        # 8. Record transaction in SQLite history & sync with Asset and Alert ledgers
        db_record_id = None
        now_utc = datetime.now(timezone.utc)
        if db is not None:
            try:
                history_entry = PredictionHistory(
                    battery_id=measurement.battery_id,
                    cycle_number=measurement.cycle_number,
                    voltage_mean=measurement.voltage_mean,
                    voltage_min=measurement.voltage_min,
                    temperature_max=measurement.temperature_max,
                    internal_impedance=measurement.internal_impedance,
                    discharge_duration=measurement.discharge_duration,
                    predicted_soh=rec_soh,
                    predicted_rul=rec_rul,
                    predicted_condition=cat_name,
                    ensemble_condition=ens_resp.consensus_category,
                    cluster_id=cluster_id,
                    cluster_name=cluster_name,
                    expert_status=expert_eval["overall_status"],
                    triggered_rules_json=json.dumps(expert_eval["triggered_rules"]),
                    maintenance_path=" -> ".join(a_star_plan["path"])
                )
                db.add(history_entry)

                # Sync state with BatteryAsset entity if registered
                asset = db.query(BatteryAsset).filter(BatteryAsset.battery_id == measurement.battery_id).first()
                if asset:
                    asset.current_soh = rec_soh
                    asset.current_rul = rec_rul
                    asset.health_condition = cat_name
                    asset.operating_regime = cluster_name
                    if measurement.cycle_number > asset.cycle_count:
                        asset.cycle_count = measurement.cycle_number
                    if expert_eval["overall_status"] == "CRITICAL":
                        asset.status = "MAINTENANCE"
                    asset.updated_at = now_utc

                # Triggered alert persistence with deduplication
                for rule in expert_eval["triggered_rules"]:
                    if rule.get("severity") in ["CRITICAL", "WARNING"]:
                        existing_alert = db.query(AlertRecord).filter(
                            AlertRecord.battery_id == measurement.battery_id,
                            AlertRecord.action_code == rule.get("action_code"),
                            AlertRecord.status == "ACTIVE"
                        ).first()
                        if not existing_alert:
                            new_alert = AlertRecord(
                                battery_id=measurement.battery_id,
                                alert_type=rule.get("rule_id", "ANOMALY"),
                                severity=rule.get("severity", "WARNING"),
                                title=rule.get("name", "Operational Anomaly"),
                                description=rule.get("description", "Condition anomaly detected."),
                                action_code=rule.get("action_code", "INSPECT"),
                                recommendation=rule.get("recommendation", "Review battery telemetry."),
                                status="ACTIVE",
                                created_at=now_utc
                            )
                            db.add(new_alert)

                db.commit()
                db.refresh(history_entry)
                db_record_id = history_entry.id
            except Exception as e:
                db.rollback()
                print(f"Warning: Failed to save prediction history or sync assets: {e}")

        return IntegratedPredictionResponse(
            battery_id=measurement.battery_id,
            cycle_number=measurement.cycle_number,
            timestamp=now_utc.isoformat(),
            soh_prediction=soh_resp,
            rul_prediction=rul_resp,
            condition_classification=clf_resp,
            ensemble_classification=ens_resp,
            usage_clustering=cluster_resp,
            expert_system=expert_resp,
            optimal_maintenance_plan=search_resp,
            database_record_id=db_record_id
        )


# Global Integrated Engine Instance
integrated_engine = IntegratedPredictiveEngine()
