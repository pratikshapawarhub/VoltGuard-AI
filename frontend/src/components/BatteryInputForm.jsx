import React, { useState } from 'react';
import { Upload, Sparkles, RefreshCw, AlertCircle } from 'lucide-react';

const PRESETS = [
  {
    label: 'Healthy Cell (B0005 Cycle 15)',
    data: {
      battery_id: 'B0005_C15',
      cycle_number: 15,
      voltage_mean: 3.54,
      voltage_max: 4.20,
      voltage_min: 2.52,
      voltage_std: 0.23,
      current_mean: 1.84,
      current_std: 0.51,
      temperature_mean: 31.8,
      temperature_max: 38.2,
      temperature_min: 23.9,
      charge_duration: 10450.0,
      discharge_duration: 3340.0,
      internal_impedance: 0.118,
      recent_soh_drop: 0.2
    }
  },
  {
    label: 'Moderate Cell (B0007 Cycle 75)',
    data: {
      battery_id: 'B0007_C75',
      cycle_number: 75,
      voltage_mean: 3.51,
      voltage_max: 4.19,
      voltage_min: 2.44,
      voltage_std: 0.24,
      current_mean: 1.84,
      current_std: 0.52,
      temperature_mean: 32.5,
      temperature_max: 39.4,
      temperature_min: 24.0,
      charge_duration: 10480.0,
      discharge_duration: 3120.0,
      internal_impedance: 0.138,
      recent_soh_drop: 0.5
    }
  },
  {
    label: 'Degraded Cell (B0018 Cycle 95)',
    data: {
      battery_id: 'B0018_C95',
      cycle_number: 95,
      voltage_mean: 3.47,
      voltage_max: 4.18,
      voltage_min: 2.38,
      voltage_std: 0.26,
      current_mean: 1.83,
      current_std: 0.53,
      temperature_mean: 33.1,
      temperature_max: 40.8,
      temperature_min: 24.2,
      charge_duration: 10520.0,
      discharge_duration: 2950.0,
      internal_impedance: 0.158,
      recent_soh_drop: 1.2
    }
  },
  {
    label: 'Critical Cell (B0006 Cycle 135)',
    data: {
      battery_id: 'B0006_C135',
      cycle_number: 135,
      voltage_mean: 3.41,
      voltage_max: 4.18,
      voltage_min: 2.12,
      voltage_std: 0.28,
      current_mean: 1.82,
      current_std: 0.55,
      temperature_mean: 34.2,
      temperature_max: 42.5,
      temperature_min: 24.5,
      charge_duration: 10600.0,
      discharge_duration: 2450.0,
      internal_impedance: 0.176,
      recent_soh_drop: 2.4
    }
  }
];

export default function BatteryInputForm({ onSubmit, isLoading, onFileUpload }) {
  const [formData, setFormData] = useState(PRESETS[0].data);
  const [fileError, setFileError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'battery_id' ? value : parseFloat(value) || 0
    }));
  };

  const handlePresetSelect = (presetData) => {
    setFormData(presetData);
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.name.endsWith('.csv')) {
        setFileError('Only .csv files are supported');
        return;
      }
      setFileError(null);
      if (onFileUpload) {
        onFileUpload(file);
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-navy-800 gap-3">
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            Battery Measurement Telemetry Input
          </h3>
          <p className="text-xs text-slate-400">Select benchmark preset, upload CSV, or input live measurements</p>
        </div>

        <div className="flex items-center gap-2">
          <label className="cursor-pointer flex items-center gap-1.5 px-3 py-1.5 bg-navy-800 hover:bg-navy-750 text-slate-300 text-xs rounded-lg border border-navy-700 transition">
            <Upload className="w-3.5 h-3.5 text-cyan-400" />
            <span>Upload CSV</span>
            <input type="file" accept=".csv" onChange={handleFileInput} className="hidden" />
          </label>
        </div>
      </div>

      {fileError && (
        <div className="mt-3 p-2 bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs rounded-lg flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          <span>{fileError}</span>
        </div>
      )}

      {/* Preset Buttons */}
      <div className="mt-4">
        <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
          Benchmark NASA Battery Presets
        </span>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handlePresetSelect(p.data)}
              className="text-left p-2.5 rounded-lg bg-navy-850 hover:bg-navy-800 border border-navy-750 hover:border-cyan-500/30 transition text-xs"
            >
              <span className="text-slate-200 font-medium block truncate">{p.label}</span>
              <span className="text-[10px] text-slate-400 font-mono">
                Z: {p.data.internal_impedance}Ω • T: {p.data.temperature_max}°C
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Form Fields */}
      <form onSubmit={handleSubmit} className="mt-5 space-y-4">
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 text-xs">
          <div>
            <label className="text-slate-400 block mb-1">Battery ID</label>
            <input
              type="text"
              name="battery_id"
              value={formData.battery_id}
              onChange={handleChange}
              className="w-full bg-navy-950 border border-navy-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">Cycle Number</label>
            <input
              type="number"
              name="cycle_number"
              value={formData.cycle_number}
              onChange={handleChange}
              min="1"
              max="1000"
              className="w-full bg-navy-950 border border-navy-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">Voltage Mean (V)</label>
            <input
              type="number"
              step="0.01"
              name="voltage_mean"
              value={formData.voltage_mean}
              onChange={handleChange}
              className="w-full bg-navy-950 border border-navy-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">Cut-off Voltage Min (V)</label>
            <input
              type="number"
              step="0.01"
              name="voltage_min"
              value={formData.voltage_min}
              onChange={handleChange}
              className="w-full bg-navy-950 border border-navy-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">Peak Temp Max (°C)</label>
            <input
              type="number"
              step="0.1"
              name="temperature_max"
              value={formData.temperature_max}
              onChange={handleChange}
              className="w-full bg-navy-950 border border-navy-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">Internal Impedance (Ω)</label>
            <input
              type="number"
              step="0.001"
              name="internal_impedance"
              value={formData.internal_impedance}
              onChange={handleChange}
              className="w-full bg-navy-950 border border-navy-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">Discharge Duration (s)</label>
            <input
              type="number"
              step="1"
              name="discharge_duration"
              value={formData.discharge_duration}
              onChange={handleChange}
              className="w-full bg-navy-950 border border-navy-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
              required
            />
          </div>

          <div>
            <label className="text-slate-400 block mb-1">Recent SOH Drop (%)</label>
            <input
              type="number"
              step="0.1"
              name="recent_soh_drop"
              value={formData.recent_soh_drop}
              onChange={handleChange}
              className="w-full bg-navy-950 border border-navy-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
            />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={isLoading}
            className="flex items-center gap-2 px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-navy-950 font-semibold text-xs rounded-lg transition disabled:opacity-50"
          >
            {isLoading ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Processing Models...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-3.5 h-3.5" />
                <span>Run Diagnostic & Prognosis Engine</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
