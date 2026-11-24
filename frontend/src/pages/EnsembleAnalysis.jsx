import React, { useState, useEffect } from 'react';
import { Layers, Award, CheckCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { api } from '../services/api';

export default function EnsembleAnalysis() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    api.getEnsembleMetrics()
      .then(setMetrics)
      .catch(console.error);
  }, []);

  const benchmarkData = [
    { model: 'Decision Tree', type: 'Base', accuracy: 71.97, macroF1: 0.609 },
    { model: 'Stacking Ensemble', type: 'Ensemble', accuracy: 71.97, macroF1: 0.609 },
    { model: 'AdaBoost Ensemble', type: 'Ensemble', accuracy: 68.18, macroF1: 0.564 },
    { model: 'SVM', type: 'Base', accuracy: 61.36, macroF1: 0.526 },
    { model: 'Hard Voting', type: 'Ensemble', accuracy: 61.36, macroF1: 0.526 },
    { model: 'Naive Bayes', type: 'Base', accuracy: 57.58, macroF1: 0.498 },
    { model: 'KNN', type: 'Base', accuracy: 38.64, macroF1: 0.299 }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-cyan-400" />
          Practical 5: Ensemble Learning & Performance Evaluation
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Benchmarking Stacking (with 5-fold out-of-fold Logistic Regression meta-classifier), AdaBoost,
          and Hard Voting against all 4 base models on unseen cell B0018.
        </p>
      </div>

      {/* 7-Model Benchmark Table */}
      <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
        <h3 className="text-sm font-semibold text-white mb-3">
          Comprehensive 7-Model Performance Comparison (Test Cell B0018)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="text-[11px] text-slate-400 border-b border-navy-800 font-mono">
              <tr>
                <th className="py-2.5">Paradigm</th>
                <th className="py-2.5">Model Name</th>
                <th className="py-2.5">Accuracy</th>
                <th className="py-2.5">Macro F1-Score</th>
                <th className="py-2.5">Log Loss</th>
                <th className="py-2.5">Theoretical Performance Explanation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-navy-800/60 font-mono">
              <tr className="hover:bg-navy-850/50 bg-cyan-500/5">
                <td className="py-2.5 text-cyan-300 font-sans font-bold">Ensemble</td>
                <td className="py-2.5 font-bold text-cyan-400 font-sans">Stacking Ensemble</td>
                <td className="py-2.5 text-emerald-400 font-bold">71.97 %</td>
                <td className="py-2.5 text-white font-bold">0.6090</td>
                <td className="py-2.5 text-emerald-400 font-bold">1.1602 (Lowest Log Loss!)</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">
                  Meta-classifier smoothly calibrates class probabilities using 5-fold out-of-fold CV
                </td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 text-slate-400 font-sans">Base</td>
                <td className="py-2.5 font-bold text-white font-sans">Decision Tree Classifier</td>
                <td className="py-2.5 text-emerald-400 font-bold">71.97 %</td>
                <td className="py-2.5 text-white font-bold">0.6090</td>
                <td className="py-2.5 text-slate-300">10.1054</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">
                  High accuracy but uncalibrated step-function probabilities at leaf nodes
                </td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 text-cyan-300 font-sans font-bold">Ensemble</td>
                <td className="py-2.5 font-bold text-slate-200 font-sans">AdaBoost Ensemble</td>
                <td className="py-2.5 text-white">68.18 %</td>
                <td className="py-2.5 text-slate-300">0.5636</td>
                <td className="py-2.5 text-slate-300">1.2292</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">
                  Iterative boosting focuses on misclassified boundary transitions
                </td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 text-slate-400 font-sans">Base</td>
                <td className="py-2.5 font-bold text-slate-200 font-sans">Support Vector Machine (SVM)</td>
                <td className="py-2.5 text-white">61.36 %</td>
                <td className="py-2.5 text-slate-300">0.5257</td>
                <td className="py-2.5 text-slate-300">1.2260</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">
                  Strong probability calibration via Platt scaling
                </td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 text-cyan-300 font-sans font-bold">Ensemble</td>
                <td className="py-2.5 font-bold text-slate-300 font-sans">Hard Voting Ensemble</td>
                <td className="py-2.5 text-white">61.36 %</td>
                <td className="py-2.5 text-slate-300">0.5257</td>
                <td className="py-2.5 text-slate-400">N/A (Hard)</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">
                  Democratic voting degrades because poor KNN accuracy pulls down consensus
                </td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 text-slate-400 font-sans">Base</td>
                <td className="py-2.5 font-bold text-slate-400 font-sans">Gaussian Naive Bayes</td>
                <td className="py-2.5 text-slate-300">57.58 %</td>
                <td className="py-2.5 text-slate-400">0.4977</td>
                <td className="py-2.5 text-slate-400">9.6157</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">
                  Fast generative model; independence assumption partially violated
                </td>
              </tr>
              <tr className="hover:bg-navy-850/50">
                <td className="py-2.5 text-slate-400 font-sans">Base</td>
                <td className="py-2.5 font-bold text-slate-400 font-sans">K-Nearest Neighbors</td>
                <td className="py-2.5 text-slate-400">38.64 %</td>
                <td className="py-2.5 text-slate-400">0.2986</td>
                <td className="py-2.5 text-rose-400">17.4397</td>
                <td className="py-2.5 font-sans text-slate-300 text-[11px]">
                  Severe domain shift across different battery packs degrades nearest-neighbor lookups
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Benchmark Chart */}
      <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
        <h4 className="text-xs font-semibold text-white uppercase tracking-wider mb-2">
          7-Model Benchmark: Accuracy Comparison
        </h4>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={benchmarkData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="model" stroke="#64748b" fontSize={10.5} />
              <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }} />
              <Bar dataKey="accuracy" fill="#06b6d4" name="Accuracy (%)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
