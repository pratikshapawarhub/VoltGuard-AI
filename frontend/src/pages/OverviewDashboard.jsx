import React, { useState, useEffect } from 'react';
import {
  Activity,
  Boxes,
  AlertTriangle,
  AlertOctagon,
  Clock,
  Layers,
  TrendingDown,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Calendar,
  Cpu,
  RefreshCw,
  Zap,
  Battery
} from 'lucide-react';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell, Legend
} from 'recharts';
import KPICard from '../components/KPICard';
import { api } from '../services/api';

export default function OverviewDashboard({ onNavigate }) {
  const [fleetOverview, setFleetOverview] = useState(null);
  const [activeAlerts, setActiveAlerts] = useState([]);
  const [maintenanceTasks, setMaintenanceTasks] = useState([]);
  const [recentHistory, setRecentHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      const [overviewData, alertsData, tasksData, historyData] = await Promise.all([
        api.getFleetOverview().catch(() => null),
        api.listAlerts('ACTIVE', null, null, 4).catch(() => []),
        api.listMaintenanceTasks('SCHEDULED', null, null).catch(() => []),
        api.getPredictionHistory(5).catch(() => [])
      ]);

      setFleetOverview(overviewData);
      setActiveAlerts(alertsData);
      setMaintenanceTasks(tasksData.slice(0, 4));
      setRecentHistory(historyData);
    } catch (err) {
      console.error("Dashboard data load error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const healthDistData = fleetOverview?.health_distribution
    ? [
        { name: 'Healthy', count: fleetOverview.health_distribution.Healthy || 0, color: '#10b981' },
        { name: 'Moderate', count: fleetOverview.health_distribution.Moderate || 0, color: '#06b6d4' },
        { name: 'Degraded', count: fleetOverview.health_distribution.Degraded || 0, color: '#fbbf24' },
        { name: 'Critical', count: fleetOverview.health_distribution.Critical || 0, color: '#f43f5e' }
      ]
    : [];

  const degradationCurves = [
    { cycle: 10, B0005: 93.1, B0006: 101.2, B0007: 94.2, B0018: 92.5 },
    { cycle: 30, B0005: 91.5, B0006: 98.4, B0007: 92.0, B0018: 90.1 },
    { cycle: 60, B0005: 88.2, B0006: 91.0, B0007: 89.1, B0018: 85.4 },
    { cycle: 90, B0005: 84.1, B0006: 82.5, B0007: 85.2, B0018: 73.2 },
    { cycle: 120, B0005: 78.4, B0006: 72.1, B0007: 80.4, B0018: 68.1 },
    { cycle: 150, B0005: 71.0, B0006: 62.5, B0007: 74.2, B0018: 66.5 }
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-navy-900 to-navy-850 border border-navy-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 text-xs font-mono mb-3">
            <span>NASA Li-ion Prognostics Benchmark • 636 Physical Cycles</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Commercial Battery Health & Predictive Maintenance Platform
          </h2>
          <p className="mt-2 text-xs text-slate-300 leading-relaxed">
            VoltGuard AI provides end-to-end prognostic intelligence for mission-critical lithium-ion energy assets.
            Integrating physical degradation modeling, multi-model SOH regression, multi-class condition classification,
            unsupervised usage clustering, and heuristic A* maintenance planning.
          </p>

          <div className="mt-4 flex flex-wrap gap-3">
            <button
              onClick={() => onNavigate('prediction')}
              className="flex items-center gap-2 px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-navy-950 font-bold text-xs rounded-xl transition cursor-pointer shadow-lg"
            >
              <Cpu className="w-4 h-4" />
              <span>Predictive Intelligence Engine</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onNavigate('assets')}
              className="px-4 py-2 bg-navy-800 hover:bg-navy-750 text-slate-200 text-xs font-semibold rounded-xl border border-navy-700 transition cursor-pointer flex items-center gap-1.5"
            >
              <Boxes className="w-3.5 h-3.5 text-cyan-400" />
              <span>Asset Registry ({fleetOverview?.total_batteries || 5} units)</span>
            </button>
            <button
              onClick={() => onNavigate('maintenance')}
              className="px-4 py-2 bg-navy-800 hover:bg-navy-750 text-slate-200 text-xs font-semibold rounded-xl border border-navy-700 transition cursor-pointer flex items-center gap-1.5"
            >
              <Calendar className="w-3.5 h-3.5 text-amber-400" />
              <span>Maintenance Center</span>
            </button>
          </div>
        </div>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Registered Assets</span>
          <span className="text-2xl font-bold text-white font-mono mt-1 block">
            {fleetOverview ? fleetOverview.total_batteries : 5}
          </span>
          <span className="text-[10px] text-cyan-400">Total tracked units</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Active Online</span>
          <span className="text-2xl font-bold text-emerald-400 font-mono mt-1 block">
            {fleetOverview ? fleetOverview.active_batteries : 4}
          </span>
          <span className="text-[10px] text-emerald-500">Nominal telemetry</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Attention Required</span>
          <span className="text-2xl font-bold text-amber-400 font-mono mt-1 block">
            {fleetOverview ? fleetOverview.maintenance_batteries : 1}
          </span>
          <span className="text-[10px] text-amber-400">Degraded / Inspection</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Critical EOL</span>
          <span className="text-2xl font-bold text-rose-400 font-mono mt-1 block">
            {fleetOverview ? fleetOverview.critical_alerts_count : 3}
          </span>
          <span className="text-[10px] text-rose-400">Capacity below 70%</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Mean Fleet SOH</span>
          <span className="text-2xl font-bold text-cyan-400 font-mono mt-1 block">
            {fleetOverview ? `${fleetOverview.average_soh}%` : '72.6%'}
          </span>
          <span className="text-[10px] text-slate-400">Degradation index</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
          <span className="text-[10px] text-slate-500 uppercase font-bold block">Mean Fleet RUL</span>
          <span className="text-2xl font-bold text-purple-400 font-mono mt-1 block">
            {fleetOverview ? `${fleetOverview.average_rul}` : '39.8'}
          </span>
          <span className="text-[10px] text-slate-400">Cycles remaining</span>
        </div>
      </div>

      {/* Main Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: SOH Degradation Curves */}
        <div className="lg:col-span-8 bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                <TrendingDown className="w-4 h-4 text-cyan-400" />
                Fleet SOH Degradation Kinetics Across Aging Cycles
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Comparative capacity fade tracking commercial 18650 cells to certified 70% End-of-Life boundary.
              </p>
            </div>
            <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40">
              NASA Ames Benchmark
            </span>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={degradationCurves} margin={{ top: 10, right: 20, left: -10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="cycle" stroke="#64748b" fontSize={11} label={{ value: 'Cycle Count', position: 'insideBottom', offset: -4 }} />
                <YAxis stroke="#64748b" fontSize={11} domain={[50, 105]} />
                <Tooltip contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '12px' }} />
                <Legend />
                <Line type="monotone" dataKey="B0005" stroke="#06b6d4" strokeWidth={2} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="B0006" stroke="#f43f5e" strokeWidth={2} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="B0007" stroke="#10b981" strokeWidth={2} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="B0018" stroke="#a855f7" strokeWidth={2} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right Column: Health State Distribution */}
        <div className="lg:col-span-4 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-semibold text-white mb-1">Fleet Health Distribution</h3>
            <p className="text-xs text-slate-400 mb-4">Discrete degradation categories</p>

            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={healthDistData} layout="vertical" margin={{ top: 0, right: 20, left: 20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                  <XAxis type="number" stroke="#64748b" fontSize={10} />
                  <YAxis type="category" dataKey="name" stroke="#94a3b8" fontSize={11} width={65} />
                  <Tooltip contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '12px' }} />
                  <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                    {healthDistData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-400 pt-3 border-t border-slate-800/80 font-mono">
            <div>Healthy: &ge;90% SOH</div>
            <div>Moderate: 80-90%</div>
            <div>Degraded: 70-80%</div>
            <div>Critical: &lt;70% (EOL)</div>
          </div>
        </div>
      </div>

      {/* Bottom Row: Active Operational Alerts & Scheduled Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Alerts */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              Active Anomaly Alerts ({activeAlerts.length})
            </h3>
            <button
              onClick={() => onNavigate('alerts')}
              className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1"
            >
              Alerts Center <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {activeAlerts.length === 0 ? (
            <div className="p-6 text-center text-xs text-slate-500 bg-slate-950 rounded-xl border border-slate-800">
              No active anomaly alerts. All cells within tolerance.
            </div>
          ) : (
            <div className="space-y-2.5">
              {activeAlerts.map((alert) => (
                <div
                  key={alert.id}
                  className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 hover:border-slate-700 flex items-start justify-between gap-3 text-xs"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        alert.severity === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'
                      }`}>
                        {alert.severity}
                      </span>
                      <span className="font-mono text-cyan-400 font-bold">{alert.battery_id}</span>
                      <span className="text-[10px] text-slate-500">{new Date(alert.created_at).toLocaleTimeString()}</span>
                    </div>
                    <div className="font-semibold text-white">{alert.title}</div>
                    <p className="text-[11px] text-slate-400">{alert.recommendation}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Scheduled Maintenance Tasks */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <Calendar className="w-4 h-4 text-cyan-400" />
              Scheduled Servicing Operations ({maintenanceTasks.length})
            </h3>
            <button
              onClick={() => onNavigate('maintenance')}
              className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1"
            >
              Maintenance Center <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {maintenanceTasks.length === 0 ? (
            <div className="p-6 text-center text-xs text-slate-500 bg-slate-950 rounded-xl border border-slate-800">
              No maintenance work orders currently scheduled.
            </div>
          ) : (
            <div className="space-y-2.5">
              {maintenanceTasks.map((task) => (
                <div
                  key={task.task_id}
                  className="bg-slate-950 p-3.5 rounded-xl border border-slate-800 flex items-center justify-between gap-3 text-xs"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-white bg-slate-800 px-2 py-0.5 rounded text-[10px]">
                        {task.task_id}
                      </span>
                      <span className="font-mono text-cyan-400 font-semibold">{task.battery_id}</span>
                      <span className="text-slate-500 text-[10px] font-mono">{task.scheduled_slot}</span>
                    </div>
                    <div className="text-slate-200 font-medium">{task.title}</div>
                    <div className="text-[10px] text-slate-400">Assigned: {task.technician_name}</div>
                  </div>

                  <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950/40 border border-emerald-800/40 px-2 py-1 rounded">
                    ${task.estimated_cost}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
