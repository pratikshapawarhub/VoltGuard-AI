import React from 'react';
import { Zap, ShieldCheck, Activity, Database, BookOpen, Bell } from 'lucide-react';

export default function Navbar({ activePage, setActivePage, isConnected, criticalAlertCount = 0 }) {
  return (
    <header className="h-16 border-b border-navy-800 bg-navy-900/95 backdrop-blur px-4 sm:px-6 flex items-center justify-between sticky top-0 z-40">
      {/* Brand Identity */}
      <div className="flex items-center space-x-3">
        <div className="p-2 bg-cyan-500/10 rounded-xl border border-cyan-500/25 text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.15)]">
          <Zap className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold tracking-tight text-white">
              VoltGuard <span className="text-cyan-400 font-semibold">AI</span>
            </span>
            <span className="hidden sm:inline-block text-[10px] bg-cyan-950/60 text-cyan-300 font-mono px-2 py-0.5 rounded border border-cyan-800/50">
              Enterprise v1.0
            </span>
          </div>
          <p className="text-[11px] text-slate-400 hidden sm:block leading-none">
            Intelligent Battery Health. Predictive Maintenance. Smarter Decisions.
          </p>
        </div>
      </div>

      {/* Action Indicators */}
      <div className="flex items-center gap-3">
        {/* Alerts Pill */}
        <button
          onClick={() => setActivePage('alerts')}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-navy-800 bg-navy-950 text-slate-300 hover:text-white hover:border-slate-700 transition-all text-xs"
        >
          <Bell className="w-3.5 h-3.5 text-amber-400" />
          <span className="hidden md:inline text-[11px]">Alerts</span>
          {criticalAlertCount > 0 && (
            <span className="bg-rose-500 text-white font-mono text-[10px] font-bold px-1.5 py-0.2 rounded-full">
              {criticalAlertCount}
            </span>
          )}
        </button>

        {/* Academic Mapping Secondary Access */}
        <button
          onClick={() => setActivePage('academic_mapping')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
            activePage === 'academic_mapping'
              ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
              : 'text-slate-400 hover:text-slate-200 border border-navy-800 bg-navy-950'
          }`}
          title="Open Academic Curriculum Mapping & Practical Evidence"
        >
          <BookOpen className="w-3.5 h-3.5 text-purple-400" />
          <span className="hidden lg:inline text-[11px]">Academic Traceability</span>
        </button>

        {/* Connection Status Indicator */}
        <div className="flex items-center gap-2 text-xs px-3 py-1.5 rounded-full border bg-navy-850 border-navy-700">
          <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
          <span className="text-slate-300 font-medium text-[11px] hidden sm:inline">
            {isConnected ? 'System Operational' : 'Connecting...'}
          </span>
        </div>
      </div>
    </header>
  );
}
