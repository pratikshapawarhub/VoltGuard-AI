import React from 'react';
import {
  LayoutDashboard,
  Boxes,
  Activity,
  Cpu,
  LineChart,
  Wrench,
  Bell,
  FileSpreadsheet,
  BookOpen,
  ChevronRight,
  ShieldCheck
} from 'lucide-react';

export const PRODUCT_MODULES = [
  { id: 'overview', label: 'Fleet Overview', icon: LayoutDashboard },
  { id: 'assets', label: 'Battery Assets', icon: Boxes },
  { id: 'monitoring', label: 'Health Monitoring', icon: Activity },
  { id: 'prediction', label: 'Predictive Intelligence', icon: Cpu },
  { id: 'analytics', label: 'Analytics & Regimes', icon: LineChart },
  { id: 'maintenance', label: 'Maintenance Center', icon: Wrench },
  { id: 'alerts', label: 'Alerts & Notifications', icon: Bell },
  { id: 'reports', label: 'Reports & Exports', icon: FileSpreadsheet }
];

export default function Sidebar({ activePage, setActivePage }) {
  return (
    <aside className="w-64 bg-navy-900 border-r border-navy-800 flex flex-col justify-between h-[calc(100vh-4rem)] sticky top-16 select-none shrink-0">
      <div className="py-4 px-3 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-bold tracking-wider text-slate-500 uppercase">
          Enterprise Modules
        </div>
        
        {PRODUCT_MODULES.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                isActive
                  ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-navy-850 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {isActive && (
                <div className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
              )}
            </button>
          );
        })}
      </div>

      {/* Academic Implementation Secondary Access Footer */}
      <div className="p-3 border-t border-navy-800/80 bg-navy-950/40">
        <button
          onClick={() => setActivePage('academic_mapping')}
          className={`w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition-all border ${
            activePage === 'academic_mapping'
              ? 'bg-purple-950/40 text-purple-300 border-purple-500/40'
              : 'bg-navy-900/60 text-slate-400 hover:text-slate-200 border-navy-800 hover:border-slate-700'
          }`}
        >
          <div className="flex items-center gap-2.5">
            <BookOpen className="w-4 h-4 text-purple-400 shrink-0" />
            <div className="text-left">
              <div className="text-[11px] font-semibold text-slate-200">Academic Traceability</div>
              <div className="text-[10px] text-slate-500">P1–P7 Syllabus Mapping</div>
            </div>
          </div>
          <ChevronRight className="w-3.5 h-3.5 text-slate-500" />
        </button>

        <div className="mt-3 px-1 flex items-center justify-between text-[10px] text-slate-600 font-mono">
          <span>B2B SaaS Edition</span>
          <span>v1.0.0</span>
        </div>
      </div>
    </aside>
  );
}
