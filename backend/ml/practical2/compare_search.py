"""
VoltGuard AI - Practical 2: Search Algorithms Benchmark & Comparison
Executes and compares:
1. Breadth-First Search (BFS)
2. Depth-First Search (DFS)
3. A* Informed Search
4. Hill Climbing Local Search
5. Backtracking CSP Solver
Saves unified benchmark results to backend/saved_models/search_comparison.json.
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.ml.practical2.uninformed_search import run_bfs, run_dfs
from backend.ml.practical2.informed_search import run_a_star
from backend.ml.practical2.local_search import run_hill_climbing
from backend.ml.practical2.csp_solver import run_csp_solver

MODELS_DIR = os.path.join(BASE_DIR, "backend", "saved_models")


def run_all_search_benchmarks() -> dict:
    os.makedirs(MODELS_DIR, exist_ok=True)

    print("Running Uninformed Search: BFS & DFS...")
    bfs_result = run_bfs()
    dfs_result = run_dfs()

    print("Running Informed Search: A*...")
    a_star_result = run_a_star()

    print("Running Local Search: Hill Climbing...")
    hc_result = run_hill_climbing()

    print("Running Constraint Satisfaction Problem: Backtracking CSP...")
    csp_result = run_csp_solver()

    benchmark_summary = {
        "Graph_Search_Comparison": [
            {
                "algorithm": bfs_result["algorithm"],
                "path": " -> ".join(bfs_result["path"]),
                "steps": bfs_result["steps"],
                "total_cost": bfs_result["total_cost"],
                "nodes_explored": bfs_result["nodes_explored"],
                "execution_time_ms": bfs_result["execution_time_ms"],
                "optimality": "Step-Optimal (Fewest Transitions)"
            },
            {
                "algorithm": dfs_result["algorithm"],
                "path": " -> ".join(dfs_result["path"]),
                "steps": dfs_result["steps"],
                "total_cost": dfs_result["total_cost"],
                "nodes_explored": dfs_result["nodes_explored"],
                "execution_time_ms": dfs_result["execution_time_ms"],
                "optimality": "Non-Optimal (Deep Traversal)"
            },
            {
                "algorithm": a_star_result["algorithm"],
                "path": " -> ".join(a_star_result["path"]),
                "steps": a_star_result["steps"],
                "total_cost": a_star_result["total_cost"],
                "nodes_explored": a_star_result["nodes_explored"],
                "execution_time_ms": a_star_result["execution_time_ms"],
                "optimality": "Cost-Optimal (Lowest Total Maintenance Cost)"
            }
        ],
        "Local_Search": hc_result,
        "Constraint_Satisfaction": csp_result
    }

    save_path = os.path.join(MODELS_DIR, "search_comparison.json")
    with open(save_path, "w") as f:
        json.dump(benchmark_summary, f, indent=2)

    print(f"\nSaved search benchmark comparison to {save_path}")
    return benchmark_summary


if __name__ == "__main__":
    results = run_all_search_benchmarks()
    print("\n--- Practical 2 Search Benchmark Results ---")
    for r in results["Graph_Search_Comparison"]:
        print(f"\n{r['algorithm']}:")
        print(f"  Path:             {r['path']}")
        print(f"  Cost:             ${r['total_cost']}")
        print(f"  Nodes Explored:   {r['nodes_explored']}")
        print(f"  Time:             {r['execution_time_ms']} ms")
        print(f"  Optimality:       {r['optimality']}")

    print("\nHill Climbing Local Optimization:")
    print(f"  Initial Fleet Risk: {results['Local_Search']['initial_risk']}")
    print(f"  Optimized Risk:     {results['Local_Search']['optimized_risk']} (-{results['Local_Search']['risk_reduction_pct']}%)")
    print(f"  Iterations:         {results['Local_Search']['iterations']}")

    print("\nBacktracking CSP Solver:")
    print(f"  Solved Satisfied:   {results['Constraint_Satisfaction']['is_satisfied']}")
    print(f"  Nodes Explored:     {results['Constraint_Satisfaction']['nodes_explored']}")
    print(f"  Backtracks:         {results['Constraint_Satisfaction']['backtracks_count']}")
    print(f"  Schedule Generated: {len(results['Constraint_Satisfaction']['schedule'])} tasks scheduled conflict-free")
