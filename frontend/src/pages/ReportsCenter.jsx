import React, { useState, useEffect } from 'react';
import { 
  FileSpreadsheet, Download, RefreshCw, Layers, CheckCircle2, 
  BarChart2, FileText, Database, ShieldCheck, ExternalLink, Calendar
} from 'lucide-react';
import { api } from '../services/api';

export default function ReportsCenter() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReport();
  }, []);

  const loadReport = async () => {
    try {
      setLoading(true);
      const data = await api.getReportSummary();
      setReport(data);
    } catch (err) {
      console.error("Failed to load report summary:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (reportType) => {
    const url = api.getExportCsvUrl(reportType);
    window.open(url, '_blank');
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 text-xs font-semibold tracking-wider uppercase mb-1">
            <FileSpreadsheet className="w-4 h-4" /> Reporting & Analytics
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Fleet Health Dossier & Exports
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Consolidated enterprise health audits, raw telemetry data streams, maintenance work orders, and CSV export utilities.
          </p>
        </div>

        <button
          onClick={loadReport}
          className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-slate-300 rounded-xl text-xs flex items-center gap-2 self-start md:self-auto border border-slate-800"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} /> Refresh Report
        </button>
      </div>

      {/* CSV Export Quick Action Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Export 1: Battery Assets */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-cyan-500/40 transition-all flex flex-col justify-between">
          <div>
            <div className="p-2.5 bg-cyan-500/10 text-cyan-400 rounded-xl w-fit border border-cyan-500/20 mb-3">
              <Database className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-sm">Battery Assets Registry</h3>
            <p className="text-xs text-slate-400 mt-1">
              Complete catalog of registered cells, chemistry, rated capacities, locations, and current SOH.
            </p>
          </div>
          <button
            onClick={() => handleDownload('assets')}
            className="mt-4 w-full py-2 bg-slate-950 hover:bg-slate-800 text-cyan-400 border border-slate-800 hover:border-cyan-500/50 rounded-xl text-xs font-bold flex items-center justify-center gap-2 cursor-pointer transition-all"
          >
            <Download className="w-3.5 h-3.5" /> Export Assets CSV
          </button>
        </div>

        {/* Export 2: Diagnostic History */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-blue-500/40 transition-all flex flex-col justify-between">
          <div>
            <div className="p-2.5 bg-blue-500/10 text-blue-400 rounded-xl w-fit border border-blue-500/20 mb-3">
              <Layers className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-sm">Diagnostic Predictions</h3>
            <p className="text-xs text-slate-400 mt-1">
              Timestamped SOH, RUL, condition classifications, ensemble consensus, and telemetry records.
            </p>
          </div>
          <button
            onClick={() => handleDownload('history')}
            className="mt-4 w-full py-2 bg-slate-950 hover:bg-slate-800 text-blue-400 border border-slate-800 hover:border-blue-500/50 rounded-xl text-xs font-bold flex items-center justify-center gap-2 cursor-pointer transition-all"
          >
            <Download className="w-3.5 h-3.5" /> Export Diagnostics CSV
          </button>
        </div>

        {/* Export 3: Maintenance Tasks */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-amber-500/40 transition-all flex flex-col justify-between">
          <div>
            <div className="p-2.5 bg-amber-500/10 text-amber-400 rounded-xl w-fit border border-amber-500/20 mb-3">
              <Calendar className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-sm">Maintenance Work Orders</h3>
            <p className="text-xs text-slate-400 mt-1">
              Dispatched servicing schedules, assigned technicians, estimated costs, and A* path sequences.
            </p>
          </div>
          <button
            onClick={() => handleDownload('maintenance')}
            className="mt-4 w-full py-2 bg-slate-950 hover:bg-slate-800 text-amber-400 border border-slate-800 hover:border-amber-500/50 rounded-xl text-xs font-bold flex items-center justify-center gap-2 cursor-pointer transition-all"
          >
            <Download className="w-3.5 h-3.5" /> Export Tasks CSV
          </button>
        </div>

        {/* Export 4: Alerts Ledger */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-rose-500/40 transition-all flex flex-col justify-between">
          <div>
            <div className="p-2.5 bg-rose-500/10 text-rose-400 rounded-xl w-fit border border-rose-500/20 mb-3">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-white text-sm">Operational Alerts Ledger</h3>
            <p className="text-xs text-slate-400 mt-1">
              Comprehensive audit trail of triggered expert rules, thermal warnings, and resolution timestamps.
            </p>
          </div>
          <button
            onClick={() => handleDownload('alerts')}
            className="mt-4 w-full py-2 bg-slate-950 hover:bg-slate-800 text-rose-400 border border-slate-800 hover:border-rose-500/50 rounded-xl text-xs font-bold flex items-center justify-center gap-2 cursor-pointer transition-all"
          >
            <Download className="w-3.5 h-3.5" /> Export Alerts CSV
          </button>
        </div>
      </div>

      {/* Fleet Health Summary Table */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-base font-semibold text-white">Fleet Asset Dossier Snapshot</h3>
            <p className="text-xs text-slate-400">Current electrochemical state of registered battery assets</p>
          </div>
          {report && (
            <span className="text-[10px] font-mono text-slate-500">
              Synced: {new Date(report.report_generated_at).toLocaleString()}
            </span>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-950 text-slate-400 border-b border-slate-800 font-semibold">
              <tr>
                <th className="py-3 px-4">Battery ID</th>
                <th className="py-3 px-4">Asset Name</th>
                <th className="py-3 px-4">Chemistry</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Current SOH</th>
                <th className="py-3 px-4">Estimated RUL</th>
                <th className="py-3 px-4">Condition</th>
                <th className="py-3 px-4">Operating Regime</th>
                <th className="py-3 px-4">Location</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {report && report.assets_summary && report.assets_summary.map((asset) => (
                <tr key={asset.battery_id} className="hover:bg-slate-800/40">
                  <td className="py-3 px-4 font-bold text-cyan-400">{asset.battery_id}</td>
                  <td className="py-3 px-4 font-sans text-white font-medium">{asset.name}</td>
                  <td className="py-3 px-4 text-slate-300">{asset.chemistry}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      asset.status === 'ACTIVE' ? 'bg-emerald-500/20 text-emerald-400' :
                      asset.status === 'MAINTENANCE' ? 'bg-amber-500/20 text-amber-400' :
                      'bg-rose-500/20 text-rose-400'
                    }`}>
                      {asset.status}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-bold text-white">{asset.current_soh}%</td>
                  <td className="py-3 px-4 text-slate-300">{asset.current_rul} cyc</td>
                  <td className="py-3 px-4 font-sans text-slate-300">{asset.health_condition}</td>
                  <td className="py-3 px-4 text-cyan-300 text-[11px] font-sans">{asset.operating_regime}</td>
                  <td className="py-3 px-4 font-sans text-slate-400">{asset.location}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
