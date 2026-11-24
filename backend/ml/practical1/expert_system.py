"""
VoltGuard AI - Practical 1: Rule-Based Expert System
Knowledge-based reasoning engine implementing forward-chaining IF-THEN rules
to evaluate battery health facts, detect operational anomalies, and generate
prioritized maintenance recommendations.
"""

from typing import Dict, Any, List, Optional


class Rule:
    """
    Modular representation of an IF-THEN expert system rule.
    """
    def __init__(
        self,
        rule_id: str,
        name: str,
        description: str,
        severity: str,  # 'INFO', 'WARNING', 'CRITICAL'
        condition_fn,
        recommendation: str,
        action_code: str
    ):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.severity = severity
        self.condition_fn = condition_fn
        self.recommendation = recommendation
        self.action_code = action_code

    def evaluate(self, facts: Dict[str, Any], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Evaluates the rule condition against current battery facts and configuration thresholds.
        """
        try:
            if self.condition_fn(facts, config):
                return {
                    "rule_id": self.rule_id,
                    "name": self.name,
                    "description": self.description,
                    "severity": self.severity,
                    "recommendation": self.recommendation,
                    "action_code": self.action_code
                }
        except Exception:
            pass
        return None


class BatteryExpertSystem:
    """
    Forward-chaining rule-based expert system for intelligent battery monitoring.
    """
    DEFAULT_CONFIG = {
        "temp_warning_threshold": 39.5,      # °C - High operating temperature
        "temp_critical_threshold": 42.0,     # °C - Thermal runaway / severe thermal stress
        "soh_warning_threshold": 80.0,       # % - Entering Degraded health zone
        "soh_critical_threshold": 70.0,      # % - End of Life (EOL) safety boundary
        "impedance_warning_threshold": 0.150,# Ohms - Elevated internal resistance
        "impedance_critical_threshold": 0.170,# Ohms - Extreme internal impedance rise
        "undervoltage_threshold": 2.20,      # V - Severe over-discharge threshold
        "rapid_degradation_drop": 2.0        # % drop over recent cycles
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        self.rules: List[Rule] = []
        self._initialize_rules()

    def _initialize_rules(self):
        """
        Configures the rule knowledge base.
        """
        # Rule 1: Thermal Critical Alert
        self.rules.append(Rule(
            rule_id="RULE_TEMP_CRIT",
            name="Critical Temperature Warning",
            description="Peak cell temperature exceeds critical thermal runaway threshold.",
            severity="CRITICAL",
            condition_fn=lambda f, c: f.get("temperature_max", 0.0) >= c["temp_critical_threshold"],
            recommendation="Immediate cooling intervention required. Suspend rapid charging and inspect thermal dissipation subsystem.",
            action_code="ACT_COOLING_SHUTDOWN"
        ))

        # Rule 2: High Operating Temperature Warning
        self.rules.append(Rule(
            rule_id="RULE_TEMP_WARN",
            name="Elevated Operating Temperature",
            description="Cell temperature exceeds standard operational threshold.",
            severity="WARNING",
            condition_fn=lambda f, c: c["temp_warning_threshold"] <= f.get("temperature_max", 0.0) < c["temp_critical_threshold"],
            recommendation="Active cooling recommended during subsequent discharge. Derate continuous charge current by 20%.",
            action_code="ACT_DERATE_CURRENT"
        ))

        # Rule 3: Critical SOH (End of Life reached)
        self.rules.append(Rule(
            rule_id="RULE_SOH_CRIT",
            name="Critical State of Health (EOL)",
            description="State of Health (SOH) has breached the 70% End-of-Life threshold.",
            severity="CRITICAL",
            condition_fn=lambda f, c: f.get("soh", 100.0) < c["soh_critical_threshold"],
            recommendation="Battery pack has reached end of functional life. Schedule immediate decommissioning and replacement to avoid unexpected failure.",
            action_code="ACT_SCHEDULE_REPLACEMENT"
        ))

        # Rule 4: Degraded SOH Warning
        self.rules.append(Rule(
            rule_id="RULE_SOH_DEGRADED",
            name="Moderate Capacity Degradation",
            description="Battery capacity has degraded below 80% of nominal rating.",
            severity="WARNING",
            condition_fn=lambda f, c: c["soh_critical_threshold"] <= f.get("soh", 100.0) < c["soh_warning_threshold"],
            recommendation="Increase monitoring frequency. Schedule routine cell balance and state-of-charge recalibration.",
            action_code="ACT_SCHEDULE_INSPECTION"
        ))

        # Rule 5: Critical Internal Impedance Rise
        self.rules.append(Rule(
            rule_id="RULE_IMPEDANCE_CRIT",
            name="Severe Internal Impedance Surge",
            description="Internal cell resistance (Re + Rct) is severely elevated, causing large IR voltage drops.",
            severity="CRITICAL",
            condition_fn=lambda f, c: f.get("internal_impedance", 0.0) >= c["impedance_critical_threshold"],
            recommendation="High internal resistance detected. Limit peak discharge currents to prevent deep under-voltage trips.",
            action_code="ACT_LIMIT_LOAD"
        ))

        # Rule 6: Moderate Impedance Warning
        self.rules.append(Rule(
            rule_id="RULE_IMPEDANCE_WARN",
            name="Elevated Internal Impedance",
            description="Internal impedance is notably above fresh cell baseline (0.10 - 0.12 Ω).",
            severity="WARNING",
            condition_fn=lambda f, c: c["impedance_warning_threshold"] <= f.get("internal_impedance", 0.0) < c["impedance_critical_threshold"],
            recommendation="Electrolyte degradation and SEI growth indicated. Plan full electrochemical impedance spectroscopy (EIS) test.",
            action_code="ACT_PLAN_EIS_TEST"
        ))

        # Rule 7: Deep Under-Voltage Risk
        self.rules.append(Rule(
            rule_id="RULE_VOLTAGE_MIN",
            name="Deep Discharge Cutoff Breach",
            description="Minimum terminal voltage dropped below safe cutoff voltage.",
            severity="WARNING",
            condition_fn=lambda f, c: f.get("voltage_min", 3.0) <= c["undervoltage_threshold"],
            recommendation="Deep discharge event detected. Adjust load cutoff voltage threshold to prevent irreversible electrode copper dissolution.",
            action_code="ACT_ADJUST_CUTOFF"
        ))

        # Rule 8: Rapid SOH Decline Gradient
        self.rules.append(Rule(
            rule_id="RULE_RAPID_DROP",
            name="Accelerated Degradation Rate",
            description="SOH drop rate across recent cycling window exceeds typical linear degradation.",
            severity="WARNING",
            condition_fn=lambda f, c: f.get("recent_soh_drop", 0.0) >= c["rapid_degradation_drop"],
            recommendation="Abnormal capacity fading rate detected. Perform internal short-circuit diagnosis and mechanical inspection.",
            action_code="ACT_PHYSICAL_INSPECTION"
        ))

        # Rule 9: Healthy Baseline
        self.rules.append(Rule(
            rule_id="RULE_HEALTHY_STATUS",
            name="Optimal Operating Condition",
            description="All monitored parameters (SOH >= 80%, Temp < 39.5°C, Impedance < 0.150 Ω) within safe bounds.",
            severity="INFO",
            condition_fn=lambda f, c: (
                f.get("soh", 100.0) >= c["soh_warning_threshold"] and
                f.get("temperature_max", 0.0) < c["temp_warning_threshold"] and
                f.get("internal_impedance", 0.0) < c["impedance_warning_threshold"]
            ),
            recommendation="Continue standard operational cycles. No corrective maintenance required.",
            action_code="ACT_CONTINUE_MONITORING"
        ))

    def evaluate(self, facts: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates current facts against the rule base and compiles condition summary.
        """
        triggered_rules = []
        has_critical = False
        has_warning = False

        for rule in self.rules:
            result = rule.evaluate(facts, self.config)
            if result:
                triggered_rules.append(result)
                if result["severity"] == "CRITICAL":
                    has_critical = True
                elif result["severity"] == "WARNING":
                    has_warning = True

        # Synthesize overall condition description
        if has_critical:
            overall_status = "CRITICAL"
            condition_summary = "High-risk battery state detected. Multiple critical thresholds breached. Immediate maintenance intervention required."
        elif has_warning:
            overall_status = "WARNING"
            condition_summary = "Operational warnings present. Cell exhibits early degradation or thermal elevation. Preventive maintenance advised."
        else:
            overall_status = "HEALTHY"
            condition_summary = "Battery is operating within standard parameters. Electro-thermal indicators show normal baseline behavior."

        # Deduplicate recommendations preserving order of severity
        prioritized_recs = []
        for r in sorted(triggered_rules, key=lambda x: 0 if x["severity"] == "CRITICAL" else (1 if x["severity"] == "WARNING" else 2)):
            if r["recommendation"] not in prioritized_recs:
                prioritized_recs.append(r["recommendation"])

        return {
            "overall_status": overall_status,
            "condition_summary": condition_summary,
            "rules_evaluated_count": len(self.rules),
            "triggered_rules_count": len(triggered_rules),
            "triggered_rules": triggered_rules,
            "recommendations": prioritized_recs,
            "input_facts": facts,
            "disclaimer": "Academic demonstration expert system rules. These project-configured thresholds do not replace certified safety BMS cutoffs."
        }
