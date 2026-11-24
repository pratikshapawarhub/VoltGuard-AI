import React, { useState } from 'react';
import {
  Sparkles,
  CheckCircle,
  AlertTriangle,
  Clock,
  Layers,
  PieChart,
  ShieldAlert,
  ArrowRight,
  TrendingDown
} from 'lucide-react';
import BatteryInputForm from '../components/BatteryInputForm';
import { api } from '../services/api';

export default function BatteryHealthPrediction() {
  const [predictionResult, setPredictionResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async (formData) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await api.runIntegratedEngine(formData);
      setPredictionResult(result);
    } catch (err) {
      setError(err.message || 'Prediction failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCsvUpload = async (file) => {
    setIsLoading(true);
    setError(null);
    try {
      const uploadResp = await api.uploadCsv(file);
      if (uploadResp.preview && uploadResp.preview.length > 0) {
        // Run prediction on first row of CSV
        const firstRow = uploadResp.preview[0];
        const formatted = {
          battery_id: firstRow.battery_id || 'CSV_BATCH_01',
          cycle_number: parseInt(firstRow.cycle_number) || 1,
          voltage_mean: parseFloat(firstRow.voltage_mean) || 3.5,
          voltage_max: parseFloat(firstRow.voltage_max) || 4.19,
          voltage_min: parseFloat(firstRow.voltage_min) || 2.4,
          voltage_std: parseFloat(firstRow.voltage_std) || 0.24,
          current_mean: parseFloat(firstRow.current_mean) || 1.84,
          current_std: parseFloat(firstRow.current_std) || 0.52,
          temperature_mean: parseFloat(firstRow.temperature_mean) || 32.5,
          temperature_max: parseFloat(firstRow.temperature_max) || 39.5,
          temperature_min: parseFloat(firstRow.temperature_min) || 24.0,
          charge_duration: parseFloat(firstRow.charge_duration) || 10400.0,
          discharge_duration: parseFloat(firstRow.discharge_duration) || 3100.0,
          internal_impedance: parseFloat(firstRow.internal_impedance) || 0.14,
          recent_soh_drop: 0.5
        };
        await handlePredict(formatted);
      }
    } catch (err) {
      setError(err.message || 'Failed to process CSV');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          Predictive Intelligence Engine
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Executes end-to-end multi-model inference combining SOH/RUL regression, condition classification,
          ensemble consensus, usage clustering, expert system rules, and A* maintenance planning.
        </p>
      </div>

      {/* Input Form */}
      <BatteryInputForm
        onSubmit={handlePredict}
        isLoading={isLoading}
        onFileUpload={handleCsvUpload}
      />

      {error && (
        <div className="p-3 bg-rose-500/10 border border-rose-500/25 rounded-lg text-rose-300 text-xs flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      {/* Prediction Output Results */}
      {predictionResult && (
        <div className="space-y-6 animate-fadeIn">
          {/* Main Prognostic KPI Row */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* SOH */}
            <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Predicted State of Health (SOH)
              </span>
              <div className="mt-2 flex items-baseline gap-1">
                <span className="text-3xl font-extrabold text-cyan-400">
                  {predictionResult.soh_prediction.recommended_soh}%
                </span>
              </div>
              <div className="mt-2 text-[10px] text-slate-400 space-y-0.5 font-mono">
                <div>Linear Reg: {predictionResult.soh_prediction.soh_sklearn_lr}%</div>
                <div>Manual GD: {predictionResult.soh_prediction.soh_manual_gd}%</div>
                <div>Random Forest: {predictionResult.soh_prediction.soh_random_forest}%</div>
              </div>
            </div>

            {/* RUL */}
            <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Remaining Useful Life (RUL)
              </span>
              <div className="mt-2 flex items-baseline gap-1">
                <span className="text-3xl font-extrabold text-purple-400">
                  {predictionResult.rul_prediction.recommended_rul}
                </span>
                <span className="text-xs text-slate-400 ml-1">cycles</span>
              </div>
              <p className="mt-2 text-[10px] text-slate-400 font-mono">
                Until 70% SOH (1.40 Ahr) EOL threshold
              </p>
            </div>

            {/* Condition Classification */}
            <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Condition Classification
              </span>
              <div className="mt-2">
                <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                  predictionResult.condition_classification.predicted_category === 'Healthy' ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30' :
                  predictionResult.condition_classification.predicted_category === 'Moderate' ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30' :
                  predictionResult.condition_classification.predicted_category === 'Degraded' ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30' :
                  'bg-rose-500/15 text-rose-300 border border-rose-500/30'
                }`}>
                  {predictionResult.condition_classification.predicted_category}
                </span>
              </div>
              <p className="mt-3 text-[10px] text-slate-400 font-mono">
                Ensemble: {predictionResult.ensemble_classification.consensus_category}
              </p>
            </div>

            {/* Learned Cluster */}
            <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Usage Cluster Segment
              </span>
              <div className="mt-2 text-sm font-semibold text-slate-200 truncate">
                {predictionResult.usage_clustering.cluster_name}
              </div>
              <p className="mt-1 text-[11px] text-slate-400 line-clamp-2">
                {predictionResult.usage_clustering.description}
              </p>
            </div>
          </div>

          {/* Expert System Rules Triggered & Action Recommendations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
              <div className="flex items-center justify-between pb-3 border-b border-navy-800">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-amber-400" />
                  Practical 1: Rule-Based Expert System Audit
                </h3>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                  predictionResult.expert_system.overall_status === 'HEALTHY' ? 'bg-emerald-500/20 text-emerald-300' :
                  predictionResult.expert_system.overall_status === 'WARNING' ? 'bg-amber-500/20 text-amber-300' :
                  'bg-rose-500/20 text-rose-300'
                }`}>
                  STATUS: {predictionResult.expert_system.overall_status}
                </span>
              </div>

              <p className="mt-3 text-xs text-slate-300">
                {predictionResult.expert_system.condition_summary}
              </p>

              <div className="mt-4 space-y-2">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  Triggered IF-THEN Rules ({predictionResult.expert_system.triggered_rules_count})
                </span>
                {predictionResult.expert_system.triggered_rules.map((rule, idx) => (
                  <div key={idx} className="p-2.5 rounded bg-navy-850 border border-navy-750 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-white">{rule.name}</span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
                        rule.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300' :
                        rule.severity === 'WARNING' ? 'bg-amber-500/20 text-amber-300' :
                        'bg-emerald-500/20 text-emerald-300'
                      }`}>
                        {rule.severity}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 mt-1">{rule.description}</p>
                    <p className="text-[11px] text-cyan-300 mt-1 font-mono">Action: {rule.action_code}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Practical 2: A* Search Optimal Maintenance Trajectory */}
            <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
              <div className="flex items-center justify-between pb-3 border-b border-navy-800">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <ArrowRight className="w-4 h-4 text-cyan-400" />
                  Practical 2: Optimal Servicing Trajectory (A* Search)
                </h3>
                <span className="text-[10px] text-cyan-400 font-mono bg-navy-800 px-2 py-0.5 rounded border border-navy-700">
                  Total Cost: ${predictionResult.optimal_maintenance_plan.total_cost}
                </span>
              </div>

              <div className="mt-3 text-xs text-slate-300">
                <span>Algorithm: </span>
                <strong className="text-white">{predictionResult.optimal_maintenance_plan.algorithm}</strong>
                <span className="text-slate-400 ml-2">({predictionResult.optimal_maintenance_plan.optimality})</span>
              </div>

              {/* Step Flow */}
              <div className="mt-4 space-y-2">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  Service Step Transitions ({predictionResult.optimal_maintenance_plan.steps} steps)
                </span>
                <div className="space-y-1.5 font-mono text-xs">
                  {predictionResult.optimal_maintenance_plan.path.map((step, idx) => (
                    <div key={idx} className="flex items-center gap-2 p-2 bg-navy-850 rounded border border-navy-750">
                      <span className="w-5 h-5 flex items-center justify-center rounded-full bg-cyan-500/20 text-cyan-300 text-[10px]">
                        {idx + 1}
                      </span>
                      <span className="text-slate-200 font-semibold">{step}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mt-4 p-3 rounded-lg bg-navy-950 border border-navy-800 text-[11px] text-slate-400">
                <span>Recommendations Checklist:</span>
                <ul className="list-disc list-inside mt-1 space-y-1 text-slate-300">
                  {predictionResult.expert_system.recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
