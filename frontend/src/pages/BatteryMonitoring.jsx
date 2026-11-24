import React, { useState, useEffect } from 'react';
import { Database, Filter, RefreshCw } from 'lucide-react';
import { api } from '../services/api';

export default function BatteryMonitoring() {
  const [selectedBattery, setSelectedBattery] = useState('All');
  const [records, setRecords] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [limit, setLimit] = useState(25);
  const [offset, setOffset] = useState(0);
  const [totalRecords, setTotalRecords] = useState(0);

  const fetchRecords = (battery, off = 0) => {
    setIsLoading(true);
    const batId = battery === 'All' ? null : battery;
    api.getDatasetRecords(batId, limit, off)
      .then((data) => {
        setRecords(data.records);
        setTotalRecords(data.total_records);
        setOffset(off);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setIsLoading(false);
      });
  };

  useEffect(() => {
    fetchRecords(selectedBattery, 0);
  }, [selectedBattery, limit]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Database className="w-5 h-5 text-cyan-400" />
            NASA Battery Cycle Telemetry Records
          </h2>
          <p className="text-xs text-slate-400">
            Inspect cycle-level statistical features extracted from raw NASA .mat files (B0005, B0006, B0007, B0018)
          </p>
        </div>

        {/* Battery Filter Tabs */}
        <div className="flex items-center gap-1 bg-navy-950 p-1 rounded-lg border border-navy-800">
          {['All', 'B0005', 'B0006', 'B0007', 'B0018'].map((bat) => (
            <button
              key={bat}
              onClick={() => setSelectedBattery(bat)}
              className={`px-3 py-1.5 rounded text-xs font-mono transition ${
                selectedBattery === bat
                  ? 'bg-cyan-500 text-navy-950 font-bold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {bat}
            </button>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
        <div className="flex items-center justify-between pb-3 border-b border-navy-800 text-xs text-slate-400">
          <span>
            Showing <strong className="text-white">{records.length}</strong> of{' '}
            <strong className="text-white">{totalRecords}</strong> total cycles
          </span>

          <button
            onClick={() => fetchRecords(selectedBattery, offset)}
            className="flex items-center gap-1.5 text-cyan-400 hover:text-cyan-300"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>

        <div className="overflow-x-auto mt-3">
          <table className="w-full text-left text-xs">
            <thead className="text-[11px] text-slate-400 border-b border-navy-800 font-mono">
              <tr>
                <th className="py-2">Battery</th>
                <th className="py-2">Cycle #</th>
                <th className="py-2">SOH (%)</th>
                <th className="py-2">Capacity (Ahr)</th>
                <th className="py-2">RUL (Cycles)</th>
                <th className="py-2">Voltage Mean (V)</th>
                <th className="py-2">Voltage Min (V)</th>
                <th className="py-2">Temp Max (°C)</th>
                <th className="py-2">Impedance (Ω)</th>
                <th className="py-2">Condition</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-navy-800/60 font-mono">
              {records.map((r, idx) => (
                <tr key={idx} className="hover:bg-navy-850/50">
                  <td className="py-2 font-bold text-white font-sans">{r.battery_id}</td>
                  <td className="py-2 text-slate-300">{r.cycle_number}</td>
                  <td className="py-2 text-cyan-300 font-semibold">{r.soh?.toFixed(2)}%</td>
                  <td className="py-2 text-slate-300">{r.discharge_capacity?.toFixed(4)}</td>
                  <td className="py-2 text-purple-300">{r.rul}</td>
                  <td className="py-2 text-slate-300">{r.voltage_mean?.toFixed(3)}</td>
                  <td className="py-2 text-slate-300">{r.voltage_min?.toFixed(3)}</td>
                  <td className="py-2 text-amber-300">{r.temperature_max?.toFixed(1)}</td>
                  <td className="py-2 text-slate-300">{r.internal_impedance?.toFixed(4)}</td>
                  <td className="py-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-sans ${
                      r.health_category === 'Healthy' ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20' :
                      r.health_category === 'Moderate' ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/20' :
                      r.health_category === 'Degraded' ? 'bg-amber-500/10 text-amber-300 border border-amber-500/20' :
                      'bg-rose-500/10 text-rose-300 border border-rose-500/20'
                    }`}>
                      {r.health_category}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        <div className="flex items-center justify-between pt-4 border-t border-navy-800 mt-3 text-xs">
          <button
            onClick={() => fetchRecords(selectedBattery, Math.max(0, offset - limit))}
            disabled={offset === 0 || isLoading}
            className="px-3 py-1.5 bg-navy-850 hover:bg-navy-800 text-slate-300 rounded border border-navy-700 disabled:opacity-40"
          >
            ← Previous
          </button>
          <span className="text-slate-400 font-mono">
            Page {Math.floor(offset / limit) + 1} of {Math.ceil(totalRecords / limit)}
          </span>
          <button
            onClick={() => fetchRecords(selectedBattery, offset + limit)}
            disabled={offset + limit >= totalRecords || isLoading}
            className="px-3 py-1.5 bg-navy-850 hover:bg-navy-800 text-slate-300 rounded border border-navy-700 disabled:opacity-40"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
}
