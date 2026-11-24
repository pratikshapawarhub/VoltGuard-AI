import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import OverviewDashboard from './pages/OverviewDashboard';
import BatteryAssetManagement from './pages/BatteryAssetManagement';
import BatteryMonitoring from './pages/BatteryMonitoring';
import BatteryHealthPrediction from './pages/BatteryHealthPrediction';
import BatteryClustering from './pages/BatteryClustering';
import MaintenanceCenter from './pages/MaintenanceCenter';
import AlertsCenter from './pages/AlertsCenter';
import ReportsCenter from './pages/ReportsCenter';
import AcademicMapping from './pages/AcademicMapping';

// Individual Practical Laboratories (accessible via deep-links/academic trace)
import RegressionAnalysis from './pages/RegressionAnalysis';
import ClassificationAnalysis from './pages/ClassificationAnalysis';
import EnsembleAnalysis from './pages/EnsembleAnalysis';
import PEASAndExpertSystem from './pages/PEASAndExpertSystem';
import SearchLab from './pages/SearchLab';

import { api } from './services/api';

export default function App() {
  const [activePage, setActivePage] = useState('overview');
  const [isConnected, setIsConnected] = useState(false);
  const [criticalAlertCount, setCriticalAlertCount] = useState(0);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        await api.getHealth();
        setIsConnected(true);
        const stats = await api.getAlertStats().catch(() => null);
        if (stats && stats.critical_alerts !== undefined) {
          setCriticalAlertCount(stats.critical_alerts);
        }
      } catch (err) {
        setIsConnected(false);
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 15000);
    return () => clearInterval(interval);
  }, []);

  const renderActivePage = () => {
    switch (activePage) {
      // Commercial B2B SaaS Modules
      case 'overview':
        return <OverviewDashboard onNavigate={setActivePage} />;
      case 'assets':
        return <BatteryAssetManagement onNavigate={setActivePage} />;
      case 'monitoring':
        return <BatteryMonitoring onNavigate={setActivePage} />;
      case 'prediction':
        return <BatteryHealthPrediction onNavigate={setActivePage} />;
      case 'analytics':
        return <BatteryClustering onNavigate={setActivePage} />;
      case 'maintenance':
        return <MaintenanceCenter onNavigate={setActivePage} />;
      case 'alerts':
        return <AlertsCenter onNavigate={setActivePage} />;
      case 'reports':
        return <ReportsCenter onNavigate={setActivePage} />;
      case 'academic_mapping':
        return <AcademicMapping onNavigate={setActivePage} />;

      // Legacy/Algorithm Laboratory Deep-links
      case 'regression':
        return <RegressionAnalysis onNavigate={setActivePage} />;
      case 'classification':
        return <ClassificationAnalysis onNavigate={setActivePage} />;
      case 'ensemble':
        return <EnsembleAnalysis onNavigate={setActivePage} />;
      case 'clustering':
        return <BatteryClustering onNavigate={setActivePage} />;
      case 'expert_system':
        return <PEASAndExpertSystem onNavigate={setActivePage} />;
      case 'search_lab':
        return <SearchLab onNavigate={setActivePage} />;

      default:
        return <OverviewDashboard onNavigate={setActivePage} />;
    }
  };

  return (
    <div className="min-h-screen bg-navy-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      <Navbar 
        activePage={activePage} 
        setActivePage={setActivePage} 
        isConnected={isConnected} 
        criticalAlertCount={criticalAlertCount} 
      />
      
      <div className="flex-1 flex overflow-hidden">
        <Sidebar activePage={activePage} setActivePage={setActivePage} />
        
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full">
          {renderActivePage()}
        </main>
      </div>
    </div>
  );
}
