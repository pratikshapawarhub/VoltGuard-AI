"""
VoltGuard AI - Practical 2 API Router
Exposes BFS, DFS, A* Search, Hill Climbing, and Backtracking CSP Solver endpoints.
"""

from fastapi import APIRouter, Query
from typing import Dict, Any, Optional

from backend.app.schemas.battery import SearchMaintenanceResponse
from backend.ml.practical2.uninformed_search import run_bfs, run_dfs
from backend.ml.practical2.informed_search import run_a_star
from backend.ml.practical2.local_search import run_hill_climbing
from backend.ml.practical2.csp_solver import run_csp_solver
from backend.app.engine.model_loader import registry

router = APIRouter(prefix="/api/practical2", tags=["Practical 2 - Search Algorithms & CSP"])


@router.get("/bfs")
def get_bfs_plan(
    start_state: str = Query("CRITICAL_FAULT"),
    goal_state: str = Query("CERTIFIED_OPERATIONAL")
):
    """
    Executes Breadth-First Search (BFS) to find the step-optimal maintenance path.
    """
    return run_bfs(start_state=start_state, goal_state=goal_state)


@router.get("/dfs")
def get_dfs_plan(
    start_state: str = Query("CRITICAL_FAULT"),
    goal_state: str = Query("CERTIFIED_OPERATIONAL")
):
    """
    Executes Depth-First Search (DFS) exploring deep diagnostic paths.
    """
    return run_dfs(start_state=start_state, goal_state=goal_state)


@router.get("/a-star")
def get_a_star_plan(
    start_state: str = Query("CRITICAL_FAULT"),
    goal_state: str = Query("CERTIFIED_OPERATIONAL")
):
    """
    Executes A* Informed Search to find the cost-optimal (lowest total maintenance cost) trajectory.
    """
    return run_a_star(start_state=start_state, goal_state=goal_state)


@router.get("/hill-climbing")
def get_hill_climbing_schedule():
    """
    Executes Hill Climbing local search to optimize fleet maintenance dispatch and minimize aggregate failure risk.
    """
    return run_hill_climbing()


@router.get("/csp")
def get_csp_schedule():
    """
    Executes Backtracking CSP Solver with MRV to generate conflict-free technician and slot assignments.
    """
    return run_csp_solver()


@router.get("/compare")
def get_search_comparison():
    """
    Returns side-by-side comparative benchmarks across all 5 search algorithms.
    """
    return registry.get_metrics("search")
