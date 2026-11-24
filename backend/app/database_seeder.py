"""
VoltGuard AI - Database Seeder
Seeds initial benchmark battery assets, operational alerts, and maintenance tasks
from the NASA PCoE battery dataset if the database is unpopulated.
"""

from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from backend.app.models.battery_asset import BatteryAsset
from backend.app.models.alert import AlertRecord
from backend.app.models.maintenance_task import MaintenanceTask
from backend.app.database import SessionLocal


def seed_database_if_empty():
    db: Session = SessionLocal()
    try:
        # Check if assets already exist
        existing_assets = db.query(BatteryAsset).count()
        if existing_assets == 0:
            now = datetime.now(timezone.utc)
            
            # Benchmark Batteries from NASA Aging Experiments
            assets = [
                BatteryAsset(
                    battery_id="B0005",
                    name="NASA 18650 Cell 05 (Ames Test Bed)",
                    chemistry="LiCoO2 / Graphite",
                    nominal_capacity=2.0,
                    nominal_voltage=3.7,
                    installation_date="2023-08-01",
                    status="ACTIVE",
                    cycle_count=168,
                    current_soh=65.5,
                    current_rul=0.0,
                    health_condition="Critical",
                    operating_regime="Degraded / High-Impedance EOL",
                    location="Bay A - Thermal Chamber 1",
                    notes="Reached EOL boundary (1.31 Ahr). Scheduled for post-mortem EIS analysis.",
                    created_at=now - timedelta(days=60),
                    updated_at=now
                ),
                BatteryAsset(
                    battery_id="B0006",
                    name="NASA 18650 Cell 06 (Accelerated Stress)",
                    chemistry="LiCoO2 / Graphite",
                    nominal_capacity=2.0,
                    nominal_voltage=3.7,
                    installation_date="2023-08-01",
                    status="MAINTENANCE",
                    cycle_count=168,
                    current_soh=58.7,
                    current_rul=0.0,
                    health_condition="Critical",
                    operating_regime="Degraded / High-Impedance EOL",
                    location="Bay A - Thermal Chamber 2",
                    notes="Elevated impedance growth observed. Auxiliary cooling throttled.",
                    created_at=now - timedelta(days=60),
                    updated_at=now
                ),
                BatteryAsset(
                    battery_id="B0007",
                    name="NASA 18650 Cell 07 (Cyclic Baseline)",
                    chemistry="LiCoO2 / Graphite",
                    nominal_capacity=2.0,
                    nominal_voltage=3.7,
                    installation_date="2023-08-15",
                    status="ACTIVE",
                    cycle_count=168,
                    current_soh=72.8,
                    current_rul=14.0,
                    health_condition="Degraded",
                    operating_regime="Intermediate / Active Aging",
                    location="Bay B - Bench 1",
                    notes="Capacity fade tracking standard degradation kinetics.",
                    created_at=now - timedelta(days=45),
                    updated_at=now
                ),
                BatteryAsset(
                    battery_id="B0018",
                    name="NASA 18650 Cell 18 (Cross-Validation Test Cell)",
                    chemistry="LiCoO2 / Graphite",
                    nominal_capacity=2.0,
                    nominal_voltage=3.7,
                    installation_date="2023-09-01",
                    status="ACTIVE",
                    cycle_count=132,
                    current_soh=67.8,
                    current_rul=0.0,
                    health_condition="Critical",
                    operating_regime="Degraded / High-Impedance EOL",
                    location="Bay B - Bench 2",
                    notes="Unseen physical test cell used for independent model evaluation.",
                    created_at=now - timedelta(days=30),
                    updated_at=now
                ),
                BatteryAsset(
                    battery_id="EV-PACK-01",
                    name="Commercial Fleet Module Alpha",
                    chemistry="NMC 811 / Silicon-C",
                    nominal_capacity=60.0,
                    nominal_voltage=48.0,
                    installation_date="2024-02-10",
                    status="ACTIVE",
                    cycle_count=24,
                    current_soh=98.2,
                    current_rul=185.0,
                    health_condition="Healthy",
                    operating_regime="Fresh Baseline",
                    location="Vehicle Fleet Depot - Van 04",
                    notes="Nominal operation. Telemetry synced hourly.",
                    created_at=now - timedelta(days=10),
                    updated_at=now
                )
            ]
            db.add_all(assets)
            db.commit()

        # Seed initial alerts if empty
        if db.query(AlertRecord).count() == 0:
            now = datetime.now(timezone.utc)
            initial_alerts = [
                AlertRecord(
                    battery_id="B0006",
                    alert_type="CRITICAL_SOH",
                    severity="CRITICAL",
                    title="End of Life Boundary Violation",
                    description="Cell SOH at 58.7%, below the 70.0% safety boundary. Severe active lithium loss.",
                    action_code="REPLACE_CELL_IMMEDIATE",
                    recommendation="Decommission cell immediately; schedule physical cell replacement.",
                    status="ACTIVE",
                    created_at=now - timedelta(hours=3)
                ),
                AlertRecord(
                    battery_id="B0006",
                    alert_type="SEVERE_IMPEDANCE",
                    severity="CRITICAL",
                    title="Impedance Growth Exceeds Limit",
                    description="Internal impedance Re + Rct reached 0.178 Ohms (> 0.170 Ohm safety threshold).",
                    action_code="ELECTROLYTE_RECONDITION_OR_REPLACE",
                    recommendation="Electrolyte reconditioning or cell retirement required.",
                    status="ACTIVE",
                    created_at=now - timedelta(hours=5)
                ),
                AlertRecord(
                    battery_id="B0007",
                    alert_type="DEGRADED_CAPACITY",
                    severity="WARNING",
                    title="Entering Degraded Degradation Regime",
                    description="Capacity dropped to 72.8% SOH. High-rate fast charging should be restricted.",
                    action_code="FLAG_PREVENTIVE_MAINTENANCE",
                    recommendation="Flag for preventive maintenance; restrict high-rate discharge.",
                    status="ACKNOWLEDGED",
                    created_at=now - timedelta(days=1)
                )
            ]
            db.add_all(initial_alerts)
            db.commit()

        # Seed initial maintenance tasks if empty
        if db.query(MaintenanceTask).count() == 0:
            now = datetime.now(timezone.utc)
            tasks = [
                MaintenanceTask(
                    task_id="TASK-B0006-01",
                    battery_id="B0006",
                    title="Emergency Cell Decommission & Replacement",
                    priority="CRITICAL",
                    status="SCHEDULED",
                    technician_name="Alice (Senior Specialist)",
                    is_senior_required=True,
                    scheduled_slot="SLOT_0900",
                    estimated_duration_hours=1.5,
                    estimated_cost=130.0,
                    search_algorithm_used="A* Search",
                    servicing_path="CRITICAL_FAULT -> ISOLATION -> PRELIMINARY_SCAN -> CELL_REPLACEMENT -> CALIBRATION_TEST -> CERTIFIED_OPERATIONAL",
                    notes="A* optimal cost path generated. Priority early morning slot assigned.",
                    created_at=now - timedelta(hours=2)
                ),
                MaintenanceTask(
                    task_id="TASK-B0018-02",
                    battery_id="B0018",
                    title="Comprehensive EIS Diagnostic & Overhaul",
                    priority="CRITICAL",
                    status="SCHEDULED",
                    technician_name="Alice (Senior Specialist)",
                    is_senior_required=True,
                    scheduled_slot="SLOT_1100",
                    estimated_duration_hours=1.0,
                    estimated_cost=130.0,
                    search_algorithm_used="A* Search",
                    servicing_path="CRITICAL_FAULT -> ISOLATION -> PRELIMINARY_SCAN -> CELL_REBALANCING -> CALIBRATION_TEST -> CERTIFIED_OPERATIONAL",
                    notes="CSP conflict-free assignment verified.",
                    created_at=now - timedelta(hours=1)
                ),
                MaintenanceTask(
                    task_id="TASK-B0007-03",
                    battery_id="B0007",
                    title="Cell Rebalancing & Capacity Verification",
                    priority="MODERATE",
                    status="IN_PROGRESS",
                    technician_name="Bob (Junior Tech)",
                    is_senior_required=False,
                    scheduled_slot="SLOT_1400",
                    estimated_duration_hours=1.0,
                    estimated_cost=95.0,
                    search_algorithm_used="A* Search",
                    servicing_path="PRELIMINARY_SCAN -> CELL_REBALANCING -> CALIBRATION_TEST -> CERTIFIED_OPERATIONAL",
                    notes="Routine preventive servicing.",
                    created_at=now - timedelta(days=1)
                )
            ]
            db.add_all(tasks)
            db.commit()

    except Exception as e:
        db.rollback()
        print(f"Warning: Failed to seed database: {e}")
    finally:
        db.close()
