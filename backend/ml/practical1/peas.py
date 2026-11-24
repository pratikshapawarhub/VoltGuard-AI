"""
VoltGuard AI - Practical 1: PEAS Descriptors
Formal specification of the Intelligent Battery Monitoring Agent using the PEAS framework:
- Performance Measure
- Environment
- Actuators
- Sensors
"""

from typing import Dict, Any, List


def get_peas_description() -> Dict[str, Any]:
    """
    Returns the formal PEAS specification for the VoltGuard AI Intelligent Battery Monitoring Agent.
    """
    return {
        "agent_name": "VoltGuard Intelligent Battery Monitoring Agent",
        "agent_type": "Utility-Based Hybrid Prognostic & Expert Agent",
        "dimensions": {
            "Performance_Measure": {
                "title": "Performance Measure (P)",
                "description": "Criteria by which the agent's monitoring, diagnostic, and predictive success is evaluated.",
                "items": [
                    {
                        "metric": "SOH Prediction Accuracy",
                        "target": "R² > 0.90, MAE < 2.0%",
                        "description": "Accurate estimation of continuous battery capacity degradation."
                    },
                    {
                        "metric": "RUL Prognosis Horizon",
                        "target": "MAE < 20 cycles",
                        "description": "Timely and reliable remaining useful life forecasting before EOL threshold."
                    },
                    {
                        "metric": "Degradation Classification F1-Score",
                        "target": "Macro F1 > 0.60 across 4 classes",
                        "description": "Correct classification of cell state into Healthy, Moderate, Degraded, Critical."
                    },
                    {
                        "metric": "False Alarm Minimization",
                        "target": "False Positive Rate < 5%",
                        "description": "Prevention of spurious maintenance dispatches on normal cell fluctuations."
                    },
                    {
                        "metric": "Actionable Maintenance Recommendations",
                        "target": "100% rule-backed explanations",
                        "description": "Clear audit trails linking triggered IF-THEN rules to specific service actions."
                    }
                ]
            },
            "Environment": {
                "title": "Environment (E)",
                "description": "The operational context and electro-chemical system in which the agent operates.",
                "items": [
                    {
                        "element": "Lithium-Ion Electrochemical Cells",
                        "details": "Commercial 18650 LiCoO2 / graphite cells with nominal capacity of 2.0 Ahr."
                    },
                    {
                        "element": "Operational Charging & Discharging Cycles",
                        "details": "CC/CV charging profiles, constant current (2.0A) discharge loads."
                    },
                    {
                        "element": "Thermal Environment",
                        "details": "Ambient operating temperatures (~24°C nominal) with cell self-heating up to 43°C."
                    },
                    {
                        "element": "Physical Aging Dynamics",
                        "details": "Solid Electrolyte Interphase (SEI) growth, lithium plating, active material loss, internal resistance rise."
                    },
                    {
                        "element": "Operational Constraints",
                        "details": "Maintenance scheduling slots, technician availability limits, and fleet usage demands."
                    }
                ]
            },
            "Actuators": {
                "title": "Actuators (A)",
                "description": "Mechanisms through which the agent takes action, issues directives, and influences the environment.",
                "items": [
                    {
                        "actuator": "Visual UI Alert System",
                        "action": "Display real-time banners (INFO, WARNING, CRITICAL) on dashboard."
                    },
                    {
                        "actuator": "Maintenance Recommendation Engine",
                        "action": "Generate structured, rule-backed service checklists and corrective work orders."
                    },
                    {
                        "actuator": "Automated Maintenance Planner Trigger",
                        "action": "Invoke graph search (A*) and CSP solvers to schedule optimal technician service slots."
                    },
                    {
                        "actuator": "State of Health (SOH) Status Publisher",
                        "action": "Update health scores, remaining cycles, and clustering segments in database."
                    },
                    {
                        "actuator": "Operational Derating Advice",
                        "action": "Recommend charge current reduction or thermal throttling when stress thresholds are exceeded."
                    }
                ]
            },
            "Sensors": {
                "title": "Sensors (S)",
                "description": "Telemetry instruments and data ingestion interfaces providing physical observations.",
                "items": [
                    {
                        "sensor": "Voltage Transducers",
                        "signal": "Terminal Voltage (V)",
                        "range": "2.0V - 4.25V DC",
                        "features": "voltage_mean, voltage_max, voltage_min, voltage_std"
                    },
                    {
                        "sensor": "Current Hall Sensors",
                        "signal": "Pack Current (A)",
                        "range": "-2.0A to +2.0A",
                        "features": "current_mean, current_std"
                    },
                    {
                        "sensor": "Thermocouples",
                        "signal": "Cell Surface Temperature (°C)",
                        "range": "20°C - 50°C",
                        "features": "temperature_mean, temperature_max, temperature_min"
                    },
                    {
                        "sensor": "Coulomb Counting Accumulators",
                        "signal": "Discharge Capacity (Ahr)",
                        "range": "1.0 Ahr - 2.1 Ahr",
                        "features": "discharge_capacity, energy_throughput"
                    },
                    {
                        "sensor": "Electrochemical Impedance Spectroscopy (EIS)",
                        "signal": "Internal Impedance (Re + Rct, Ω)",
                        "range": "0.05Ω - 0.25Ω",
                        "features": "internal_impedance"
                    },
                    {
                        "sensor": "Cycle Sequence Counter & Timer",
                        "signal": "Operational Timestamps & Durations (s)",
                        "range": "0 - 15,000s",
                        "features": "charge_duration, discharge_duration, cycle_number"
                    }
                ]
            }
        }
    }


if __name__ == "__main__":
    import json
    print(json.dumps(get_peas_description(), indent=2))
