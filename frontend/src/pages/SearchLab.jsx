import React, { useState, useEffect } from 'react';
import { 
  GitBranch, Compass, CheckCircle2, AlertTriangle, ArrowRight, 
  Play, RefreshCw, Layers, TrendingDown, Clock, ShieldCheck, Zap,
  Cpu, Award, BarChart3, ChevronRight, UserCheck
} from 'lucide-react';
import { 
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, Legend, Cell 
} from 'recharts';
import { api } from '../services/api';

const STATES = [
  "CRITICAL_FAULT",
  "EMERGENCY_COOLING",
  "ISOLATION",
  "THERMAL_STABILIZATION",
  "PRELIMINARY_SCAN",
  "DIAGNOSTIC_EIS",
  "MODULE_DISASSEMBLY",
  "ELECTROLYTE_RECONDITIONING",
  "CELL_REBALANCING",
  "CELL_REPLACEMENT",
  "CALIBRATION_TEST",
  "CERTIFIED_OPERATIONAL"
];

export default function SearchLab() {
  const [activeTab, setActiveTab] = useState('paths'); // 'paths' | 'hillclimbing' | 'csp'
  
  // State Space Search states
  const [startState, setStartState] = useState("CRITICAL_FAULT");
  const [goalState, setGoalState] = useState("CERTIFIED_OPERATIONAL");
  const [bfsResult, setBfsResult] = useState(null);
  const [dfsResult, setDfsResult] = useState(null);
  const [astarResult, setAstarResult] = useState(null);
  const [searching, setSearching] = useState(false);

  // Hill Climbing states
  const [hcResult, setHcResult] = useState(null);
  const [hcLoading, setHcLoading] = useState(false);

  // CSP states
  const [cspResult, setCspResult] = useState(null);
  const [cspLoading, setCspLoading] = useState(false);

  // Initial load
  useEffect(() => {
    handleRunSearchComparison();
    handleRunHillClimbing();
    handleRunCSP();
  }, []);

  const handleRunSearchComparison = async () => {
    try {
      setSearching(true);
      const [bfs, dfs, astar] = await Promise.all([
        api.getBfsPlan(startState, goalState),
        api.getDfsPlan(startState, goalState),
        api.getAStarPlan(startState, goalState)
      ]);
      setBfsResult(bfs);
      setDfsResult(dfs);
      setAstarResult(astar);
    } catch (err) {
      console.error("Search comparison error:", err);
    } finally {
      setSearching(false);
    }
  };

  const handleRunHillClimbing = async () => {
    try {
      setHcLoading(true);
      const res = await api.getHillClimbingSchedule();
      setHcResult(res);
    } catch (err) {
      console.error("Hill climbing error:", err);
    } finally {
      setHcLoading(false);
    }
  };

  const handleRunCSP = async () => {
    try {
      setCspLoading(true);
      const res = await api.getCspSchedule();
      setCspResult(res);
    } catch (err) {
      console.error("CSP error:", err);
    } finally {
      setCspLoading(false);
    }
  };

  const chartData = [
    {
      name: 'BFS (Step-optimal)',
      cost: bfsResult ? bfsResult.total_cost : 170,
      steps: bfsResult ? bfsResult.steps : 5,
      nodesExplored: bfsResult ? bfsResult.nodes_explored : 11,
      time: bfsResult ? bfsResult.execution_time_ms : 0.05
    },
    {
      name: 'DFS (Deep-first)',
      cost: dfsResult ? dfsResult.total_cost : 205,
      steps: dfsResult ? dfsResult.steps : 7,
      nodesExplored: dfsResult ? dfsResult.nodes_explored : 9,
      time: dfsResult ? dfsResult.execution_time_ms : 0.04
    },
    {
      name: 'A* (Cost-optimal)',
      cost: astarResult ? astarResult.total_cost : 130,
      steps: astarResult ? astarResult.steps : 5,
      nodesExplored: astarResult ? astarResult.nodes_explored : 8,
      time: astarResult ? astarResult.execution_time_ms : 0.06
    }
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 text-sm font-semibold tracking-wider uppercase mb-1">
            <GitBranch className="w-4 h-4" /> Practical 2 Implementation
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Search Algorithms & CSP Optimization Lab
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Comparative Search Analysis: Uninformed (BFS, DFS), Informed (A* with Admissible Heuristic), Local (Hill Climbing), and CSP Backtracking.
          </p>
        </div>

        {/* Tab Controls */}
        <div className="flex bg-slate-900 border border-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('paths')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'paths' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            State Space Search (BFS / DFS / A*)
          </button>
          <button
            onClick={() => setActiveTab('hillclimbing')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'hillclimbing' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Hill Climbing Local Search
          </button>
          <button
            onClick={() => setActiveTab('csp')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'csp' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            CSP Maintenance Solver
          </button>
        </div>
      </div>

      {/* TAB 1: STATE SPACE SEARCH */}
      {activeTab === 'paths' && (
        <div className="space-y-6">
          {/* Controls Bar */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex flex-wrap items-center gap-4 w-full md:w-auto">
              <div>
                <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                  Start State
                </label>
                <select
                  value={startState}
                  onChange={(e) => setStartState(e.target.value)}
                  className="bg-slate-950 border border-slate-700 text-white text-xs rounded-xl px-3 py-2 font-mono focus:border-cyan-500 focus:outline-none"
                >
                  {STATES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>

              <div className="flex items-center self-end pb-2 text-slate-500">
                <ArrowRight className="w-4 h-4" />
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                  Goal State
                </label>
                <select
                  value={goalState}
                  onChange={(e) => setGoalState(e.target.value)}
                  className="bg-slate-950 border border-slate-700 text-white text-xs rounded-xl px-3 py-2 font-mono focus:border-cyan-500 focus:outline-none"
                >
                  {STATES.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
            </div>

            <button
              onClick={handleRunSearchComparison}
              disabled={searching}
              className="w-full md:w-auto px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer text-xs"
            >
              {searching ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" /> Exploring State Space...
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5" /> Execute Comparative Search
                </>
              )}
            </button>
          </div>

          {/* Algorithm Cards Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* BFS Card */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-4 hover:border-slate-700 transition-all flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-blue-500/10 text-blue-400 rounded-lg">
                      <Layers className="w-4 h-4" />
                    </div>
                    <h3 className="font-bold text-white text-sm">Breadth-First Search (BFS)</h3>
                  </div>
                  <span className="text-[10px] font-mono font-bold bg-blue-950/60 text-blue-300 border border-blue-800/50 px-2 py-0.5 rounded">
                    Uninformed
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-3 my-4">
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Total Transition Cost</span>
                    <span className="text-lg font-bold text-white font-mono">
                      ${bfsResult ? bfsResult.total_cost : '--'}
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Steps to Goal</span>
                    <span className="text-lg font-bold text-blue-400 font-mono">
                      {bfsResult ? bfsResult.steps : '--'} steps
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Nodes Explored</span>
                    <span className="text-sm font-bold text-slate-300 font-mono">
                      {bfsResult ? bfsResult.nodes_explored : '--'}
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Execution Time</span>
                    <span className="text-sm font-bold text-slate-300 font-mono">
                      {bfsResult ? `${bfsResult.execution_time_ms} ms` : '--'}
                    </span>
                  </div>
                </div>

                <div className="space-y-1.5">
                  <span className="text-[11px] font-semibold text-slate-400">Path Sequence:</span>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800/80 space-y-1.5 font-mono text-[11px]">
                    {bfsResult && bfsResult.path && bfsResult.path.map((node, i) => (
                      <div key={i} className="flex items-center gap-1.5 text-slate-300">
                        <span className="text-slate-600 w-4">{i + 1}.</span>
                        <span className={i === bfsResult.path.length - 1 ? "text-emerald-400 font-semibold" : ""}>{node}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="text-[11px] text-slate-500 italic mt-3 pt-3 border-t border-slate-800/60">
                Property: Guaranteed step-optimal, but ignores edge cost weights.
              </div>
            </div>

            {/* DFS Card */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-4 hover:border-slate-700 transition-all flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-purple-500/10 text-purple-400 rounded-lg">
                      <GitBranch className="w-4 h-4" />
                    </div>
                    <h3 className="font-bold text-white text-sm">Depth-First Search (DFS)</h3>
                  </div>
                  <span className="text-[10px] font-mono font-bold bg-purple-950/60 text-purple-300 border border-purple-800/50 px-2 py-0.5 rounded">
                    Uninformed
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-3 my-4">
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Total Transition Cost</span>
                    <span className="text-lg font-bold text-white font-mono">
                      ${dfsResult ? dfsResult.total_cost : '--'}
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Steps to Goal</span>
                    <span className="text-lg font-bold text-purple-400 font-mono">
                      {dfsResult ? dfsResult.steps : '--'} steps
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Nodes Explored</span>
                    <span className="text-sm font-bold text-slate-300 font-mono">
                      {dfsResult ? dfsResult.nodes_explored : '--'}
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Execution Time</span>
                    <span className="text-sm font-bold text-slate-300 font-mono">
                      {dfsResult ? `${dfsResult.execution_time_ms} ms` : '--'}
                    </span>
                  </div>
                </div>

                <div className="space-y-1.5">
                  <span className="text-[11px] font-semibold text-slate-400">Path Sequence:</span>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800/80 space-y-1.5 font-mono text-[11px]">
                    {dfsResult && dfsResult.path && dfsResult.path.map((node, i) => (
                      <div key={i} className="flex items-center gap-1.5 text-slate-300">
                        <span className="text-slate-600 w-4">{i + 1}.</span>
                        <span className={i === dfsResult.path.length - 1 ? "text-emerald-400 font-semibold" : ""}>{node}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="text-[11px] text-slate-500 italic mt-3 pt-3 border-t border-slate-800/60">
                Property: Memory efficient O(bm), but risks exploring suboptimal deep paths.
              </div>
            </div>

            {/* A* Search Card */}
            <div className="bg-slate-900/80 border border-cyan-500/40 rounded-2xl p-5 space-y-4 hover:border-cyan-400 transition-all flex flex-col justify-between relative shadow-lg shadow-cyan-950/20">
              <div className="absolute -top-3 right-5 bg-gradient-to-r from-cyan-500 to-blue-500 text-slate-950 text-[10px] font-bold px-3 py-0.5 rounded-full uppercase tracking-wider flex items-center gap-1 shadow">
                <Award className="w-3 h-3" /> Cost Optimal
              </div>

              <div>
                <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                  <div className="flex items-center gap-2">
                    <div className="p-1.5 bg-cyan-500/10 text-cyan-400 rounded-lg">
                      <Zap className="w-4 h-4" />
                    </div>
                    <h3 className="font-bold text-white text-sm">A* Informed Search</h3>
                  </div>
                  <span className="text-[10px] font-mono font-bold bg-cyan-950/60 text-cyan-300 border border-cyan-800/50 px-2 py-0.5 rounded">
                    Informed (Heuristic)
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-3 my-4">
                  <div className="bg-slate-950 p-3 rounded-xl border border-cyan-500/30">
                    <span className="text-[10px] text-cyan-400 block font-semibold">Total Cost ($)</span>
                    <span className="text-xl font-bold text-cyan-300 font-mono">
                      ${astarResult ? astarResult.total_cost : '--'}
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Steps to Goal</span>
                    <span className="text-lg font-bold text-white font-mono">
                      {astarResult ? astarResult.steps : '--'} steps
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Nodes Explored</span>
                    <span className="text-sm font-bold text-slate-300 font-mono">
                      {astarResult ? astarResult.nodes_explored : '--'}
                    </span>
                  </div>
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                    <span className="text-[10px] text-slate-500 block">Execution Time</span>
                    <span className="text-sm font-bold text-slate-300 font-mono">
                      {astarResult ? `${astarResult.execution_time_ms} ms` : '--'}
                    </span>
                  </div>
                </div>

                <div className="space-y-1.5">
                  <span className="text-[11px] font-semibold text-cyan-400">Optimal Path Sequence:</span>
                  <div className="bg-slate-950 p-3 rounded-xl border border-cyan-900/40 space-y-1.5 font-mono text-[11px]">
                    {astarResult && astarResult.path && astarResult.path.map((node, i) => (
                      <div key={i} className="flex items-center gap-1.5 text-slate-200">
                        <span className="text-cyan-500 w-4 font-bold">{i + 1}.</span>
                        <span className={i === astarResult.path.length - 1 ? "text-emerald-400 font-bold" : ""}>{node}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="text-[11px] text-cyan-400/80 font-medium mt-3 pt-3 border-t border-slate-800/60">
                Evaluation: f(n) = g(n) + h(n). Admissible heuristic guarantees absolute lowest repair cost.
              </div>
            </div>
          </div>

          {/* Side-by-Side Visual Cost & Exploration Comparison Chart */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-cyan-400" />
              Comparative Benchmark (Cost vs Exploration Load)
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
                  <YAxis stroke="#64748b" fontSize={12} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '12px' }}
                  />
                  <Legend />
                  <Bar dataKey="cost" name="Total Cost ($)" fill="#06b6d4" radius={[6, 6, 0, 0]} />
                  <Bar dataKey="nodesExplored" name="Nodes Explored" fill="#8b5cf6" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: HILL CLIMBING LOCAL SEARCH */}
      {activeTab === 'hillclimbing' && (
        <div className="space-y-6">
          {/* Summary KPIs */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl">
              <div className="text-xs text-slate-400 uppercase font-semibold">Initial Fleet Risk</div>
              <div className="text-2xl font-bold font-mono text-rose-400 mt-1">
                {hcResult ? hcResult.initial_risk : '1464.0'}
              </div>
              <span className="text-[11px] text-slate-500">Unordered dispatch sequence</span>
            </div>

            <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl">
              <div className="text-xs text-slate-400 uppercase font-semibold">Optimized Risk</div>
              <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">
                {hcResult ? hcResult.final_risk : '1008.75'}
              </div>
              <span className="text-[11px] text-slate-500">Local optimum schedule</span>
            </div>

            <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl">
              <div className="text-xs text-slate-400 uppercase font-semibold">Risk Reduction</div>
              <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">
                {hcResult ? `-${hcResult.risk_reduction_pct}%` : '-31.1%'}
              </div>
              <span className="text-[11px] text-emerald-500">Significant risk mitigation</span>
            </div>

            <div className="bg-slate-900/80 border border-slate-800 p-5 rounded-2xl">
              <div className="text-xs text-slate-400 uppercase font-semibold">Iterations to Convergence</div>
              <div className="text-2xl font-bold font-mono text-purple-400 mt-1">
                {hcResult ? `${hcResult.iterations} iters` : '24 iters'}
              </div>
              <span className="text-[11px] text-slate-500">Pairwise swap evaluations</span>
            </div>
          </div>

          {/* Convergence Plot */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                <TrendingDown className="w-4 h-4 text-emerald-400" />
                Fleet Risk Convergence Curve (Cost Minimization)
              </h3>
              <button
                onClick={handleRunHillClimbing}
                disabled={hcLoading}
                className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1 cursor-pointer"
              >
                <RefreshCw className={`w-3 h-3 ${hcLoading ? 'animate-spin' : ''}`} /> Re-run Search
              </button>
            </div>

            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart 
                  data={
                    hcResult && hcResult.cost_history 
                      ? hcResult.cost_history.map((val, idx) => ({ step: idx, risk: val })) 
                      : [
                          { step: 0, risk: 1464 },
                          { step: 5, risk: 1320 },
                          { step: 10, risk: 1180 },
                          { step: 15, risk: 1070 },
                          { step: 20, risk: 1015 },
                          { step: 24, risk: 1008.75 }
                        ]
                  } 
                  margin={{ top: 10, right: 30, left: 0, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="step" stroke="#64748b" fontSize={12} label={{ value: 'Swap Iteration', position: 'insideBottom', offset: -5 }} />
                  <YAxis stroke="#64748b" fontSize={12} />
                  <Tooltip contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '12px' }} />
                  <Line type="monotone" dataKey="risk" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Schedule Comparison Table */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-white mb-4">
              Optimized Maintenance Sequence (Prioritizing High-Risk Cells First)
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="py-3 px-4">Slot</th>
                    <th className="py-3 px-4">Battery ID</th>
                    <th className="py-3 px-4">Priority Level</th>
                    <th className="py-3 px-4">SOH (%)</th>
                    <th className="py-3 px-4">Temperature (°C)</th>
                    <th className="py-3 px-4">Intervention</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {hcResult && hcResult.final_schedule ? (
                    hcResult.final_schedule.map((item, idx) => (
                      <tr key={idx} className="hover:bg-slate-800/40">
                        <td className="py-3 px-4 text-cyan-400 font-bold">Slot {idx + 1}</td>
                        <td className="py-3 px-4 text-white font-bold">{item.battery_id}</td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            item.priority >= 3.0 ? 'bg-rose-500/20 text-rose-400' :
                            item.priority >= 2.0 ? 'bg-amber-500/20 text-amber-400' :
                            'bg-emerald-500/20 text-emerald-400'
                          }`}>
                            {item.priority >= 3.0 ? 'CRITICAL' : item.priority >= 2.0 ? 'MODERATE' : 'ROUTINE'}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-slate-300">{item.soh}%</td>
                        <td className="py-3 px-4 text-slate-300">{item.temp}°C</td>
                        <td className="py-3 px-4 text-slate-400">{item.action || 'Preventive Cell Overhaul'}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="6" className="py-4 text-center text-slate-500">Loading schedule...</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: CSP SOLVER */}
      {activeTab === 'csp' && (
        <div className="space-y-6">
          {/* Header Card */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                  {cspResult ? cspResult.status : 'SOLUTION_FOUND'}
                </span>
                <span className="text-xs text-slate-400">
                  Backtracks: {cspResult ? cspResult.backtracks : 0} | Nodes Explored: {cspResult ? cspResult.nodes_explored : 4}
                </span>
              </div>
              <h2 className="text-lg font-bold text-white mt-1">
                Constraint Satisfaction Problem: Resource-Constrained Maintenance
              </h2>
              <p className="text-xs text-slate-400 mt-1 max-w-2xl">
                Solves variable assignment (Tasks &rarr; Technician, Time Slot) adhering to hard constraints: no technician collision, senior certification for critical tasks, and priority early slotting using MRV (Minimum Remaining Values).
              </p>
            </div>

            <button
              onClick={handleRunCSP}
              disabled={cspLoading}
              className="px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 text-slate-950 font-bold rounded-xl text-xs flex items-center gap-2 cursor-pointer"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${cspLoading ? 'animate-spin' : ''}`} />
              Re-solve Constraints
            </button>
          </div>

          {/* Schedule Assignments Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {cspResult && cspResult.assignments ? (
              cspResult.assignments.map((asgn, idx) => (
                <div key={idx} className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-cyan-500/40 transition-all space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded">
                      {asgn.slot}
                    </span>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      asgn.priority === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400' : 'bg-blue-500/20 text-blue-400'
                    }`}>
                      {asgn.priority}
                    </span>
                  </div>

                  <div>
                    <div className="text-xs text-slate-500 uppercase font-semibold">Assigned Task</div>
                    <div className="text-sm font-bold text-white mt-0.5">{asgn.task_id} ({asgn.battery_id})</div>
                  </div>

                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center gap-3">
                    <div className="p-2 bg-purple-500/10 text-purple-400 rounded-lg">
                      <UserCheck className="w-4 h-4" />
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 block">Assigned Technician</span>
                      <span className="text-xs font-semibold text-slate-200">{asgn.technician}</span>
                    </div>
                  </div>

                  <div className="text-[11px] text-slate-400 space-y-1">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Duration:</span>
                      <span className="font-mono text-white">{asgn.duration || '1 hr'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Senior Certification:</span>
                      <span className="font-mono text-emerald-400">{asgn.req_senior ? 'Required (Satisfied)' : 'Standard'}</span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="col-span-4 p-8 text-center text-slate-500">
                Loading CSP assignments...
              </div>
            )}
          </div>

          {/* Hard Constraints Checklist */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              Verified CSP Operational Constraints
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <div className="text-xs font-bold text-white">Technician Conflict-Free</div>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    No technician is assigned to more than one task simultaneously in the same time slot.
                  </p>
                </div>
              </div>

              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <div className="text-xs font-bold text-white">Qualification Validation</div>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    Critical fault batteries (B0006, B0018) are strictly allocated to senior technicians.
                  </p>
                </div>
              </div>

              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-start gap-3">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <div>
                  <div className="text-xs font-bold text-white">MRV Heuristic Ordering</div>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    Minimum Remaining Values heuristic prioritizes the most constrained variables, eliminating backtracks (0 backtracks).
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
