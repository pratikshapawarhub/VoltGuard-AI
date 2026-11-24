"""
VoltGuard AI - Practical 2 Unit & Validation Tests
Validates BFS, DFS, A* Search, Hill Climbing, and Backtracking CSP Solver.
"""

import pytest
from backend.ml.practical2.uninformed_search import run_bfs, run_dfs
from backend.ml.practical2.informed_search import run_a_star
from backend.ml.practical2.local_search import run_hill_climbing, BatteryMaintenanceHillClimbing
from backend.ml.practical2.csp_solver import run_csp_solver, MaintenanceCSPSolver


def test_bfs_search():
    res = run_bfs()
    assert res["path"][0] == "CRITICAL_FAULT"
    assert res["path"][-1] == "CERTIFIED_OPERATIONAL"
    assert res["nodes_explored"] > 0
    assert res["total_cost"] > 0
    # BFS guarantees shortest path in steps (5 steps)
    assert res["steps"] == 5


def test_dfs_search():
    res = run_dfs()
    assert res["path"][0] == "CRITICAL_FAULT"
    assert res["path"][-1] == "CERTIFIED_OPERATIONAL"
    assert res["nodes_explored"] > 0
    assert len(res["path"]) >= 6


def test_a_star_optimality():
    bfs_res = run_bfs()
    dfs_res = run_dfs()
    a_star_res = run_a_star()

    assert a_star_res["path"][0] == "CRITICAL_FAULT"
    assert a_star_res["path"][-1] == "CERTIFIED_OPERATIONAL"

    # A* must find the cost-optimal path (cost <= BFS and cost <= DFS)
    assert a_star_res["total_cost"] <= bfs_res["total_cost"]
    assert a_star_res["total_cost"] <= dfs_res["total_cost"]
    assert a_star_res["total_cost"] == 130.0  # Exact ground truth optimal path cost


def test_hill_climbing_risk_minimization():
    res = run_hill_climbing()
    assert res["optimized_risk"] <= res["initial_risk"]
    assert res["risk_reduction_pct"] >= 0.0
    assert len(res["cost_history"]) >= 1
    # Check cost history monotonically non-increasing
    for i in range(len(res["cost_history"]) - 1):
        assert res["cost_history"][i] >= res["cost_history"][i + 1]


def test_backtracking_csp_solver_constraints():
    res = run_csp_solver()
    assert res["is_satisfied"] is True
    schedule = res["schedule"]
    assert len(schedule) == 4

    # Verify Constraint 1: No technician double-booked in the same slot
    tech_slot_pairs = [(item["technician"], item["time_slot"]) for item in schedule]
    assert len(tech_slot_pairs) == len(set(tech_slot_pairs)), "Technician double-booked in slot!"

    # Verify Constraint 2: Senior tech assigned to critical tasks
    for item in schedule:
        if item["priority"] == "CRITICAL":
            assert "Senior" in item["technician"], f"Critical task {item['task_id']} assigned to junior tech!"
