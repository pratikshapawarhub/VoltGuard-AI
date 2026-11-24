import React, { useState } from 'react';
import { 
  BookOpen, Code, Layers, CheckCircle2, Award, 
  ExternalLink, FileText, Cpu, ChevronRight, BarChart2
} from 'lucide-react';

const PRACTICALS = [
  {
    practical_num: "Practical 1",
    syllabus_title: "PEAS Descriptors and Expert System",
    product_module: "Intelligent Battery Monitoring Agent (Alerts & Rule Engine)",
    algorithms: "Russell & Norvig PEAS Specification, Forward-Chaining Deductive Inference Engine with 9 Production Rules",
    source_file: "backend/ml/practical1/expert_system.py",
    secondary_file: "backend/ml/practical1/peas.py",
    main_functions: "BatteryExpertSystem.evaluate(facts), Rule.evaluate(), get_peas_description()",
    input_data: "Cycle telemetry facts: soh, temperature_max, internal_impedance, voltage_min, voltage_max, recent_soh_drop",
    output: "ExpertSystemResponse (overall_status, condition_summary, triggered_rules list, prioritized action codes, audit trail)",
    evaluation: "Deterministic forward-chaining rules with safety override priority (Critical > Warning > Info). 100% Thermal Runaway Recall.",
    execution_evidence: "39/39 automated pytest validations passing; evaluated in live engine transactions and persisted to database.",
    figure_ref: "docs/figures/soh_degradation_curves.png"
  },
  {
    practical_num: "Practical 2",
    syllabus_title: "Problem Solving through Search & CSP",
    product_module: "Predictive Maintenance Center & Fleet Dispatch",
    algorithms: "Breadth-First Search (BFS), Depth-First Search (DFS), A* Informed Search, Hill Climbing Local Search, Backtracking CSP with MRV",
    source_file: "backend/ml/practical2/informed_search.py",
    secondary_file: "backend/ml/practical2/uninformed_search.py, local_search.py, csp_solver.py",
    main_functions: "run_a_star(), run_bfs(), run_dfs(), run_hill_climbing(), run_csp_solver()",
    input_data: "Maintenance state graph (12 nodes, weighted repair costs), heuristic vector h(n), technician-slot constraints",
    output: "Cost-optimal maintenance trajectory, fleet risk reduction (%), conflict-free technician slot assignments",
    evaluation: "A* found cost-optimal path at $130.0 (vs BFS $170.0 and DFS $205.0); Hill Climbing reduced fleet risk by 31.1% in 24 iterations; CSP solved with 0 backtracks.",
    execution_evidence: "Saved in backend/saved_models/search_comparison.json, verified in test_practical2_search.py.",
    figure_ref: "docs/figures/soh_degradation_curves.png"
  },
  {
    practical_num: "Practical 3",
    syllabus_title: "Regression Model Evaluation for SOH & RUL",
    product_module: "Predictive Intelligence: Health & Lifespan Prognosis",
    algorithms: "Manual Batch Gradient Descent from first principles (w, b, analytical gradients, MSE), Sklearn Linear Regression, Random Forest Regressor",
    source_file: "backend/ml/practical3/manual_gradient_descent.py",
    secondary_file: "backend/ml/practical3/linear_regression.py, random_forest_regression.py",
    main_functions: "ManualGradientDescentRegressor.fit(), predict(), calculate_mse(), calculate_gradients()",
    input_data: "13 scaled operational features: cycle number, voltage stats, current stats, thermal peaks, impedance",
    output: "Continuous SOH (% capacity) and RUL (remaining cycles until 70% EOL boundary)",
    evaluation: "Unseen test cell B0018: Sklearn LR SOH R²=0.9968 (MAE 0.34%); Manual GD RUL R²=0.5872 (MAE 18.37 cycles, beating <20 target).",
    execution_evidence: "Serialized to backend/saved_models/soh_manual_gd.joblib, rul_manual_gd.joblib, metrics in regression_metrics.json.",
    figure_ref: "docs/figures/actual_vs_predicted_soh.png, gradient_descent_loss_curve.png"
  },
  {
    practical_num: "Practical 4",
    syllabus_title: "Classification Models for Degradation States",
    product_module: "Battery Condition Assessment (Healthy, Moderate, Degraded, Critical)",
    algorithms: "Support Vector Classifier (RBF kernel, Platt probabilities), Decision Tree Classifier (Gini), K-Nearest Neighbors (K=5), Gaussian Naive Bayes",
    source_file: "backend/ml/practical4/classifiers.py",
    secondary_file: "backend/ml/practical4/train_classification.py",
    main_functions: "BatterySVMClassifier.predict(), BatteryDecisionTreeClassifier.predict_proba()",
    input_data: "13 standard operational features per cycle; ground truth labeled into 4 classes",
    output: "Predicted discrete condition label, class name, and posterior probability distribution",
    evaluation: "Evaluated on unseen test cell B0018: Decision Tree Accuracy 71.97% (Macro F1 0.6090); SVM best log loss calibration (1.226).",
    execution_evidence: "Serialized in backend/saved_models/classification_decision_tree.joblib, classification_metrics.json.",
    figure_ref: "docs/figures/confusion_matrices_all_classifiers.png"
  },
  {
    practical_num: "Practical 5",
    syllabus_title: "Ensemble Learning (Stacking, AdaBoost, Voting)",
    product_module: "Combined Prediction Engine & Multi-Model Consensus",
    algorithms: "Stacking Classifier (5-fold out-of-fold cross-validation with L2-regularized Logistic Regression meta-classifier), AdaBoost (50 decision stumps), Hard Voting",
    source_file: "backend/ml/practical5/ensemble_models.py",
    secondary_file: "backend/ml/practical5/train_ensemble.py",
    main_functions: "BatteryStackingEnsemble.fit(), predict(), predict_proba(), evaluate()",
    input_data: "Base classifier probability vectors (SVM, Decision Tree, KNN, Naive Bayes)",
    output: "Ensemble consensus condition category and meta-learner calibrated probabilities",
    evaluation: "Stacking Meta-Classifier achieved 71.97% Accuracy with lowest test Log Loss (1.1602) across all 7 evaluated models.",
    execution_evidence: "Serialized in backend/saved_models/ensemble_stacking.joblib, ensemble_comparison_metrics.json.",
    figure_ref: "docs/figures/ensemble_vs_base_comparison.png"
  },
  {
    practical_num: "Practical 6",
    syllabus_title: "Clustering Algorithms for Operating Regimes",
    product_module: "Battery Usage Segmentation & Regime Discovery",
    algorithms: "Multi-Feature K-Means Clustering, Automated WCSS Elbow method sweep (K=2..8), Silhouette Coefficient, Davies-Bouldin Index",
    source_file: "backend/ml/practical6/kmeans_clustering.py",
    secondary_file: "backend/ml/practical6/train_clustering.py",
    main_functions: "BatteryKMeansClusterer.fit(), predict_cluster(), compute_elbow_curve()",
    input_data: "Unsupervised features: SOH, discharge capacity, peak temperature, internal impedance, cycle number",
    output: "Cluster ID, regime name (Fresh Baseline, Intermediate Aging, Degraded EOL), cluster centroid distances",
    evaluation: "Optimal K=3 identified via WCSS elbow inflection point (Silhouette 0.3608, Davies-Bouldin 1.0584). Zero label leakage.",
    execution_evidence: "Serialized in backend/saved_models/kmeans_model.joblib, clustering_metrics.json.",
    figure_ref: "docs/figures/kmeans_elbow_and_silhouette.png, kmeans_cluster_scatter.png"
  },
  {
    practical_num: "Practical 7",
    syllabus_title: "Integrated Predictive Maintenance Platform",
    product_module: "Complete VoltGuard AI Enterprise Application",
    algorithms: "End-to-end multi-model inference pipeline integrating P1 through P6, Singleton Registry, SQLite persistence, FastAPI async services, React dashboard",
    source_file: "backend/app/engine/engine.py",
    secondary_file: "backend/app/main.py, frontend/src/App.jsx",
    main_functions: "IntegratedPredictiveEngine.process_battery_sample(), registry.load_all()",
    input_data: "Multi-dimensional battery measurement payload (BatteryMeasurementInput)",
    output: "Unified diagnostic payload: SOH, RUL, Condition, Ensemble, Regime Cluster, Fired Expert Rules, A* Servicing Path, Alert Ledger entry",
    evaluation: "43/43 automated pytest integration tests passing; zero mock data; full asset CRUD and real-time database transactions.",
    execution_evidence: "Live SQLite database at backend/voltguard.db, Swagger documentation at /docs.",
    figure_ref: "docs/figures/regression_models_comparison.png"
  }
];

export default function AcademicMapping() {
  const [selectedPractical, setSelectedPractical] = useState(PRACTICALS[0]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-800 pb-5">
        <div>
          <div className="flex items-center gap-2 text-purple-400 text-xs font-semibold tracking-wider uppercase mb-1">
            <BookOpen className="w-4 h-4" /> Academic Curriculum Traceability
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white tracking-tight">
            Laboratory Practical Implementation Mapping
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Detailed 1-to-1 mapping linking each laboratory syllabus practical (P1 through P7) to its product integration, source code, mathematical formulation, and execution evidence.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-purple-950/40 border border-purple-800/50 text-purple-300 px-3 py-1.5 rounded-xl text-xs font-mono">
          <Award className="w-4 h-4 text-purple-400" />
          <span>7 of 7 Practicals Fully Integrated</span>
        </div>
      </div>

      {/* Main Grid: List on Left, Detail Dossier on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Practicals Selector */}
        <div className="lg:col-span-5 space-y-2">
          {PRACTICALS.map((p) => {
            const isSelected = selectedPractical.practical_num === p.practical_num;
            return (
              <button
                key={p.practical_num}
                onClick={() => setSelectedPractical(p)}
                className={`w-full text-left p-4 rounded-2xl border transition-all flex items-center justify-between ${
                  isSelected
                    ? 'bg-purple-950/30 border-purple-500/50 shadow-md'
                    : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-purple-400 bg-purple-950/60 border border-purple-800/40 px-2 py-0.5 rounded">
                      {p.practical_num}
                    </span>
                    <span className="text-xs font-semibold text-white">
                      {p.syllabus_title}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400 mt-1">
                    Product Integration: <span className="text-cyan-300 font-medium">{p.product_module}</span>
                  </div>
                </div>
                <ChevronRight className={`w-4 h-4 ${isSelected ? 'text-purple-400' : 'text-slate-600'}`} />
              </button>
            );
          })}
        </div>

        {/* Right Column: Detailed Practical Dossier */}
        <div className="lg:col-span-7 bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <span className="text-xs font-mono font-bold text-purple-400 uppercase tracking-wider">
                {selectedPractical.practical_num} Technical Specification
              </span>
              <h2 className="text-lg font-bold text-white mt-0.5">
                {selectedPractical.syllabus_title}
              </h2>
            </div>
            <span className="text-xs text-emerald-400 bg-emerald-950/60 border border-emerald-800/40 px-2.5 py-1 rounded-full flex items-center gap-1 font-mono">
              <CheckCircle2 className="w-3.5 h-3.5" /> Fully Operational
            </span>
          </div>

          {/* Product Module Integration */}
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-1">
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Integrated Commercial Feature</span>
            <div className="text-sm font-bold text-cyan-300">{selectedPractical.product_module}</div>
          </div>

          {/* Algorithms Used */}
          <div className="space-y-1">
            <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">Implemented Algorithms & Techniques</span>
            <p className="text-xs text-slate-200 leading-relaxed font-mono bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              {selectedPractical.algorithms}
            </p>
          </div>

          {/* Exact Source Code Files */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 block text-[11px] uppercase font-semibold">Primary Source File</span>
              <span className="font-mono text-purple-300 font-bold break-all">{selectedPractical.source_file}</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-500 block text-[11px] uppercase font-semibold">Key Functions & Methods</span>
              <span className="font-mono text-slate-300 break-all">{selectedPractical.main_functions}</span>
            </div>
          </div>

          {/* Input & Output Specifications */}
          <div className="space-y-3 text-xs">
            <div>
              <span className="text-slate-500 uppercase font-semibold block text-[11px]">Input Telemetry & Constraints:</span>
              <div className="text-slate-300 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/60 mt-1">
                {selectedPractical.input_data}
              </div>
            </div>
            <div>
              <span className="text-slate-500 uppercase font-semibold block text-[11px]">Output Predictions & Format:</span>
              <div className="text-slate-300 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/60 mt-1">
                {selectedPractical.output}
              </div>
            </div>
          </div>

          {/* Evaluation Method & Evidence */}
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <span className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" /> Empirical Evaluation & Validation Results
            </span>
            <p className="text-xs text-slate-200 leading-relaxed">
              {selectedPractical.evaluation}
            </p>
            <div className="text-[11px] text-slate-400 pt-2 border-t border-slate-800/60">
              <span className="font-semibold text-slate-300">Execution Evidence:</span> {selectedPractical.execution_evidence}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
