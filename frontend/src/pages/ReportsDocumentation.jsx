import React, { useState } from 'react';
import { 
  FileText, BookOpen, Layers, CheckCircle2, Award, 
  ExternalLink, Download, Code, Cpu, ChevronRight, Terminal, BarChart2
} from 'lucide-react';

const PRACTICALS_MAP = [
  {
    num: "Practical 1",
    title: "PEAS Descriptors & Rule-Based Expert System",
    branch: "Knowledge-Based AI & Agent Architecture",
    file: "backend/ml/practical1/expert_system.py",
    api: "/api/practical1/evaluate",
    ui: "PEAS & Expert System",
    result: "100% Thermal Runaway Recall, 9 Forward-Chaining Production Rules"
  },
  {
    num: "Practical 2",
    title: "Problem Solving through Search & CSP",
    branch: "Classical AI Search & Constraint Optimization",
    file: "backend/ml/practical2/informed_search.py",
    api: "/api/practical2/compare",
    ui: "Search Algorithms Lab",
    result: "A* optimal cost $130.0 vs BFS $170.0; Hill Climbing -31.1% risk; CSP 0 backtracks"
  },
  {
    num: "Practical 3",
    title: "Regression Models for SOH & RUL",
    branch: "Supervised Continuous Learning",
    file: "backend/ml/practical3/manual_gradient_descent.py",
    api: "/api/practical3/predict-soh",
    ui: "Regression Analysis",
    result: "Sklearn SOH R²=0.9968 (MAE 0.34%); Scratch GD RUL R²=0.5872 (MAE 18.37 cyc)"
  },
  {
    num: "Practical 4",
    title: "Classification of Battery Degradation",
    branch: "Supervised Discrete Multi-Class Learning",
    file: "backend/ml/practical4/classifiers.py",
    api: "/api/practical4/classify",
    ui: "Classification Analysis",
    result: "Decision Tree 71.97% Accuracy; SVM best probability calibration (Log loss 1.226)"
  },
  {
    num: "Practical 5",
    title: "Ensemble Learning (Stacking, AdaBoost, Voting)",
    branch: "Meta-Learning & Ensemble Methods",
    file: "backend/ml/practical5/ensemble_models.py",
    api: "/api/practical5/metrics",
    ui: "Ensemble Analysis",
    result: "Stacking Meta-Classifier lowest Log Loss (1.1602) across all 7 evaluated models"
  },
  {
    num: "Practical 6",
    title: "Unsupervised Clustering of Operating Regimes",
    branch: "Unsupervised Pattern Recognition",
    file: "backend/ml/practical6/kmeans_clustering.py",
    api: "/api/practical6/metrics",
    ui: "Battery Clustering",
    result: "Optimal K=3 (Fresh 34.0%, Intermediate 31.1%, Degraded 34.9%), Silhouette 0.3608"
  },
  {
    num: "Practical 7",
    title: "Integrated Predictive Maintenance Platform",
    branch: "Full-Stack AI Engineering & MLOps",
    file: "backend/app/engine/engine.py",
    api: "/api/practical7/predict-all",
    ui: "Integrated Engine & Overview",
    result: "Unified inference pipeline combining P1-P6 with SQLite persistence & Dark UI"
  }
];

const FIGURES = [
  { name: "SOH Degradation Trajectories", file: "soh_degradation_curves.png", desc: "Comparative capacity fade across NASA B0005, B0006, B0007, B0018" },
  { name: "Feature Correlation Heatmap", file: "correlation_heatmap.png", desc: "Pearson cross-correlation matrix across all 15 operational features" },
  { name: "Actual vs Predicted SOH", file: "actual_vs_predicted_soh.png", desc: "Unseen B0018 test cell evaluation across Sklearn LR, RF, and Manual GD" },
  { name: "Gradient Descent Loss Curve", file: "gradient_descent_loss_curve.png", desc: "Batch GD Mean Squared Error convergence from scratch" },
  { name: "Confusion Matrices", file: "confusion_matrices_all_classifiers.png", desc: "4-class health state classification across SVM, DT, KNN, Naive Bayes" },
  { name: "Ensemble vs Base Comparison", file: "ensemble_vs_base_comparison.png", desc: "Side-by-side benchmark comparing Base Classifiers to Stacking and AdaBoost" },
  { name: "K-Means Elbow & Silhouette", file: "kmeans_elbow_and_silhouette.png", desc: "Automated WCSS sweep confirming optimal K=3 clusters" },
  { name: "K-Means Cluster Scatter", file: "kmeans_cluster_scatter.png", desc: "Visualizing 3 operating regimes in SOH vs Internal Impedance space" }
];

export default function ReportsDocumentation() {
  const [activeSection, setActiveSection] = useState('syllabus'); // 'syllabus' | 'math' | 'figures'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 text-sm font-semibold tracking-wider uppercase mb-1">
            <BookOpen className="w-4 h-4" /> Academic Documentation & Laboratory Report
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            VoltGuard AI Engineering Dossier
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Third Year B.E. / B.Tech Computer Science (Artificial Intelligence & Machine Learning) Mini-Project.
          </p>
        </div>

        {/* Section Navigation */}
        <div className="flex bg-slate-900 border border-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveSection('syllabus')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeSection === 'syllabus' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Syllabus Mapping (P1–P7)
          </button>
          <button
            onClick={() => setActiveSection('math')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeSection === 'math' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Mathematical Formulations
          </button>
          <button
            onClick={() => setActiveSection('figures')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeSection === 'figures' 
                ? 'bg-cyan-500 text-slate-950 shadow-md' 
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Academic Plots & Figures
          </button>
        </div>
      </div>

      {/* SECTION 1: SYLLABUS MAPPING */}
      {activeSection === 'syllabus' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-base font-semibold text-white">Curriculum Integration Matrix</h3>
                <p className="text-xs text-slate-400">
                  Direct traceability from academic laboratory syllabus practicals to production code and UI endpoints.
                </p>
              </div>
              <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded-full">
                7 / 7 Practicals Fully Integrated
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="py-3 px-4 font-semibold">Practical</th>
                    <th className="py-3 px-4 font-semibold">Topic & AI Branch</th>
                    <th className="py-3 px-4 font-semibold">Backend Implementation File</th>
                    <th className="py-3 px-4 font-semibold">API Router Endpoint</th>
                    <th className="py-3 px-4 font-semibold">Frontend View</th>
                    <th className="py-3 px-4 font-semibold">Empirical Benchmark</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {PRACTICALS_MAP.map((item, idx) => (
                    <tr key={idx} className="hover:bg-slate-800/40">
                      <td className="py-3 px-4 font-bold text-cyan-400 whitespace-nowrap">{item.num}</td>
                      <td className="py-3 px-4 text-white font-medium">
                        <div>{item.title}</div>
                        <span className="text-[10px] text-slate-500 font-normal">{item.branch}</span>
                      </td>
                      <td className="py-3 px-4 text-slate-300 text-[11px]">{item.file}</td>
                      <td className="py-3 px-4 text-purple-400 text-[11px]">{item.api}</td>
                      <td className="py-3 px-4 text-blue-400 text-[11px] whitespace-nowrap">{item.ui}</td>
                      <td className="py-3 px-4 text-emerald-400 text-[11px]">{item.result}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Academic Project Summary Card */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-2">
              <div className="text-xs text-slate-500 uppercase font-bold">Research Dataset</div>
              <div className="text-sm font-bold text-white">NASA Ames Li-ion Prognostics Center</div>
              <p className="text-xs text-slate-400">
                18650 Commercial cells (B0005, B0006, B0007, B0018) cycled under CC-CV charge and 2.0A discharge regimes.
              </p>
            </div>

            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-2">
              <div className="text-xs text-slate-500 uppercase font-bold">Validation Rigor</div>
              <div className="text-sm font-bold text-white">Battery-Grouped Split (Zero Leakage)</div>
              <p className="text-xs text-slate-400">
                Trained exclusively on cells B0005, B0006, and B0007. Evaluated on completely unseen physical cell B0018.
              </p>
            </div>

            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 space-y-2">
              <div className="text-xs text-slate-500 uppercase font-bold">Architecture</div>
              <div className="text-sm font-bold text-white">Decoupled Microservice Architecture</div>
              <p className="text-xs text-slate-400">
                FastAPI asynchronous Python backend with SQLAlchemy persistence paired with React 18 / Tailwind CSS client.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* SECTION 2: MATHEMATICAL FORMULATIONS */}
      {activeSection === 'math' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* SOH & RUL */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-3">
              <h3 className="text-sm font-bold text-cyan-400 uppercase tracking-wider">
                1. State of Health (SOH) & Remaining Useful Life (RUL)
              </h3>
              <p className="text-xs text-slate-300">
                State of Health expresses the current discharge capacity as a percentage of initial manufacturer rated nominal capacity:
              </p>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-cyan-300">
                {"SOH(k) = [ C_discharge(k) / C_nominal ] * 100%"}
                <br />
                {"where C_nominal = 2.0 Ahr (NASA 18650 Spec)"}
              </div>
              <p className="text-xs text-slate-400">
                Remaining Useful Life represents the cycle differential until battery capacity reaches the internationally certified End-of-Life (EOL) safety boundary (70% SOH = 1.40 Ahr):
              </p>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-emerald-300">
                {"RUL(k) = k_EOL - k"}
                <br />
                {"where k_EOL = min { k | SOH(k) <= 70.0% }"}
              </div>
            </div>

            {/* Manual Gradient Descent */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-3">
              <h3 className="text-sm font-bold text-cyan-400 uppercase tracking-wider">
                2. First-Principles Batch Gradient Descent (P3)
              </h3>
              <p className="text-xs text-slate-300">
                Linear model hypothesis with analytical gradient updates minimizing Mean Squared Error (MSE) objective function:
              </p>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-amber-300">
                {"Loss J(w, b) = (1 / 2m) * sum_{i=1}^m [ (w*x^(i) + b) - y^(i) ]^2"}
              </div>
              <p className="text-xs text-slate-400">
                Partial derivative updates with learning rate α and early stopping convergence check:
              </p>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-amber-400">
                {"dJ/dw = (1/m) * sum_{i=1}^m (y_hat^(i) - y^(i)) * x^(i)"}
                <br />
                {"dJ/db = (1/m) * sum_{i=1}^m (y_hat^(i) - y^(i))"}
                <br />
                {"w := w - alpha * dJ/dw,  b := b - alpha * dJ/db"}
              </div>
            </div>

            {/* A* Search & Heuristic Admissibility */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-3">
              <h3 className="text-sm font-bold text-cyan-400 uppercase tracking-wider">
                3. A* Informed Search & Heuristic Admissibility (P2)
              </h3>
              <p className="text-xs text-slate-300">
                A* search expands the node in the priority queue with the lowest total estimated path cost f(n):
              </p>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-purple-300">
                {"f(n) = g(n) + h(n)"}
                <br />
                {"g(n): Exact path cost accumulated from start state"}
                <br />
                {"h(n): Estimated remaining cost to reach certified state"}
              </div>
              <p className="text-xs text-slate-400">
                To guarantee absolute cost optimality, the heuristic must be <strong>admissible</strong>:
              </p>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-purple-400">
                {"For all nodes n:  0 <= h(n) <= h*(n)"}
                <br />
                {"where h*(n) is the true minimal cost to goal"}
              </div>
            </div>

            {/* Ensemble Stacking */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-3">
              <h3 className="text-sm font-bold text-cyan-400 uppercase tracking-wider">
                4. Out-of-Fold Stacking Meta-Classifier (P5)
              </h3>
              <p className="text-xs text-slate-300">
                Prevents data leakage by training meta-features using 5-fold cross-validation on the base models (SVM, Decision Tree, KNN, Naive Bayes):
              </p>
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs text-blue-300">
                {"z_i = [ M_svm(x_i), M_dt(x_i), M_knn(x_i), M_nb(x_i) ]"}
                <br />
                {"P(y=c | z_i) = softmax( W_meta * z_i + b_meta )"}
              </div>
              <p className="text-xs text-slate-400">
                The L2-regularized Logistic Regression meta-learner assigns optimal weights to each base classifier's predictions, achieving lowest overall log-loss (1.1602).
              </p>
            </div>
          </div>
        </div>
      )}

      {/* SECTION 3: FIGURES & PLOTS */}
      {activeSection === 'figures' && (
        <div className="space-y-6">
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6">
            <h3 className="text-base font-semibold text-white mb-2">Academic Visualizations Gallery</h3>
            <p className="text-xs text-slate-400 mb-6">
              Diagnostic plots generated directly from the Python ML training pipelines in <code>backend/ml/</code> and saved into <code>docs/figures/</code>.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {FIGURES.map((fig, idx) => (
                <div key={idx} className="bg-slate-950 rounded-xl border border-slate-800 overflow-hidden hover:border-cyan-500/50 transition-all flex flex-col justify-between">
                  <div className="p-4 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded">
                        Figure {idx + 1}
                      </span>
                      <BarChart2 className="w-4 h-4 text-slate-500" />
                    </div>
                    <h4 className="text-xs font-bold text-white">{fig.name}</h4>
                    <p className="text-[11px] text-slate-400">{fig.desc}</p>
                  </div>
                  <div className="p-3 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-[11px]">
                    <span className="font-mono text-slate-500 truncate max-w-[130px]">{fig.file}</span>
                    <a
                      href={`/figures/${fig.file}`}
                      target="_blank"
                      rel="noreferrer"
                      className="text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1"
                    >
                      View <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
