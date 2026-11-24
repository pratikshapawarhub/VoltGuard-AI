import React, { useState, useEffect } from 'react';
import { 
  Boxes, Plus, Search, Filter, RefreshCw, AlertTriangle, 
  CheckCircle2, Clock, MapPin, Battery, Activity, Trash2, 
  Edit3, Eye, ChevronRight, X, ShieldAlert, Cpu
} from 'lucide-react';
import { api } from '../services/api';

export default function BatteryAssetManagement({ onNavigate }) {
  const [batteries, setBatteries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  
  // Registration modal state
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [formData, setFormData] = useState({
    battery_id: '',
    name: '',
    chemistry: 'LiCoO2 / Graphite',
    nominal_capacity: 2.0,
    nominal_voltage: 3.7,
    installation_date: new Date().toISOString().split('T')[0],
    status: 'ACTIVE',
    location: 'Chamber Bay A',
    notes: ''
  });
  const [formSubmitting, setFormSubmitting] = useState(false);
  const [formError, setFormError] = useState('');

  // Asset detail drawer state
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [assetHistory, setAssetHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  // Edit modal state
  const [editingAsset, setEditingAsset] = useState(null);
  const [editFormData, setEditFormData] = useState({});

  useEffect(() => {
    loadBatteries();
  }, [statusFilter]);

  const loadBatteries = async () => {
    try {
      setLoading(true);
      const st = statusFilter === 'ALL' ? null : statusFilter;
      const data = await api.listBatteries(search || null, st);
      setBatteries(data);
    } catch (err) {
      console.error("Failed to load battery assets:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadBatteries();
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    if (!formData.battery_id.trim() || !formData.name.trim()) {
      setFormError('Battery ID and Name are required.');
      return;
    }

    try {
      setFormSubmitting(true);
      await api.registerBattery(formData);
      setShowRegisterModal(false);
      setFormData({
        battery_id: '',
        name: '',
        chemistry: 'LiCoO2 / Graphite',
        nominal_capacity: 2.0,
        nominal_voltage: 3.7,
        installation_date: new Date().toISOString().split('T')[0],
        status: 'ACTIVE',
        location: 'Chamber Bay A',
        notes: ''
      });
      loadBatteries();
    } catch (err) {
      setFormError(err.message || 'Failed to register battery asset.');
    } finally {
      setFormSubmitting(false);
    }
  };

  const handleOpenDetail = async (asset) => {
    setSelectedAsset(asset);
    try {
      setLoadingHistory(true);
      const res = await api.getBatteryHistory(asset.battery_id, 20);
      setAssetHistory(res.history || []);
    } catch (err) {
      console.error("Failed to fetch asset history:", err);
      setAssetHistory([]);
    } finally {
      setLoadingHistory(false);
    }
  };

  const handleDelete = async (batteryId) => {
    if (!window.confirm(`Are you sure you want to decommission and remove battery ${batteryId}?`)) {
      return;
    }
    try {
      await api.deleteBattery(batteryId);
      if (selectedAsset && selectedAsset.battery_id === batteryId) {
        setSelectedAsset(null);
      }
      loadBatteries();
    } catch (err) {
      alert(`Delete failed: ${err.message}`);
    }
  };

  const handleOpenEdit = (asset) => {
    setEditingAsset(asset);
    setEditFormData({
      name: asset.name,
      chemistry: asset.chemistry,
      nominal_capacity: asset.nominal_capacity,
      nominal_voltage: asset.nominal_voltage,
      status: asset.status,
      location: asset.location,
      notes: asset.notes || ''
    });
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.updateBattery(editingAsset.battery_id, editFormData);
      setEditingAsset(null);
      loadBatteries();
      if (selectedAsset && selectedAsset.battery_id === editingAsset.battery_id) {
        setSelectedAsset({ ...selectedAsset, ...editFormData });
      }
    } catch (err) {
      alert(`Update failed: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 text-xs font-semibold tracking-wider uppercase mb-1">
            <Boxes className="w-4 h-4" /> Asset Management
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Battery Fleet Registry
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Register, inspect, and manage physical battery packs, chemical specifications, and lifecycle histories.
          </p>
        </div>

        <button
          onClick={() => setShowRegisterModal(true)}
          className="px-4 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold rounded-xl shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer text-xs"
        >
          <Plus className="w-4 h-4" /> Register New Battery
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="w-full md:w-80 relative">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by ID, name, bay..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </form>

        {/* Status Filter Chips */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full md:w-auto pb-1 md:pb-0">
          {['ALL', 'ACTIVE', 'MAINTENANCE', 'DECOMMISSIONED'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap ${
                statusFilter === st
                  ? 'bg-cyan-500 text-slate-950 shadow-sm'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {st}
            </button>
          ))}
          <button
            onClick={loadBatteries}
            className="p-2 text-slate-400 hover:text-white bg-slate-950 border border-slate-800 rounded-lg ml-1"
            title="Refresh assets"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {/* Battery Assets Cards Grid */}
      {loading ? (
        <div className="py-16 text-center text-slate-400">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-2 text-cyan-400" />
          <p className="text-xs">Loading battery asset registry...</p>
        </div>
      ) : batteries.length === 0 ? (
        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-12 text-center">
          <Boxes className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <h3 className="text-white font-semibold text-base">No Battery Assets Found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto mt-1">
            No batteries match your search criteria. You can register a new battery asset to begin live telemetry tracking.
          </p>
          <button
            onClick={() => setShowRegisterModal(true)}
            className="mt-4 px-4 py-2 bg-cyan-500 text-slate-950 font-bold rounded-xl text-xs inline-flex items-center gap-1.5"
          >
            <Plus className="w-3.5 h-3.5" /> Register Battery
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {batteries.map((asset) => {
            const isCritical = asset.health_condition === 'Critical' || asset.current_soh < 70;
            const isWarning = asset.health_condition === 'Degraded' || (asset.current_soh >= 70 && asset.current_soh < 80);
            return (
              <div
                key={asset.battery_id}
                className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all flex flex-col justify-between group"
              >
                <div>
                  {/* Top Bar */}
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-sm text-cyan-400">
                          {asset.battery_id}
                        </span>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                          asset.status === 'ACTIVE'
                            ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30'
                            : asset.status === 'MAINTENANCE'
                            ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30'
                            : 'bg-rose-500/15 text-rose-300 border border-rose-500/30'
                        }`}>
                          {asset.status}
                        </span>
                      </div>
                      <h3 className="text-sm font-semibold text-white mt-1 group-hover:text-cyan-300 transition-colors">
                        {asset.name}
                      </h3>
                    </div>

                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => handleOpenEdit(asset)}
                        className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-all"
                        title="Edit metadata"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleDelete(asset.battery_id)}
                        className="p-1.5 text-slate-500 hover:text-rose-400 rounded-lg hover:bg-slate-800 transition-all"
                        title="Decommission"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  {/* SOH Progress Bar */}
                  <div className="bg-slate-950 p-3 rounded-xl border border-slate-800/80 my-3">
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="text-slate-400 font-medium">State of Health (SOH)</span>
                      <span className={`font-mono font-bold ${
                        isCritical ? 'text-rose-400' : isWarning ? 'text-amber-400' : 'text-emerald-400'
                      }`}>
                        {asset.current_soh}%
                      </span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${
                          isCritical ? 'bg-rose-500' : isWarning ? 'bg-amber-500' : 'bg-emerald-400'
                        }`}
                        style={{ width: `${Math.min(100, Math.max(0, asset.current_soh))}%` }}
                      />
                    </div>
                  </div>

                  {/* Specs Grid */}
                  <div className="grid grid-cols-2 gap-2 text-[11px] mb-3">
                    <div className="bg-slate-950/60 p-2 rounded-lg border border-slate-800/60">
                      <span className="text-slate-500 block">Chemistry</span>
                      <span className="text-slate-200 font-medium truncate block">{asset.chemistry}</span>
                    </div>
                    <div className="bg-slate-950/60 p-2 rounded-lg border border-slate-800/60">
                      <span className="text-slate-500 block">Rated Specs</span>
                      <span className="text-slate-200 font-medium font-mono">{asset.nominal_capacity}Ah • {asset.nominal_voltage}V</span>
                    </div>
                    <div className="bg-slate-950/60 p-2 rounded-lg border border-slate-800/60">
                      <span className="text-slate-500 block">Cycle Count</span>
                      <span className="text-cyan-400 font-mono font-semibold">Cycle {asset.cycle_count}</span>
                    </div>
                    <div className="bg-slate-950/60 p-2 rounded-lg border border-slate-800/60">
                      <span className="text-slate-500 block">Estimated RUL</span>
                      <span className="text-slate-200 font-mono font-medium">{asset.current_rul} cycles</span>
                    </div>
                  </div>
                </div>

                {/* Card Footer */}
                <div className="pt-3 border-t border-slate-800/60 flex items-center justify-between">
                  <div className="flex items-center gap-1 text-[11px] text-slate-400">
                    <MapPin className="w-3.5 h-3.5 text-slate-500" />
                    <span className="truncate max-w-[150px]">{asset.location}</span>
                  </div>

                  <button
                    onClick={() => handleOpenDetail(asset)}
                    className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1 cursor-pointer"
                  >
                    Inspect <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* REGISTRATION MODAL */}
      {showRegisterModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <Boxes className="w-5 h-5 text-cyan-400" /> Register Battery Asset
              </h2>
              <button
                onClick={() => setShowRegisterModal(false)}
                className="text-slate-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {formError && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs rounded-xl">
                {formError}
              </div>
            )}

            <form onSubmit={handleRegisterSubmit} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1 font-medium">Battery Identifier *</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. PACK-105 or B0022"
                    value={formData.battery_id}
                    onChange={(e) => setFormData({ ...formData, battery_id: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-400 block mb-1 font-medium">Descriptive Name *</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Delivery Van Module A"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1 font-medium">Chemistry</label>
                  <select
                    value={formData.chemistry}
                    onChange={(e) => setFormData({ ...formData, chemistry: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-2 py-2 text-white focus:border-cyan-500 focus:outline-none"
                  >
                    <option value="LiCoO2 / Graphite">LiCoO2 / Graphite</option>
                    <option value="NMC 811 / Silicon">NMC 811 / Silicon</option>
                    <option value="LFP (Lithium Iron)">LFP (Iron Phosphate)</option>
                    <option value="Solid State Li-Metal">Solid State Li-Metal</option>
                  </select>
                </div>
                <div>
                  <label className="text-slate-400 block mb-1 font-medium">Capacity (Ahr)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="0.1"
                    value={formData.nominal_capacity}
                    onChange={(e) => setFormData({ ...formData, nominal_capacity: parseFloat(e.target.value) || 2.0 })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-400 block mb-1 font-medium">Voltage (V)</label>
                  <input
                    type="number"
                    step="0.1"
                    min="1.0"
                    value={formData.nominal_voltage}
                    onChange={(e) => setFormData({ ...formData, nominal_voltage: parseFloat(e.target.value) || 3.7 })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white font-mono focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1 font-medium">Installation Date</label>
                  <input
                    type="date"
                    value={formData.installation_date}
                    onChange={(e) => setFormData({ ...formData, installation_date: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:border-cyan-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-slate-400 block mb-1 font-medium">Location / Bay</label>
                  <input
                    type="text"
                    placeholder="e.g. Rack 2 - Bay 4"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-400 block mb-1 font-medium">Operational Notes</label>
                <textarea
                  rows="2"
                  placeholder="Additional servicing notes or warranty requirements..."
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white focus:border-cyan-500 focus:outline-none"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowRegisterModal(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={formSubmitting}
                  className="px-5 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-xl flex items-center gap-2"
                >
                  {formSubmitting && <RefreshCw className="w-3.5 h-3.5 animate-spin" />}
                  Register Battery
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* EDIT MODAL */}
      {editingAsset && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h2 className="text-base font-bold text-white flex items-center gap-2">
                <Edit3 className="w-4 h-4 text-cyan-400" /> Edit Battery {editingAsset.battery_id}
              </h2>
              <button onClick={() => setEditingAsset(null)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleEditSubmit} className="space-y-3 text-xs">
              <div>
                <label className="text-slate-400 block mb-1">Name</label>
                <input
                  type="text"
                  value={editFormData.name}
                  onChange={(e) => setEditFormData({ ...editFormData, name: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1">Status</label>
                  <select
                    value={editFormData.status}
                    onChange={(e) => setEditFormData({ ...editFormData, status: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-2 py-2 text-white"
                  >
                    <option value="ACTIVE">ACTIVE</option>
                    <option value="MAINTENANCE">MAINTENANCE</option>
                    <option value="DECOMMISSIONED">DECOMMISSIONED</option>
                  </select>
                </div>
                <div>
                  <label className="text-slate-400 block mb-1">Location</label>
                  <input
                    type="text"
                    value={editFormData.location}
                    onChange={(e) => setEditFormData({ ...editFormData, location: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white"
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-400 block mb-1">Notes</label>
                <textarea
                  rows="2"
                  value={editFormData.notes}
                  onChange={(e) => setEditFormData({ ...editFormData, notes: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setEditingAsset(null)}
                  className="px-4 py-2 bg-slate-800 text-slate-300 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-cyan-500 text-slate-950 font-bold rounded-xl"
                >
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* DETAIL DRAWER */}
      {selectedAsset && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex justify-end">
          <div className="bg-slate-900 border-l border-slate-800 w-full max-w-xl h-full p-6 space-y-6 overflow-y-auto shadow-2xl">
            <div className="flex items-start justify-between pb-4 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-lg font-bold text-cyan-400">{selectedAsset.battery_id}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    selectedAsset.status === 'ACTIVE' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'
                  }`}>
                    {selectedAsset.status}
                  </span>
                </div>
                <h2 className="text-base font-semibold text-white mt-1">{selectedAsset.name}</h2>
              </div>
              <button
                onClick={() => setSelectedAsset(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Quick SOH Banner */}
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex items-center justify-between">
              <div>
                <span className="text-xs text-slate-500">Current Health State</span>
                <div className="text-xl font-bold text-white font-mono mt-0.5">
                  {selectedAsset.current_soh}% SOH
                </div>
              </div>
              <div className="text-right">
                <span className="text-xs text-slate-500">Operating Regime</span>
                <div className="text-xs font-semibold text-cyan-400 mt-1">
                  {selectedAsset.operating_regime}
                </div>
              </div>
            </div>

            {/* Technical Specs */}
            <div className="space-y-2">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Specifications</h3>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-500 block">Chemistry</span>
                  <span className="font-medium text-white">{selectedAsset.chemistry}</span>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-500 block">Nominal Capacity</span>
                  <span className="font-medium text-white font-mono">{selectedAsset.nominal_capacity} Ahr</span>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-500 block">Nominal Voltage</span>
                  <span className="font-medium text-white font-mono">{selectedAsset.nominal_voltage} V</span>
                </div>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                  <span className="text-slate-500 block">Installation Date</span>
                  <span className="font-medium text-white font-mono">{selectedAsset.installation_date}</span>
                </div>
              </div>
            </div>

            {/* Diagnostic History */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Diagnostic History ({assetHistory.length} Cycles)
                </h3>
                {onNavigate && (
                  <button
                    onClick={() => {
                      setSelectedAsset(null);
                      onNavigate('prediction');
                    }}
                    className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1"
                  >
                    Run Diagnosis <Cpu className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>

              {loadingHistory ? (
                <div className="py-6 text-center text-slate-500 text-xs">
                  <RefreshCw className="w-4 h-4 animate-spin mx-auto mb-1" />
                  Loading historical cycle records...
                </div>
              ) : assetHistory.length === 0 ? (
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800/80 text-center text-xs text-slate-500">
                  No automated prediction records found for this unit.
                </div>
              ) : (
                <div className="space-y-2 max-h-60 overflow-y-auto">
                  {assetHistory.map((rec) => (
                    <div key={rec.id} className="bg-slate-950 p-3 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
                      <div>
                        <div className="font-bold text-white">Cycle {rec.cycle_number}</div>
                        <div className="text-[10px] text-slate-500">{new Date(rec.timestamp).toLocaleString()}</div>
                      </div>
                      <div className="text-right">
                        <span className="font-mono text-cyan-400 font-bold">{rec.predicted_soh}% SOH</span>
                        <div className="text-[10px] text-slate-400">{rec.predicted_condition}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="pt-4 border-t border-slate-800 flex justify-end">
              <button
                onClick={() => setSelectedAsset(null)}
                className="px-5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl"
              >
                Close Drawer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
