"""
VoltGuard AI - Practical 2: Informed Search (A* Search)
Implements A* Search to discover the lowest estimated maintenance cost path
from a degraded battery state to a fully certified operational state.
"""

import time
import heapq
from typing import Dict, List, Any, Optional, Tuple
from backend.ml.practical2.uninformed_search import MAINTENANCE_GRAPH

# Admissible Heuristic Function h(n)
# Estimates lower-bound cost to reach 'CERTIFIED_OPERATIONAL'.
# Must satisfy: h(n) <= actual_cost(n, goal) for admissibility.
HEURISTIC_COSTS: Dict[str, float] = {
    "CRITICAL_FAULT": 105.0,
    "EMERGENCY_COOLING": 95.0,
    "ISOLATION": 90.0,
    "THERMAL_STABILIZATION": 75.0,
    "PRELIMINARY_SCAN": 65.0,
    "DIAGNOSTIC_EIS": 55.0,
    "MODULE_DISASSEMBLY": 65.0,
    "ELECTROLYTE_RECONDITIONING": 50.0,
    "CELL_REBALANCING": 45.0,
    "CELL_REPLACEMENT": 40.0,
    "CALIBRATION_TEST": 20.0,
    "CERTIFIED_OPERATIONAL": 0.0
}


def run_a_star(
    start_state: str = "CRITICAL_FAULT",
    goal_state: str = "CERTIFIED_OPERATIONAL",
    graph: Dict[str, Dict[str, float]] = MAINTENANCE_GRAPH,
    heuristic: Dict[str, float] = HEURISTIC_COSTS
) -> Dict[str, Any]:
    """
    A* Informed Search using evaluation function f(n) = g(n) + h(n).
    Guaranteed to return the optimal (lowest cost) maintenance trajectory.
    """
    start_time = time.perf_counter()

    # Priority queue stores tuples: (f_score, g_score, current_node, path)
    initial_h = heuristic.get(start_state, 0.0)
    open_set = [(initial_h, 0.0, start_state, [start_state])]
    heapq.heapify(open_set)

    # Tracks lowest g_score found to each node
    g_scores = {start_state: 0.0}
    nodes_explored = 0
    step_evaluations = []

    while open_set:
        f_score, g_score, current, path = heapq.heappop(open_set)
        nodes_explored += 1

        step_evaluations.append({
            "node": current,
            "g_cost": round(g_score, 2),
            "h_cost": round(heuristic.get(current, 0.0), 2),
            "f_total": round(f_score, 2)
        })

        if current == goal_state:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "algorithm": "A* Informed Search",
                "start_state": start_state,
                "goal_state": goal_state,
                "path": path,
                "steps": len(path) - 1,
                "total_cost": round(g_score, 2),
                "nodes_explored": nodes_explored,
                "execution_time_ms": round(elapsed_ms, 4),
                "is_optimal_cost": True,
                "evaluations_trace": step_evaluations
            }

        for neighbor, weight in graph.get(current, {}).items():
            tentative_g = g_score + weight
            if tentative_g < g_scores.get(neighbor, float('inf')):
                g_scores[neighbor] = tentative_g
                h_val = heuristic.get(neighbor, 0.0)
                f_val = tentative_g + h_val
                heapq.heappush(open_set, (f_val, tentative_g, neighbor, path + [neighbor]))

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return {
        "algorithm": "A* Informed Search",
        "start_state": start_state,
        "goal_state": goal_state,
        "path": [],
        "steps": 0,
        "total_cost": 0.0,
        "nodes_explored": nodes_explored,
        "execution_time_ms": round(elapsed_ms, 4),
        "found": False
    }
