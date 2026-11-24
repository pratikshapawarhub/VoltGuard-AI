import React, { useState, useEffect } from 'react';
import { PieChart, TrendingDown, Target } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { api } from '../services/api';

export default function BatteryClustering() {
  const [metrics, setMetrics] = useState(null);
  const [elbowData, setElbowData] = useState([]);

  useEffect(() => {
    Promise.all([
      api.getClusteringMetrics().catch(() => null),
      api.getElbowCurve().catch(() => null)
    ]).then(([metricsData, elbowResp]) => {
      setMetrics(metricsData);
      if (elbowResp?.k_values) {
        const formatted = elbowResp.k_values.map((k, i) => ({
          k,
          wcss: elbowResp.wcss[i],
          silhouette: elbowResp.silhouette_scores[i]
        }));
        setElbowData(formatted);
      }
    });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <PieChart className="w-5 h-5 text-cyan-400" />
          Battery Usage Segmentation & Regime Discovery
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Unsupervised K-Means clustering discovering latent battery operational regimes without predefined labels.
          Evaluated via WCSS (Inertia), Silhouette Score, and Davies-Bouldin Index.
        </p>
      </div>

      {/* Discovered Cluster Profiles Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {metrics?.Cluster_Profiles && Object.entries(metrics.Cluster_Profiles).map(([cId, prof]) => (
          <div key={cId} className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
            <div className="flex items-center justify-between pb-2 border-b border-navy-800">
              <span className="text-xs font-mono font-bold text-cyan-400">Cluster {cId}</span>
              <span className="text-[10px] bg-navy-800 text-slate-300 font-mono px-2 py-0.5 rounded">
                {prof.percentage}% ({prof.sample_count} cycles)
              </span>
            </div>
            <h4 className="text-sm font-semibold text-white mt-3">{prof.cluster_name}</h4>
            <p className="text-xs text-slate-400 mt-1">{prof.description}</p>

            <div className="mt-4 pt-3 border-t border-navy-800 text-xs font-mono space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-400">Mean SOH:</span>
                <span className="text-cyan-300 font-semibold">{prof.means.soh}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Internal Impedance:</span>
                <span className="text-slate-200">{prof.means.internal_impedance} Ω</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Peak Discharge Temp:</span>
                <span className="text-amber-300">{prof.means.temperature_max} °C</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Mean Cycle Age:</span>
                <span className="text-purple-300">Cycle {prof.means.cycle_number}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Diagnostics Dual Plot */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Elbow WCSS */}
        <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
          <h4 className="text-xs font-semibold text-white uppercase tracking-wider mb-2">
            Elbow Method: WCSS / Inertia (Lower is better)
          </h4>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={elbowData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="k" stroke="#64748b" fontSize={11} label={{ value: 'Number of Clusters (K)', position: 'insideBottom', offset: -5 }} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }} />
                <Line type="monotone" dataKey="wcss" stroke="#06b6d4" strokeWidth={2} dot={{ r: 4 }} name="WCSS / Inertia" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Silhouette Scores */}
        <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
          <h4 className="text-xs font-semibold text-white uppercase tracking-wider mb-2">
            Silhouette Score vs K (Higher is better)
          </h4>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={elbowData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="k" stroke="#64748b" fontSize={11} label={{ value: 'Number of Clusters (K)', position: 'insideBottom', offset: -5 }} />
                <YAxis domain={[0.2, 0.5]} stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }} />
                <Line type="monotone" dataKey="silhouette" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} name="Silhouette Score" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
