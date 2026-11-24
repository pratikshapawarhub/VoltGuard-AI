import React, { useState, useEffect } from 'react';
import { TrendingDown, Award, BarChart2 } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { api } from '../services/api';

export default function RegressionAnalysis() {
  const [metrics, setMetrics] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.getRegressionMetrics()
      .then((data) => {
      setMetrics(data);
      setIsLoading(false);
    }).catch(err => {
      console.error(err);
      setIsLoading(false);
    });
  }, []);

  const sohComparisonData = metrics?.SOH_Prediction ? [
    {
      model: 'Manual GD',
      MAE: metrics.SOH_Prediction.Manual_Gradient_Descent.MAE,
      RMSE: metrics.SOH_Prediction.Manual_Gradient_Descent.RMSE,
      R2: metrics.SOH_Prediction.Manual_Gradient_Descent.R2_Score
    },
    {
      model: 'Sklearn LR',
      MAE: metrics.SOH_Prediction.Sklearn_Linear_Regression.MAE,
      RMSE: metrics.SOH_Prediction.Sklearn_Linear_Regression.RMSE,
      R2: metrics.SOH_Prediction.Sklearn_Linear_Regression.R2_Score
    },
    {
      model: 'Random Forest',
      MAE: metrics.SOH_Prediction.Random_Forest_Regressor.MAE,
      RMSE: metrics.SOH_Prediction.Random_Forest_Regressor.RMSE,
      R2: metrics.SOH_Prediction.Random_Forest_Regressor.R2_Score
    }
  ] : [];

  const rulComparisonData = metrics?.RUL_Prediction ? [
    {
      model: 'Manual GD',
      MAE: metrics.RUL_Prediction.Manual_Gradient_Descent.MAE,
      RMSE: metrics.RUL_Prediction.Manual_Gradient_Descent.RMSE,
      R2: metrics.RUL_Prediction.Manual_Gradient_Descent.R2_Score
    },
    {
      model: 'Sklearn LR',
      MAE: metrics.RUL_Prediction.Sklearn_Linear_Regression.MAE,
      RMSE: metrics.RUL_Prediction.Sklearn_Linear_Regression.RMSE,
      R2: metrics.RUL_Prediction.Sklearn_Linear_Regression.R2_Score
    },
    {
      model: 'Random Forest',
      MAE: metrics.RUL_Prediction.Random_Forest_Regressor.MAE,
      RMSE: metrics.RUL_Prediction.Random_Forest_Regressor.RMSE,
      R2: metrics.RUL_Prediction.Random_Forest_Regressor.R2_Score
    }
  ] : [];

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <TrendingDown className="w-5 h-5 text-cyan-400" />
          Practical 3: Regression Model Evaluation
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Comparative analysis between Manual Gradient Descent (from scratch), Scikit-learn Linear Regression,
          and Random Forest Regressor on unseen NASA test cell B0018.
        </p>
      </div>

      {/* SOH Evaluation Table */}
      <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
        <h3 className="text-sm font-semibold text-white mb-3">
          State of Health (SOH %) Prediction Benchmark (Test Cell B0018)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-[11px] text-slate-400 border-b border-navy-800 font-mono">
              <tr>
                <th className="py-2.5">Regression Model</th>
                <th className="py-2.5">Mean Absolute Error (MAE)</th>
                <th className="py-2.5">Mean Squared Error (MSE)</th>
                <th className="py-2.5">Root Mean Squared Error (RMSE)</th>
                <th className="py-2.5">R² Score</th>
                <th className="py-2.5">Rank</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-navy-800/60 font-mono">
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-cyan-400 font-sans">Scikit-learn Linear Regression</td>
                <td className="py-2.5 text-white">0.3397 %</td>
                <td className="py-2.5 text-slate-300">0.1930</td>
                <td className="py-2.5 text-slate-300">0.4394 %</td>
                <td className="py-2.5 text-emerald-400 font-bold">0.9968</td>
                <td className="py-2.5"><span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-sans text-[10px]">Rank 1 (Best)</span></td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-amber-400 font-sans">Manual Gradient Descent (from scratch)</td>
                <td className="py-2.5 text-white">1.7599 %</td>
                <td className="py-2.5 text-slate-300">3.3991</td>
                <td className="py-2.5 text-slate-300">1.8437 %</td>
                <td className="py-2.5 text-cyan-300 font-bold">0.9429</td>
                <td className="py-2.5"><span className="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-sans text-[10px]">Rank 2</span></td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-slate-200 font-sans">Random Forest Regressor</td>
                <td className="py-2.5 text-white">2.2595 %</td>
                <td className="py-2.5 text-slate-300">7.8269</td>
                <td className="py-2.5 text-slate-300">2.7977 %</td>
                <td className="py-2.5 text-slate-300 font-bold">0.8685</td>
                <td className="py-2.5"><span className="px-2 py-0.5 rounded bg-navy-800 text-slate-400 font-sans text-[10px]">Rank 3</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* RUL Evaluation Table */}
      <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
        <h3 className="text-sm font-semibold text-white mb-3">
          Remaining Useful Life (RUL Cycles) Prediction Benchmark (Test Cell B0018)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-[11px] text-slate-400 border-b border-navy-800 font-mono">
              <tr>
                <th className="py-2.5">Regression Model</th>
                <th className="py-2.5">MAE (Cycles)</th>
                <th className="py-2.5">MSE</th>
                <th className="py-2.5">RMSE (Cycles)</th>
                <th className="py-2.5">R² Score</th>
                <th className="py-2.5">Rank</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-navy-800/60 font-mono">
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-amber-400 font-sans">Manual Gradient Descent (from scratch)</td>
                <td className="py-2.5 text-white font-bold">18.37 cycles</td>
                <td className="py-2.5 text-slate-300">423.12</td>
                <td className="py-2.5 text-slate-300">20.57 cycles</td>
                <td className="py-2.5 text-emerald-400 font-bold">0.5872</td>
                <td className="py-2.5"><span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-sans text-[10px]">Rank 1 (Best)</span></td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-slate-200 font-sans">Random Forest Regressor</td>
                <td className="py-2.5 text-white">19.47 cycles</td>
                <td className="py-2.5 text-slate-300">485.44</td>
                <td className="py-2.5 text-slate-300">22.03 cycles</td>
                <td className="py-2.5 text-cyan-300 font-bold">0.5264</td>
                <td className="py-2.5"><span className="px-2 py-0.5 rounded bg-cyan-500/20 text-cyan-300 font-sans text-[10px]">Rank 2</span></td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-slate-400 font-sans">Scikit-learn Linear Regression</td>
                <td className="py-2.5 text-white">27.95 cycles</td>
                <td className="py-2.5 text-slate-300">970.54</td>
                <td className="py-2.5 text-slate-300">31.15 cycles</td>
                <td className="py-2.5 text-slate-400 font-bold">0.0532</td>
                <td className="py-2.5"><span className="px-2 py-0.5 rounded bg-navy-800 text-slate-400 font-sans text-[10px]">Rank 3</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Visual Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
          <h4 className="text-xs font-semibold text-white uppercase tracking-wider mb-2">
            SOH Model Comparison: R² Score
          </h4>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sohComparisonData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="model" stroke="#64748b" fontSize={11} />
                <YAxis domain={[0.8, 1.02]} stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }} />
                <Bar dataKey="R2" fill="#06b6d4" name="R² Score" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
          <h4 className="text-xs font-semibold text-white uppercase tracking-wider mb-2">
            RUL Model Comparison: MAE in Cycles (Lower is better)
          </h4>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={rulComparisonData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="model" stroke="#64748b" fontSize={11} />
                <YAxis domain={[0, 35]} stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }} />
                <Bar dataKey="MAE" fill="#a855f7" name="MAE (Cycles)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
