"""
VoltGuard AI - Practical 2: Local Search (Hill Climbing)
Optimizes battery maintenance allocation to minimize fleet degradation risk.
"""

import time
import random
from typing import Dict, List, Any, Tuple


class BatteryMaintenanceHillClimbing:
    """
    Hill Climbing local search optimizer for fleet maintenance dispatch.
    Minimizes aggregate fleet failure risk.
    """
    def __init__(self, max_iterations: int = 500, random_seed: int = 42):
        self.max_iterations = max_iterations
        self.random_seed = random_seed
        random.seed(self.random_seed)

    @staticmethod
    def calculate_fleet_risk(schedule: List[Dict[str, Any]]) -> float:
        """
        Objective / Cost Function: Lower is better.
        Risk = Sum( (100 - SOH) * (priority_weight) * (scheduled_slot_index + 1) )
               + Thermal_penalty + Overload_penalty
        """
        total_risk = 0.0
        for slot_idx, battery in enumerate(schedule):
            soh = battery.get("soh", 80.0)
            priority = battery.get("priority", 1.0)  # 3.0 for Critical, 2.0 for Moderate, 1.0 for Healthy
            temp = battery.get("temp", 35.0)

            # High-priority / degraded batteries scheduled late accumulate massive delay risk
            delay_penalty = (100.0 - soh) * priority * (slot_idx + 1) * 1.5
            thermal_penalty = max(0.0, temp - 38.0) * 15.0

            total_risk += delay_penalty + thermal_penalty

        return round(total_risk, 2)

    def optimize_schedule(self, batteries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes steepest-ascent hill climbing (minimizing risk objective).
        Generates pairwise swap neighbors.
        """
        start_time = time.perf_counter()
        current_schedule = list(batteries)
        current_cost = self.calculate_fleet_risk(current_schedule)
        cost_history = [current_cost]

        nodes_explored = 0
        n = len(current_schedule)

        for iteration in range(self.max_iterations):
            nodes_explored += 1
            best_neighbor = None
            best_neighbor_cost = current_cost

            # Explore all 2-swap neighbors
            for i in range(n):
                for j in range(i + 1, n):
                    neighbor = list(current_schedule)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                    cost = self.calculate_fleet_risk(neighbor)

                    if cost < best_neighbor_cost:
                        best_neighbor_cost = cost
                        best_neighbor = neighbor

            # If no neighbor improves cost, we reached a local (or global) minimum
            if best_neighbor is None or best_neighbor_cost >= current_cost:
                break

            current_schedule = best_neighbor
            current_cost = best_neighbor_cost
            cost_history.append(current_cost)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "algorithm": "Hill Climbing Local Search",
            "initial_risk": cost_history[0],
            "optimized_risk": current_cost,
            "risk_reduction_pct": round(((cost_history[0] - current_cost) / max(1.0, cost_history[0])) * 100.0, 2),
            "iterations": len(cost_history),
            "nodes_explored": nodes_explored,
            "execution_time_ms": round(elapsed_ms, 4),
            "cost_history": cost_history,
            "optimized_schedule": [b["battery_id"] for b in current_schedule]
        }


def run_hill_climbing(batteries: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Convenience runner with standard fleet test cases.
    """
    if not batteries:
        batteries = [
            {"battery_id": "B0007_Degraded", "soh": 72.0, "priority": 2.0, "temp": 36.5},
            {"battery_id": "B0005_Healthy", "soh": 92.5, "priority": 1.0, "temp": 32.0},
            {"battery_id": "B0006_Critical", "soh": 64.0, "priority": 3.0, "temp": 42.0},
            {"battery_id": "B0018_Critical", "soh": 67.0, "priority": 3.0, "temp": 40.5},
            {"battery_id": "B0005_Moderate", "soh": 84.0, "priority": 1.5, "temp": 34.0}
        ]
    optimizer = BatteryMaintenanceHillClimbing()
    return optimizer.optimize_schedule(batteries)
