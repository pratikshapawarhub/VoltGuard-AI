"""
VoltGuard AI - Practical 2: Uninformed Search Algorithms
Implements Breadth-First Search (BFS) and Depth-First Search (DFS)
to explore battery diagnostic state transitions from a fault state to a certified operational state.
"""

import time
from collections import deque
from typing import Dict, List, Any, Optional, Set, Tuple

# Battery Maintenance State Transition Graph
# Nodes represent discrete operational & servicing states.
# Edge values represent transition cost (hours / resource cost).
MAINTENANCE_GRAPH: Dict[str, Dict[str, float]] = {
    "CRITICAL_FAULT": {
        "ISOLATION": 15.0,
        "EMERGENCY_COOLING": 25.0
    },
    "EMERGENCY_COOLING": {
        "ISOLATION": 10.0,
        "THERMAL_STABILIZATION": 20.0
    },
    "ISOLATION": {
        "THERMAL_STABILIZATION": 15.0,
        "MODULE_DISASSEMBLY": 35.0,
        "PRELIMINARY_SCAN": 20.0
    },
    "THERMAL_STABILIZATION": {
        "DIAGNOSTIC_EIS": 25.0,
        "PRELIMINARY_SCAN": 15.0
    },
    "PRELIMINARY_SCAN": {
        "DIAGNOSTIC_EIS": 20.0,
        "CELL_REBALANCING": 45.0
    },
    "DIAGNOSTIC_EIS": {
        "MODULE_DISASSEMBLY": 30.0,
        "ELECTROLYTE_RECONDITIONING": 60.0,
        "CELL_REPLACEMENT": 90.0
    },
    "MODULE_DISASSEMBLY": {
        "CELL_REPLACEMENT": 75.0,
        "CELL_REBALANCING": 40.0
    },
    "ELECTROLYTE_RECONDITIONING": {
        "CALIBRATION_TEST": 35.0
    },
    "CELL_REBALANCING": {
        "CALIBRATION_TEST": 30.0
    },
    "CELL_REPLACEMENT": {
        "CALIBRATION_TEST": 25.0
    },
    "CALIBRATION_TEST": {
        "CERTIFIED_OPERATIONAL": 20.0
    },
    "CERTIFIED_OPERATIONAL": {}
}


def run_bfs(
    start_state: str = "CRITICAL_FAULT",
    goal_state: str = "CERTIFIED_OPERATIONAL",
    graph: Dict[str, Dict[str, float]] = MAINTENANCE_GRAPH
) -> Dict[str, Any]:
    """
    Breadth-First Search (BFS) exploring level-by-level.
    Guaranteed to find the path with the fewest state transitions.
    """
    start_time = time.perf_counter()
    queue = deque([[start_state]])
    visited = {start_state}
    nodes_explored = 0

    while queue:
        path = queue.popleft()
        current_node = path[-1]
        nodes_explored += 1

        if current_node == goal_state:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            # Calculate total path cost
            total_cost = 0.0
            for i in range(len(path) - 1):
                total_cost += graph.get(path[i], {}).get(path[i + 1], 0.0)

            return {
                "algorithm": "Breadth-First Search (BFS)",
                "start_state": start_state,
                "goal_state": goal_state,
                "path": path,
                "steps": len(path) - 1,
                "total_cost": round(total_cost, 2),
                "nodes_explored": nodes_explored,
                "execution_time_ms": round(elapsed_ms, 4),
                "is_optimal_cost": False  # BFS minimizes steps, not cost
            }

        for neighbor in graph.get(current_node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return {
        "algorithm": "Breadth-First Search (BFS)",
        "start_state": start_state,
        "goal_state": goal_state,
        "path": [],
        "steps": 0,
        "total_cost": 0.0,
        "nodes_explored": nodes_explored,
        "execution_time_ms": round(elapsed_ms, 4),
        "found": False
    }


def run_dfs(
    start_state: str = "CRITICAL_FAULT",
    goal_state: str = "CERTIFIED_OPERATIONAL",
    graph: Dict[str, Dict[str, float]] = MAINTENANCE_GRAPH
) -> Dict[str, Any]:
    """
    Depth-First Search (DFS) exploring deep paths before backtracking.
    """
    start_time = time.perf_counter()
    stack = [[start_state]]
    visited = set()
    nodes_explored = 0

    while stack:
        path = stack.pop()
        current_node = path[-1]

        if current_node not in visited:
            nodes_explored += 1
            visited.add(current_node)

            if current_node == goal_state:
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                total_cost = 0.0
                for i in range(len(path) - 1):
                    total_cost += graph.get(path[i], {}).get(path[i + 1], 0.0)

                return {
                    "algorithm": "Depth-First Search (DFS)",
                    "start_state": start_state,
                    "goal_state": goal_state,
                    "path": path,
                    "steps": len(path) - 1,
                    "total_cost": round(total_cost, 2),
                    "nodes_explored": nodes_explored,
                    "execution_time_ms": round(elapsed_ms, 4),
                    "is_optimal_cost": False
                }

            # Push unvisited neighbors onto stack (reverse order for consistent traversal)
            for neighbor in reversed(list(graph.get(current_node, {}).keys())):
                if neighbor not in visited:
                    stack.append(path + [neighbor])

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return {
        "algorithm": "Depth-First Search (DFS)",
        "start_state": start_state,
        "goal_state": goal_state,
        "path": [],
        "steps": 0,
        "total_cost": 0.0,
        "nodes_explored": nodes_explored,
        "execution_time_ms": round(elapsed_ms, 4),
        "found": False
    }
