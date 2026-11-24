import React, { useState, useEffect } from 'react';
import { Tags, ShieldCheck, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { api } from '../services/api';

export default function ClassificationAnalysis() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    api.getClassificationMetrics()
      .then(setMetrics)
      .catch(console.error);
  }, []);

  const modelsBenchmark = metrics ? [
    {
      name: 'Decision Tree',
      accuracy: (metrics.Decision_Tree?.Accuracy * 100).toFixed(1),
      macroF1: metrics.Decision_Tree?.F1_Macro.toFixed(3),
      logLoss: metrics.Decision_Tree?.Log_Loss?.toFixed(2) || 'N/A'
    },
    {
      name: 'Support Vector Machine',
      accuracy: (metrics.Support_Vector_Machine?.Accuracy * 100).toFixed(1),
      macroF1: metrics.Support_Vector_Machine?.F1_Macro.toFixed(3),
      logLoss: metrics.Support_Vector_Machine?.Log_Loss?.toFixed(2) || 'N/A'
    },
    {
      name: 'Gaussian Naive Bayes',
      accuracy: (metrics.Naive_Bayes?.Accuracy * 100).toFixed(1),
      macroF1: metrics.Naive_Bayes?.F1_Macro.toFixed(3),
      logLoss: metrics.Naive_Bayes?.Log_Loss?.toFixed(2) || 'N/A'
    },
    {
      name: 'K-Nearest Neighbors',
      accuracy: (metrics.K_Nearest_Neighbors?.Accuracy * 100).toFixed(1),
      macroF1: metrics.K_Nearest_Neighbors?.F1_Macro.toFixed(3),
      logLoss: metrics.K_Nearest_Neighbors?.Log_Loss?.toFixed(2) || 'N/A'
    }
  ] : [];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Tags className="w-5 h-5 text-cyan-400" />
          Practical 4: Battery Condition Classification
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Multi-class evaluation predicting 4 condition categories (Healthy, Moderate, Degraded, Critical)
          on unseen test cell B0018 across SVM, Decision Tree, KNN, and Gaussian Naive Bayes.
        </p>
      </div>

      {/* Models Benchmark Table */}
      <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
        <h3 className="text-sm font-semibold text-white mb-3">
          Classification Performance Comparison (Test Cell B0018)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-[11px] text-slate-400 border-b border-navy-800 font-mono">
              <tr>
                <th className="py-2.5">Classifier</th>
                <th className="py-2.5">Accuracy</th>
                <th className="py-2.5">Macro F1-Score</th>
                <th className="py-2.5">Log Loss</th>
                <th className="py-2.5">Academic Evaluation Notes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-navy-800/60 font-mono">
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-cyan-400 font-sans">Decision Tree Classifier</td>
                <td className="py-2.5 text-emerald-400 font-bold">71.97 %</td>
                <td className="py-2.5 text-white font-bold">0.6090</td>
                <td className="py-2.5 text-slate-300">10.11</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">Rank 1 (Best Accuracy) • Orthogonal splits handle non-linear wear</td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-slate-200 font-sans">Support Vector Machine (SVM)</td>
                <td className="py-2.5 text-white">61.36 %</td>
                <td className="py-2.5 text-slate-300">0.5257</td>
                <td className="py-2.5 text-emerald-400 font-bold">1.226 (Best Calibration)</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">Rank 2 • Platt scaling yields smooth, calibrated probabilities</td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-slate-200 font-sans">Gaussian Naive Bayes</td>
                <td className="py-2.5 text-white">57.58 %</td>
                <td className="py-2.5 text-slate-300">0.4977</td>
                <td className="py-2.5 text-slate-300">9.62</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">Rank 3 • Fast generative baseline assuming independent features</td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 font-bold text-slate-400 font-sans">K-Nearest Neighbors (KNN)</td>
                <td className="py-2.5 text-slate-400">38.64 %</td>
                <td className="py-2.5 text-slate-400">0.2986</td>
                <td className="py-2.5 text-rose-400">17.44</td>
                <td className="py-2.5 font-sans text-slate-400 text-[11px]">Rank 4 • Vulnerable to global baseline DC shifts across different physical cells</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Bar Chart Comparison */}
      <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
        <h4 className="text-xs font-semibold text-white uppercase tracking-wider mb-2">
          Model Comparison: Accuracy vs Macro F1-Score
        </h4>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={modelsBenchmark}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }} />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <Bar dataKey="accuracy" fill="#06b6d4" name="Accuracy (%)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
