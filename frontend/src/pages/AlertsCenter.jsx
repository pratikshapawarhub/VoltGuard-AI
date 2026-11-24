import React, { useState, useEffect } from 'react';
import { 
  Bell, AlertTriangle, AlertOctagon, CheckCircle2, RefreshCw, 
  Filter, Check, Clock, ChevronRight, ShieldAlert, Battery, ArrowRight
} from 'lucide-react';
import { api } from '../services/api';

export default function AlertsCenter({ onNavigate }) {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({ total_alerts: 0, active_alerts: 0, critical_alerts: 0, warning_alerts: 0, resolved_alerts: 0 });
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('ACTIVE');
  const [severityFilter, setSeverityFilter] = useState('ALL');

  useEffect(() => {
    loadAlerts();
  }, [statusFilter, severityFilter]);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const st = statusFilter === 'ALL' ? null : statusFilter;
      const sev = severityFilter === 'ALL' ? null : severityFilter;
      const [alertsData, statsData] = await Promise.all([
        api.listAlerts(st, sev, null, 100),
        api.getAlertStats()
      ]);
      setAlerts(alertsData);
      setStats(statsData);
    } catch (err) {
      console.error("Failed to load alerts:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateStatus = async (alertId, newStatus) => {
    try {
      await api.updateAlertStatus(alertId, newStatus);
      loadAlerts();
    } catch (err) {
      alert(`Failed to update alert: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 text-xs font-semibold tracking-wider uppercase mb-1">
            <Bell className="w-4 h-4" /> Operational Notifications
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Alerts & Anomaly Center
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time thermal risk detections, impedance threshold spikes, accelerated degradation warnings, and deduplicated work orders.
          </p>
        </div>

        <button
          onClick={loadAlerts}
          className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-slate-300 rounded-xl text-xs flex items-center gap-2 self-start md:self-auto border border-slate-800"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} /> Refresh Feed
        </button>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
          <div className="text-[11px] font-semibold text-slate-500 uppercase">Active Alerts</div>
          <div className="text-2xl font-bold text-white font-mono mt-1">{stats.active_alerts}</div>
          <span className="text-[10px] text-cyan-400">Requires operator attention</span>
        </div>

        <div className="bg-slate-900/80 border border-rose-500/20 p-4 rounded-2xl bg-rose-950/10">
          <div className="text-[11px] font-semibold text-rose-400 uppercase">Critical Risks</div>
          <div className="text-2xl font-bold text-rose-400 font-mono mt-1">{stats.critical_alerts}</div>
          <span className="text-[10px] text-rose-300">Runaway / Severe EOL</span>
        </div>

        <div className="bg-slate-900/80 border border-amber-500/20 p-4 rounded-2xl bg-amber-950/10">
          <div className="text-[11px] font-semibold text-amber-400 uppercase">Warnings</div>
          <div className="text-2xl font-bold text-amber-400 font-mono mt-1">{stats.warning_alerts}</div>
          <span className="text-[10px] text-amber-300">Preventive maintenance</span>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl">
          <div className="text-[11px] font-semibold text-slate-500 uppercase">Resolved</div>
          <div className="text-2xl font-bold text-emerald-400 font-mono mt-1">{stats.resolved_alerts}</div>
          <span className="text-[10px] text-emerald-500">Historical closed items</span>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Status Filter */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto">
          <span className="text-xs text-slate-500 font-medium mr-2">Status:</span>
          {['ALL', 'ACTIVE', 'ACKNOWLEDGED', 'RESOLVED'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                statusFilter === st
                  ? 'bg-cyan-500 text-slate-950 shadow-sm'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {st}
            </button>
          ))}
        </div>

        {/* Severity Filter */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto">
          <span className="text-xs text-slate-500 font-medium mr-2">Severity:</span>
          {['ALL', 'CRITICAL', 'WARNING', 'INFO'].map((sev) => (
            <button
              key={sev}
              onClick={() => setSeverityFilter(sev)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                severityFilter === sev
                  ? 'bg-slate-200 text-slate-950 shadow-sm'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {sev}
            </button>
          ))}
        </div>
      </div>

      {/* Alerts Feed */}
      {loading ? (
        <div className="py-16 text-center text-slate-400">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-2 text-cyan-400" />
          <p className="text-xs">Loading operational alerts ledger...</p>
        </div>
      ) : alerts.length === 0 ? (
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-12 text-center">
          <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
          <h3 className="text-white font-semibold text-base">No Operational Alerts Found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1">
            All battery assets are within calibrated operating envelopes under the current filter selection.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {alerts.map((alert) => {
            const isCrit = alert.severity === 'CRITICAL';
            const isWarn = alert.severity === 'WARNING';
            const isResolved = alert.status === 'RESOLVED';
            const isAck = alert.status === 'ACKNOWLEDGED';

            return (
              <div
                key={alert.id}
                className={`p-5 rounded-2xl border transition-all ${
                  isResolved
                    ? 'bg-slate-900/40 border-slate-800/60 opacity-60'
                    : isCrit
                    ? 'bg-rose-950/15 border-rose-500/30 hover:border-rose-500/50'
                    : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                  {/* Left Column: Details */}
                  <div className="space-y-2 max-w-3xl">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider flex items-center gap-1 ${
                        isCrit ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' :
                        isWarn ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' :
                        'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                      }`}>
                        {isCrit && <AlertOctagon className="w-3 h-3 animate-pulse" />}
                        {alert.severity}
                      </span>

                      <button
                        onClick={() => onNavigate && onNavigate('assets')}
                        className="font-mono text-xs font-bold text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-2.5 py-0.5 rounded-lg hover:bg-cyan-900/60"
                        title="Inspect Battery Asset"
                      >
                        {alert.battery_id}
                      </button>

                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                        isResolved ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-800/40' :
                        isAck ? 'bg-blue-950/60 text-blue-400 border border-blue-800/40' :
                        'bg-slate-800 text-slate-400'
                      }`}>
                        Status: {alert.status}
                      </span>

                      <span className="text-[11px] text-slate-500 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {new Date(alert.created_at).toLocaleString()}
                      </span>
                    </div>

                    <h3 className="text-base font-bold text-white">
                      {alert.title}
                    </h3>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {alert.description}
                    </p>

                    {/* Prescriptive Recommendation Box */}
                    <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 flex items-start gap-3 mt-2">
                      <div className="p-1 bg-cyan-500/10 text-cyan-400 rounded shrink-0 mt-0.5">
                        <Check className="w-3.5 h-3.5" />
                      </div>
                      <div className="text-xs">
                        <span className="font-mono font-bold text-cyan-400 mr-2">{alert.action_code}:</span>
                        <span className="text-slate-300">{alert.recommendation}</span>
                      </div>
                    </div>
                  </div>

                  {/* Right Column: Actions */}
                  <div className="flex md:flex-col items-center md:items-end gap-2 shrink-0">
                    {!isResolved && !isAck && (
                      <button
                        onClick={() => handleUpdateStatus(alert.id, 'ACKNOWLEDGED')}
                        className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 flex items-center gap-1"
                      >
                        Acknowledge
                      </button>
                    )}

                    {!isResolved && (
                      <button
                        onClick={() => handleUpdateStatus(alert.id, 'RESOLVED')}
                        className="px-4 py-1.5 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 text-xs font-bold rounded-xl border border-emerald-500/40 flex items-center gap-1"
                      >
                        <Check className="w-3.5 h-3.5" /> Resolve Alert
                      </button>
                    )}

                    {onNavigate && (
                      <button
                        onClick={() => onNavigate('maintenance')}
                        className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1 mt-1"
                      >
                        Schedule Service <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
