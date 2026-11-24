"""
VoltGuard AI - Practical 1 Unit & Validation Tests
Tests PEAS descriptors schema and forward-chaining expert system rule evaluation.
"""

import pytest
from backend.ml.practical1.peas import get_peas_description
from backend.ml.practical1.expert_system import BatteryExpertSystem


def test_peas_descriptors_structure():
    peas = get_peas_description()
    assert "agent_name" in peas
    assert "dimensions" in peas

    dims = peas["dimensions"]
    assert "Performance_Measure" in dims
    assert "Environment" in dims
    assert "Actuators" in dims
    assert "Sensors" in dims

    assert len(dims["Performance_Measure"]["items"]) >= 4
    assert len(dims["Environment"]["items"]) >= 4
    assert len(dims["Actuators"]["items"]) >= 4
    assert len(dims["Sensors"]["items"]) >= 5


def test_expert_system_healthy_evaluation():
    expert = BatteryExpertSystem()
    healthy_facts = {
        "soh": 94.5,
        "temperature_max": 34.0,
        "internal_impedance": 0.115,
        "voltage_min": 2.50,
        "recent_soh_drop": 0.2
    }
    result = expert.evaluate(healthy_facts)

    assert result["overall_status"] == "HEALTHY"
    assert result["triggered_rules_count"] >= 1
    triggered_ids = [r["rule_id"] for r in result["triggered_rules"]]
    assert "RULE_HEALTHY_STATUS" in triggered_ids
    assert "RULE_SOH_CRIT" not in triggered_ids
    assert "RULE_TEMP_CRIT" not in triggered_ids


def test_expert_system_critical_temperature():
    expert = BatteryExpertSystem()
    hot_facts = {
        "soh": 85.0,
        "temperature_max": 43.5,  # Exceeds 42.0°C critical threshold
        "internal_impedance": 0.125,
        "voltage_min": 2.45
    }
    result = expert.evaluate(hot_facts)

    assert result["overall_status"] == "CRITICAL"
    triggered_ids = [r["rule_id"] for r in result["triggered_rules"]]
    assert "RULE_TEMP_CRIT" in triggered_ids
    assert any("cooling" in rec.lower() for rec in result["recommendations"])


def test_expert_system_critical_soh_and_impedance():
    expert = BatteryExpertSystem()
    degraded_facts = {
        "soh": 66.0,               # Below 70% EOL
        "temperature_max": 37.0,
        "internal_impedance": 0.175,# Above 0.170 critical
        "voltage_min": 2.05,        # Deep discharge under-voltage
        "recent_soh_drop": 2.5
    }
    result = expert.evaluate(degraded_facts)

    assert result["overall_status"] == "CRITICAL"
    triggered_ids = [r["rule_id"] for r in result["triggered_rules"]]
    assert "RULE_SOH_CRIT" in triggered_ids
    assert "RULE_IMPEDANCE_CRIT" in triggered_ids
    assert "RULE_VOLTAGE_MIN" in triggered_ids
    assert "RULE_RAPID_DROP" in triggered_ids
    assert any("replacement" in rec.lower() for rec in result["recommendations"])


def test_expert_system_configurable_thresholds():
    # Configure custom conservative temp threshold at 35.0°C
    custom_expert = BatteryExpertSystem(config={"temp_critical_threshold": 35.0})
    facts = {
        "soh": 90.0,
        "temperature_max": 36.0,
        "internal_impedance": 0.110
    }
    result = custom_expert.evaluate(facts)
    triggered_ids = [r["rule_id"] for r in result["triggered_rules"]]
    assert "RULE_TEMP_CRIT" in triggered_ids
