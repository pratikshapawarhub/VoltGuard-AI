import React from 'react';

export default function KPICard({ title, value, unit = '', subtitle, icon: Icon, color = 'cyan', trend }) {
  const colorStyles = {
    cyan: 'border-cyan-500/20 bg-cyan-500/5 text-cyan-400',
    emerald: 'border-emerald-500/20 bg-emerald-500/5 text-emerald-400',
    amber: 'border-amber-500/20 bg-amber-500/5 text-amber-400',
    rose: 'border-rose-500/20 bg-rose-500/5 text-rose-400',
    purple: 'border-purple-500/20 bg-purple-500/5 text-purple-400'
  };

  const badgeColor = colorStyles[color] || colorStyles.cyan;

  return (
    <div className="bg-navy-900 border border-navy-800 rounded-xl p-5 shadow-lg relative overflow-hidden transition-all hover:border-navy-700">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`p-2 rounded-lg border ${badgeColor}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="mt-3 flex items-baseline gap-1">
        <span className="text-2xl font-bold text-white tracking-tight">{value}</span>
        {unit && <span className="text-xs font-medium text-slate-400 ml-1">{unit}</span>}
      </div>

      {subtitle && (
        <p className="mt-1 text-xs text-slate-400 flex items-center justify-between">
          <span>{subtitle}</span>
          {trend && (
            <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/40 px-1.5 py-0.5 rounded border border-cyan-800/40">
              {trend}
            </span>
          )}
        </p>
      )}
    </div>
  );
}
