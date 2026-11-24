import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, AlertTriangle, AlertOctagon, CheckCircle2, 
  Cpu, Wrench, Activity, Compass, ChevronRight, Sliders, Play, RotateCcw,
  Info, Database, Layers, Check
} from 'lucide-react';
import { api } from '../services/api';

const PRESETS = {
  healthy: {
    label: "Fresh Cell (Nominal)",
    cycle_number: 15,
    voltage_mean: 3.65,
    voltage_max: 4.19,
    voltage_min: 2.85,
    voltage_std: 0.18,
    current_mean: 1.85,
    current_std: 0.40,
    temperature_mean: 28.5,
    temperature_max: 32.5,
    temperature_min: 24.0,
    charge_duration: 10400.0,
    discharge_duration: 3500.0,
    internal_impedance: 0.118,
    recent_soh_drop: 0.2
  },
  thermal_risk: {
    label: "Thermal Stress Alert",
    cycle_number: 85,
    voltage_mean: 3.42,
    voltage_max: 4.22,
    voltage_min: 2.35,
    voltage_std: 0.28,
    current_mean: 1.95,
    current_std: 0.55,
    temperature_mean: 41.0,
    temperature_max: 49.5,
    temperature_min: 26.0,
    charge_duration: 10800.0,
    discharge_duration: 2800.0,
    internal_impedance: 0.145,
    recent_soh_drop: 1.2
  },
  degraded_eol: {
    label: "Severe Degradation (EOL)",
    cycle_number: 145,
    voltage_mean: 3.25,
    voltage_max: 4.15,
    voltage_min: 2.10,
    voltage_std: 0.35,
    current_mean: 1.80,
    current_std: 0.60,
    temperature_mean: 34.0,
    temperature_max: 39.0,
    temperature_min: 24.5,
    charge_duration: 11200.0,
    discharge_duration: 2100.0,
    internal_impedance: 0.185,
    recent_soh_drop: 2.8
  },
  impedance_spike: {
    label: "Impedance Growth / Short Risk",
    cycle_number: 110,
    voltage_mean: 3.35,
    voltage_max: 4.18,
    voltage_min: 2.25,
    voltage_std: 0.30,
    current_mean: 1.90,
    current_std: 0.50,
    temperature_mean: 37.0,
    temperature_max: 43.5,
    temperature_min: 25.0,
    charge_duration: 10900.0,
    discharge_duration: 2600.0,
    internal_impedance: 0.225,
    recent_soh_drop: 1.8
  }
};

export default function PEASAndExpertSystem() {
  const [activeTab, setActiveTab] = useState('peas'); // 'peas' | 'simulator' | 'rulebase'
  const [peasData, setPeasData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Simulator state
  const [inputs, setInputs] = useState(PRESETS.healthy);
  const [evalResult, setEvalResult] = useState(null);
  const [evaluating, setEvaluating] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const res = await api.getPeasMatrix();
        setPeasData(res);
      } catch (err) {
        console.error("Failed to load PEAS metadata:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleRunEvaluation = async () => {
    try {
      setEvaluating(true);
      const res = await api.evaluateExpertRules(inputs);
      setEvalResult(res);
    } catch (err) {
      console.error("Evaluation failed:", err);
    } finally {
      setEvaluating(false);
    }
  };

  const applyPreset = (key) => {
    setInputs({ ...PRESETS[key] });
    setEvalResult(null);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 text-sm font-semibold tracking-wider uppercase mb-1">
            <Compass className="w-4 h-4" /> Practical 1 Implementation
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            PEAS Descriptors & Rule-Based Expert System
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Russell & Norvig AI Agent Specification & Deterministic Forward-Chaining Inference Engine.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-slate-900 border border-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('peas')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'peas' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            PEAS Specification
          </button>
          <button
            onClick={() => setActiveTab('simulator')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'simulator' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Live Rule Simulator
          </button>
          <button
            onClick={() => setActiveTab('rulebase')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'rulebase' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Knowledge Base Rules
          </button>
        </div>
      </div>

      {/* TAB 1: PEAS MATRIX */}
      {activeTab === 'peas' && (
        <div className="space-y-6">
          {/* Agent Meta Banner */}
          {peasData && (
            <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
              <div>
                <span className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Agent Name:</span>
                <span className="text-sm font-bold text-white ml-2">{peasData.agent_name}</span>
              </div>
              <div>
                <span className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Agent Class:</span>
                <span className="text-sm font-mono text-cyan-400 ml-2">{peasData.agent_type}</span>
              </div>
            </div>
          )}

          {/* 4 Pillars Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Performance Measures */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-emerald-500/40 transition-all">
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2.5 bg-emerald-500/10 text-emerald-400 rounded-xl border border-emerald-500/20">
                  <Activity className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-white text-base">Performance (P)</h3>
                  <span className="text-xs text-slate-500">Agent Goals & Metrics</span>
                </div>
              </div>
              <ul className="text-xs text-slate-400 space-y-2 mt-3">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">•</span>
                  <span><strong>SOH Accuracy:</strong> R² &ge; 0.95, MAE &le; 2.0%</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">•</span>
                  <span><strong>RUL Prognosis:</strong> MAE &le; 20 cycles</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">•</span>
                  <span><strong>Thermal Safety:</strong> 100% Runaway Prevention Recall</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">•</span>
                  <span><strong>Dispatch Efficiency:</strong> Cost-optimal A* Search repair plan</span>
                </li>
              </ul>
            </div>

            {/* Environment */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-blue-500/40 transition-all">
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2.5 bg-blue-500/10 text-blue-400 rounded-xl border border-blue-500/20">
                  <Layers className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-white text-base">Environment (E)</h3>
                  <span className="text-xs text-slate-500">Operational Domain</span>
                </div>
              </div>
              <ul className="text-xs text-slate-400 space-y-2 mt-3">
                <li className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5">•</span>
                  <span><strong>Cells:</strong> NASA 18650 LiCoO₂ (Nominal 2.0 Ahr)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5">•</span>
                  <span><strong>Chamber:</strong> 24°C standard temperature bench</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5">•</span>
                  <span><strong>Profiles:</strong> CC-CV Charge & 2.0A constant discharge</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5">•</span>
                  <span><strong>Dynamics:</strong> Stochastic, Sequential, Non-linear aging</span>
                </li>
              </ul>
            </div>

            {/* Actuators */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-amber-500/40 transition-all">
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2.5 bg-amber-500/10 text-amber-400 rounded-xl border border-amber-500/20">
                  <Wrench className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-white text-base">Actuators (A)</h3>
                  <span className="text-xs text-slate-500">Control & Interventions</span>
                </div>
              </div>
              <ul className="text-xs text-slate-400 space-y-2 mt-3">
                <li className="flex items-start gap-2">
                  <span className="text-amber-400 mt-0.5">•</span>
                  <span><strong>Safety Switch:</strong> Emergency High-Voltage Relay Cutoff</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-400 mt-0.5">•</span>
                  <span><strong>BMS Control:</strong> Charge Rate Throttling (0.5C / 0.25C)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-400 mt-0.5">•</span>
                  <span><strong>Work Orders:</strong> Cell Replacement & Module Rebalancing</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-400 mt-0.5">•</span>
                  <span><strong>Scheduling:</strong> CSP Conflict-free Fleet Dispatch</span>
                </li>
              </ul>
            </div>

            {/* Sensors */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-purple-500/40 transition-all">
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2.5 bg-purple-500/10 text-purple-400 rounded-xl border border-purple-500/20">
                  <Cpu className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-white text-base">Sensors (S)</h3>
                  <span className="text-xs text-slate-500">Telemetry Ingestion</span>
                </div>
              </div>
              <ul className="text-xs text-slate-400 space-y-2 mt-3">
                <li className="flex items-start gap-2">
                  <span className="text-purple-400 mt-0.5">•</span>
                  <span><strong>Voltage:</strong> High-precision ADC Cell Probes (V_meas)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-400 mt-0.5">•</span>
                  <span><strong>Current:</strong> Hall-Effect In-line Shunts (I_meas)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-400 mt-0.5">•</span>
                  <span><strong>Thermal:</strong> K-Type Surface Thermocouples (T_meas)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-400 mt-0.5">•</span>
                  <span><strong>Impedance:</strong> EIS Spectroscopy (Re, Rct Impedance)</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Russell & Norvig Characterization Table */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-base font-semibold text-white mb-4 flex items-center gap-2">
              <Info className="w-4 h-4 text-cyan-400" />
              Russell & Norvig Task Environment Characterization
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider">Observability</div>
                <div className="text-sm font-semibold text-cyan-400 mt-1">Partially Observable</div>
                <p className="text-xs text-slate-400 mt-1">
                  SEI growth and internal lithium plating cannot be inspected directly without destructive physical disassembly.
                </p>
              </div>

              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider">Determinism</div>
                <div className="text-sm font-semibold text-cyan-400 mt-1">Stochastic</div>
                <p className="text-xs text-slate-400 mt-1">
                  Aging dynamics vary under heat dissipation, thermal gradients, and non-deterministic ambient temperature fluctuations.
                </p>
              </div>

              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider">Episodic vs Sequential</div>
                <div className="text-sm font-semibold text-cyan-400 mt-1">Sequential</div>
                <p className="text-xs text-slate-400 mt-1">
                  Each charge-discharge cycle irreversibly consumes battery cycle life; past usage directly impacts current and future SOH.
                </p>
              </div>

              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider">Static vs Dynamic</div>
                <div className="text-sm font-semibold text-cyan-400 mt-1">Dynamic</div>
                <p className="text-xs text-slate-400 mt-1">
                  Internal electrochemical states drift continuously while the agent is computing decisions or waiting for operator input.
                </p>
              </div>

              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider">Discrete vs Continuous</div>
                <div className="text-sm font-semibold text-cyan-400 mt-1">Continuous</div>
                <p className="text-xs text-slate-400 mt-1">
                  Voltage, current, temperature, and impedance curves vary continuously across the continuous time domain.
                </p>
              </div>

              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80">
                <div className="text-xs text-slate-500 uppercase font-bold tracking-wider">Agent Type</div>
                <div className="text-sm font-semibold text-cyan-400 mt-1">Goal- & Utility-Based Hybrid</div>
                <p className="text-xs text-slate-400 mt-1">
                  Satisfies safety thresholds (goal: prevent runaway) while maximizing operational battery lifetime (utility).
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: LIVE RULE SIMULATOR */}
      {activeTab === 'simulator' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: Preset Controls & Parameter Sliders */}
          <div className="lg:col-span-5 space-y-6">
            {/* Presets */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-3">
                Load Test Scenario Preset
              </label>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(PRESETS).map(([key, item]) => (
                  <button
                    key={key}
                    onClick={() => applyPreset(key)}
                    className="p-3 text-left rounded-xl border border-slate-800 bg-slate-950 hover:border-cyan-500/50 hover:bg-slate-900 transition-all group"
                  >
                    <div className="text-xs font-semibold text-slate-200 group-hover:text-cyan-400">
                      {item.label}
                    </div>
                    <div className="text-[10px] text-slate-500 mt-1">
                      Cycle: {item.cycle_number} | Temp: {item.temperature_max}°C
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Slider Controls */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Sliders className="w-4 h-4 text-cyan-400" />
                  Telemetry Parameter Inputs
                </h3>
                <button
                  onClick={() => applyPreset('healthy')}
                  className="text-xs text-slate-400 hover:text-white flex items-center gap-1"
                >
                  <RotateCcw className="w-3 h-3" /> Reset
                </button>
              </div>

              {/* Peak Temperature */}
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Peak Temperature (T_max)</span>
                  <span className={`font-semibold ${inputs.temperature_max >= 42 ? 'text-rose-400' : inputs.temperature_max >= 39.5 ? 'text-amber-400' : 'text-emerald-400'}`}>
                    {inputs.temperature_max}°C
                  </span>
                </div>
                <input
                  type="range"
                  min="20"
                  max="55"
                  step="0.5"
                  value={inputs.temperature_max}
                  onChange={(e) => setInputs({ ...inputs, temperature_max: parseFloat(e.target.value) })}
                  className="w-full accent-amber-400 cursor-pointer"
                />
              </div>

              {/* Internal Impedance */}
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Internal Impedance (Re + Rct)</span>
                  <span className="font-semibold text-purple-400">{inputs.internal_impedance} Ω</span>
                </div>
                <input
                  type="range"
                  min="0.08"
                  max="0.30"
                  step="0.005"
                  value={inputs.internal_impedance}
                  onChange={(e) => setInputs({ ...inputs, internal_impedance: parseFloat(e.target.value) })}
                  className="w-full accent-purple-400 cursor-pointer"
                />
              </div>

              {/* End of Discharge Voltage Min */}
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">End-of-Discharge Cut-off (V_min)</span>
                  <span className={`font-semibold ${inputs.voltage_min < 2.5 ? 'text-rose-400' : 'text-cyan-400'}`}>
                    {inputs.voltage_min} V
                  </span>
                </div>
                <input
                  type="range"
                  min="1.9"
                  max="3.2"
                  step="0.05"
                  value={inputs.voltage_min}
                  onChange={(e) => setInputs({ ...inputs, voltage_min: parseFloat(e.target.value) })}
                  className="w-full accent-cyan-400 cursor-pointer"
                />
              </div>

              {/* Cycle Number */}
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Aging Cycle Number</span>
                  <span className="font-semibold text-blue-400">Cycle {inputs.cycle_number}</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="180"
                  step="1"
                  value={inputs.cycle_number}
                  onChange={(e) => setInputs({ ...inputs, cycle_number: parseInt(e.target.value) })}
                  className="w-full accent-blue-400 cursor-pointer"
                />
              </div>

              {/* Recent SOH Drop */}
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Recent 5-Cycle Capacity Drop</span>
                  <span className={`font-semibold ${inputs.recent_soh_drop > 2.0 ? 'text-rose-400' : 'text-slate-300'}`}>
                    {inputs.recent_soh_drop}%
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="5.0"
                  step="0.1"
                  value={inputs.recent_soh_drop}
                  onChange={(e) => setInputs({ ...inputs, recent_soh_drop: parseFloat(e.target.value) })}
                  className="w-full accent-slate-400 cursor-pointer"
                />
              </div>

              {/* Action Button */}
              <button
                onClick={handleRunEvaluation}
                disabled={evaluating}
                className="w-full mt-4 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer"
              >
                {evaluating ? (
                  <>
                    <Activity className="w-4 h-4 animate-spin" /> Evaluating Rule Base...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4" /> Run Forward-Chaining Inference
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Right Column: Expert System Inference Result */}
          <div className="lg:col-span-7 space-y-6">
            {evalResult ? (
              <>
                {/* Alert Level & Main Recommendation Banner */}
                <div className={`p-6 rounded-2xl border ${
                  evalResult.overall_status === 'CRITICAL'
                    ? 'bg-rose-500/10 border-rose-500/30'
                    : evalResult.overall_status === 'WARNING'
                    ? 'bg-amber-500/10 border-amber-500/30'
                    : 'bg-emerald-500/10 border-emerald-500/30'
                }`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      {evalResult.overall_status === 'CRITICAL' ? (
                        <AlertOctagon className="w-8 h-8 text-rose-400 animate-pulse" />
                      ) : evalResult.overall_status === 'WARNING' ? (
                        <AlertTriangle className="w-8 h-8 text-amber-400" />
                      ) : (
                        <CheckCircle2 className="w-8 h-8 text-emerald-400" />
                      )}
                      <div>
                        <div className="flex items-center gap-2">
                          <span className={`text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                            evalResult.overall_status === 'CRITICAL'
                              ? 'bg-rose-500/20 text-rose-300'
                              : evalResult.overall_status === 'WARNING'
                              ? 'bg-amber-500/20 text-amber-300'
                              : 'bg-emerald-500/20 text-emerald-300'
                          }`}>
                            {evalResult.overall_status}
                          </span>
                          <span className="text-xs text-slate-400">
                            {evalResult.triggered_rules_count} / {evalResult.rules_evaluated_count} Rules Triggered
                          </span>
                        </div>
                        <h2 className="text-base font-bold text-white mt-1">
                          {evalResult.condition_summary}
                        </h2>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Recommendations */}
                {evalResult.recommendations && evalResult.recommendations.length > 0 && (
                  <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                    <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                      <Wrench className="w-4 h-4 text-cyan-400" />
                      Prescriptive Maintenance Directives
                    </h3>
                    <div className="space-y-3">
                      {evalResult.recommendations.map((rec, idx) => (
                        <div key={idx} className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-start gap-3">
                          <div className="p-1.5 bg-cyan-500/10 text-cyan-400 rounded-lg shrink-0 mt-0.5">
                            <Check className="w-4 h-4" />
                          </div>
                          <div className="space-y-1">
                            <div className="flex items-center gap-2">
                              <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-950/50 border border-cyan-800/40 px-2 py-0.5 rounded">
                                {rec.action_code}
                              </span>
                              <span className="text-xs text-slate-500">Priority {rec.priority}</span>
                            </div>
                            <p className="text-xs text-slate-300">{rec.action}</p>
                            <p className="text-[11px] text-slate-500 italic">Triggered by: {rec.triggered_by}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Triggered Rules List */}
                <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
                  <h3 className="text-sm font-semibold text-white mb-4 flex items-center justify-between">
                    <span>Fired IF-THEN Rules ({evalResult.triggered_rules.length})</span>
                    <span className="text-xs text-slate-500 font-mono">Forward Chaining</span>
                  </h3>

                  <div className="space-y-3">
                    {evalResult.triggered_rules.map((rule, idx) => (
                      <div 
                        key={idx}
                        className={`p-4 rounded-xl border ${
                          rule.severity === 'CRITICAL'
                            ? 'bg-rose-950/20 border-rose-500/30'
                            : rule.severity === 'WARNING'
                            ? 'bg-amber-950/20 border-amber-500/30'
                            : 'bg-emerald-950/20 border-emerald-500/30'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-mono font-bold text-white bg-slate-800 px-2 py-0.5 rounded">
                              {rule.rule_id}
                            </span>
                            <span className="text-xs font-semibold text-slate-200">
                              {rule.name}
                            </span>
                          </div>
                          <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                            rule.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
                          }`}>
                            {rule.severity}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 mt-2">{rule.description}</p>
                        <div className="text-xs text-cyan-400 font-mono mt-2 bg-slate-950/60 p-2 rounded border border-slate-800/60 flex items-center justify-between">
                          <span>Action: {rule.action_code}</span>
                          <span className="text-slate-400">{rule.recommendation}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Disclaimer */}
                {evalResult.disclaimer && (
                  <div className="text-[11px] text-slate-500 italic p-3 bg-slate-900/40 rounded-xl border border-slate-800/60">
                    {evalResult.disclaimer}
                  </div>
                )}
              </>
            ) : (
              <div className="bg-slate-900/50 border border-slate-800/80 rounded-2xl p-12 text-center flex flex-col items-center justify-center">
                <ShieldCheck className="w-12 h-12 text-slate-600 mb-3" />
                <h4 className="text-white font-medium">No Evaluation Executed Yet</h4>
                <p className="text-xs text-slate-400 max-w-sm mt-1">
                  Adjust parameter sliders on the left or select a scenario preset, then click "Run Forward-Chaining Inference".
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 3: RULEBASE DIRECTORY */}
      {activeTab === 'rulebase' && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h3 className="text-base font-semibold text-white">Production Rule Knowledge Base</h3>
              <p className="text-xs text-slate-400">
                Formal IF-THEN rules with priority ordering and safety-critical overrides.
              </p>
            </div>
            <span className="text-xs font-mono text-cyan-400 bg-cyan-950/40 border border-cyan-800/50 px-3 py-1 rounded-full">
              9 Active Production Rules
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { id: "R01", name: "Thermal Runaway Prevention", sev: "CRITICAL", if: "T_max >= 42.0°C", then: "Emergency load disconnect & activate maximum auxiliary cooling", act: "EMERGENCY_COOLING_DISCONNECT" },
              { id: "R02", name: "High Temperature Warning", sev: "WARNING", if: "39.5°C <= T_max < 42.0°C", then: "Throttle charge rate to 0.5C and inspect cooling fan circulation", act: "THROTTLE_CHARGE_RATE" },
              { id: "R03", name: "End of Life (EOL) Replacement", sev: "CRITICAL", if: "SOH <= 70.0% OR RUL <= 10 cycles", then: "Decommission cell immediately; schedule physical cell replacement", act: "REPLACE_CELL_IMMEDIATE" },
              { id: "R04", name: "Degraded Capacity Warning", sev: "WARNING", if: "70.0% < SOH <= 80.0%", then: "Flag for preventive maintenance; restrict high-rate discharge", act: "FLAG_PREVENTIVE_MAINTENANCE" },
              { id: "R05", name: "Severe Impedance Growth", sev: "CRITICAL", if: "internal_impedance >= 0.170 Ω", then: "Electrolyte reconditioning or cell retirement required", act: "ELECTROLYTE_RECONDITION_OR_REPLACE" },
              { id: "R06", name: "Moderate Impedance Rise", sev: "WARNING", if: "0.145 Ω <= internal_impedance < 0.170 Ω", then: "Schedule full Electrochemical Impedance Spectroscopy (EIS) sweep", act: "SCHEDULE_EIS_DIAGNOSTICS" },
              { id: "R07", name: "Accelerated Capacity Fade", sev: "WARNING", if: "recent_soh_drop >= 1.5%", then: "Perform cell rebalancing and log non-linear degradation", act: "PERFORM_CELL_REBALANCING" },
              { id: "R08", name: "Under-Voltage Deep Discharge", sev: "CRITICAL", if: "V_min <= 2.20 V", then: "Copper dissolution risk; disconnect load and perform gentle recharge", act: "PREVENT_DEEP_DISCHARGE" },
              { id: "R09", name: "Nominal Operating State", sev: "INFO", if: "All parameters within normal operating envelope", then: "Continue standard cycle logging; no intervention needed", act: "CONTINUE_NORMAL_OPERATION" }
            ].map((rule) => (
              <div 
                key={rule.id} 
                className="bg-slate-950 p-4 rounded-xl border border-slate-800 hover:border-slate-700 transition-all space-y-2"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-white bg-slate-800 px-2 py-0.5 rounded">
                      {rule.id}
                    </span>
                    <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                      rule.sev === 'CRITICAL' 
                        ? 'bg-rose-500/20 text-rose-400' 
                        : rule.sev === 'WARNING' 
                        ? 'bg-amber-500/20 text-amber-400' 
                        : 'bg-emerald-500/20 text-emerald-400'
                    }`}>
                      {rule.sev}
                    </span>
                  </div>
                  <span className="text-xs font-mono text-cyan-400">
                    {rule.act}
                  </span>
                </div>

                <div className="text-xs font-semibold text-slate-200">{rule.name}</div>

                <div className="text-xs text-slate-300 font-mono bg-slate-900 p-2 rounded border border-slate-800/80">
                  IF {rule.if}
                </div>

                <div className="text-xs text-slate-400">
                  <span className="text-slate-500 font-medium">THEN:</span> {rule.then}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
