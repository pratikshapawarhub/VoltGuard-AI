# VoltGuard AI: Interactive Demonstration & Examination Guide
## How to Demonstrate Every Practical Through the Commercial Product Interface

**Document ID:** `DEMO-VG-2026-V1`  
**Target Audience:** Academic Examiners, Viva Defense Committees, Technical Evaluators, Industry Reviewers  
**Platform:** VoltGuard AI – Intelligent Battery Health & Predictive Maintenance Platform  
**Date:** November 23, 2026  

---

## 1. Quick Environment Launch

Ensure both backend and frontend servers are executing:

```bash
# Terminal 1: Launch FastAPI Asynchronous Backend
python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Launch Vite React 18 Industrial Dashboard
cd frontend
npm run dev
```

- **Open Web Application:** [http://localhost:5173](http://localhost:5173)
- **Open Swagger API Specification:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 2. Step-by-Step Practical Demonstration Walkthrough

---

### Demonstrating Practical 1: PEAS Descriptors & Rule-Based Expert System
*Integrated Feature: Intelligent Battery Monitoring Agent & Alerts Center*

1. **Where to Navigate:** Click **Alerts & Notifications** on the sidebar, or navigate directly to **Academic Traceability → Practical 1**.
2. **What to Show the Examiner:**
   - **PEAS Specification:** Review the 4 pillars:
     - *Performance (P):* SOH $R^2 \ge 0.95$, RUL MAE $<20$ cycles, 100% thermal runaway recall.
     - *Environment (E):* NASA 18650 Li-ion cells, partially observable, stochastic, sequential aging.
     - *Actuators (A):* High-voltage interlock cutoff, charge rate throttling, work order dispatch.
     - *Sensors (S):* Surface thermocouples ($T$), precision ADC ($V$), current shunts ($I$), EIS ($Z$).
   - **Live Rule Engine Simulator:**
     - Select the **"Thermal Stress Alert"** preset ($T_{\text{max}} = 49.5^\circ\text{C}$).
     - Click **"Run Forward-Chaining Inference"**.
     - Point out the instant **CRITICAL Severity** banner and triggered rule `R01`: `EMERGENCY_COOLING_DISCONNECT`.
     - Point out the explanation: *"Thermal runaway protection triggered (T_max >= 42.0°C). Emergency load disconnect & activate maximum auxiliary cooling."*
     - Show the **Forward-Chaining Audit Log** trace displaying evaluation order.
3. **Key Viva Talking Point:**
   > *"The expert system uses forward chaining with strict priority inheritance: safety-critical thermal cutoff rules override operational efficiency rules, guaranteeing zero thermal runaway false negatives."*

---

### Demonstrating Practical 2: Problem Solving Through Search & CSP
*Integrated Feature: Predictive Maintenance Center & Fleet Dispatch*

1. **Where to Navigate:** Click **Maintenance Center** on the sidebar, or view the interactive comparative workbench under **Academic Traceability → Practical 2**.
2. **What to Show the Examiner:**
   - **A\* Informed Search Optimality:**
     - Point out the **Cost-Optimal Servicing Trajectory** card.
     - Highlight the optimal cost of **$130.0** discovered by A* using the admissible heuristic ($h(n) \le h^*(n)$).
     - Contrast with uninformed search: BFS produces a 5-step path costing **$170.0**, while DFS explores expensive disassembly paths costing **$205.0**.
   - **Constraint Satisfaction Problem (CSP) Matrix:**
     - Review the **Scheduled Work Orders** table.
     - Highlight how critical tasks for batteries `B0006` and `B0018` are strictly assigned to Senior Specialist Alice in early morning slots, while Bob (Junior) is assigned routine rebalancing, achieving **0 constraint violations** and **0 backtracks** using the Minimum Remaining Values (MRV) heuristic.
   - **Hill Climbing Local Risk Minimization:**
     - Point out the Fleet Risk Score card showing an initial un-ordered risk of **1464.0** dropping to **1008.75** (a **31.1% risk reduction**) in 24 iterations.
3. **Key Viva Talking Point:**
   > *"A* achieves guaranteed cost optimality because the heuristic lower-bounds the true remaining maintenance cost. Uninformed BFS only optimizes step count, which misses cheaper multi-step reconditioning paths."*

---

### Demonstrating Practical 3: Regression Models for SOH & RUL Prognosis
*Integrated Feature: Predictive Intelligence Engine (Continuous Prognostics)*

1. **Where to Navigate:** Click **Predictive Intelligence** on the sidebar.
2. **What to Show the Examiner:**
   - **Live Multi-Model Inference:**
     - Click **"Run Diagnosis"** on the pre-filled operational telemetry.
     - Point out the **State of Health (SOH %)** card:
       - Sklearn Linear Regression: **99.68% $R^2$**, MAE $0.34\%$.
       - Manual Gradient Descent (built from first principles without libraries): **94.29% $R^2$**, MAE $1.76\%$.
       - Random Forest Regressor: **86.85% $R^2$**, MAE $2.26\%$.
     - Point out the **Remaining Useful Life (RUL Cycles)** card:
       - Highlight that Manual Gradient Descent achieved top cross-cell generalization with an MAE of **18.37 cycles**, satisfying the syllabus requirement of $\text{MAE} < 20$ cycles.
   - **Mathematical Grounding:**
     - Explain the batch gradient update equations implemented in [`manual_gradient_descent.py`](file:///c:/Users/Dell/Desktop/VoltGuard/backend/ml/practical3/manual_gradient_descent.py):
       $$w := w - \alpha \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)}) x_j^{(i)}$$
3. **Key Viva Talking Point:**
   > *"We did not simply call `LinearRegression().fit()`. We implemented Batch Gradient Descent from mathematical first principles with analytical loss gradients and early stopping convergence checks."*

---

### Demonstrating Practical 4: Battery Condition Classification
*Integrated Feature: Predictive Intelligence Engine (Discrete Health Assessment)*

1. **Where to Navigate:** Scroll down to the **Condition Classification** section in **Predictive Intelligence**.
2. **What to Show the Examiner:**
   - **4-Class Degradation Prediction:**
     - Review the predicted operational state: **Healthy** ($\ge 90\%$), **Moderate** ($80\text{--}90\%$), **Degraded** ($70\text{--}80\%$), or **Critical** ($< 70\%$).
     - Review the posterior probability distribution bar chart across all four classes.
   - **Model Comparison Table:**
     - Highlight the benchmark on unseen test cell B0018:
       - **Decision Tree:** Top test accuracy at **71.97%** and Macro F1 of **0.6090**.
       - **Support Vector Machine (SVM):** Best probability calibration with a test Log Loss of **1.226**.
       - **Naive Bayes:** 57.58% accuracy.
       - **K-Nearest Neighbors (KNN):** 38.64% accuracy (struggles due to cross-cell impedance offsets).
3. **Key Viva Talking Point:**
   > *"Decision Tree excels because battery degradation exhibits distinct threshold cliffs (e.g. impedance crossing $0.17\,\Omega$). SVM provides the smoothest calibrated probabilities via Platt scaling."*

---

### Demonstrating Practical 5: Ensemble Learning (Stacking, AdaBoost, Voting)
*Integrated Feature: Predictive Intelligence Engine (Multi-Model Consensus)*

1. **Where to Navigate:** Scroll to the **Ensemble Learning & Consensus** card in **Predictive Intelligence**.
2. **What to Show the Examiner:**
   - **Stacking Meta-Classifier:**
     - Show the consensus category and the comparison between Stacking, AdaBoost, and Hard Voting.
     - Point out the 7-model comparative benchmark: Stacking matches Decision Tree's **71.97% Accuracy** while reducing test Log Loss from **5.340 down to 1.1602**—the lowest loss across all 7 evaluated models.
   - **Leakage Prevention:**
     - Explain how 5-fold stratified out-of-fold cross-validation was used on the training set to generate meta-features, preventing the meta-learner from overfitting.
3. **Key Viva Talking Point:**
   > *"Individual decision trees suffer from extreme, overconfident probability outputs at leaf nodes (yielding high log loss). Stacking with an $L_2$-regularized Logistic Regression meta-classifier optimally weights base predictions to achieve superior probability calibration."*

---

### Demonstrating Practical 6: Unsupervised Clustering & Operating Regimes
*Integrated Feature: Analytics & Regimes (Module 5)*

1. **Where to Navigate:** Click **Analytics & Regimes** on the sidebar.
2. **What to Show the Examiner:**
   - **Discovered Operating Regimes ($K=3$):**
     - *Cluster 1 (Fresh Baseline, 34.0% of cycles):* SOH $90.74\%$, Impedance $0.1202\,\Omega$, Cycle $29.1$.
     - *Cluster 0 (Active Intermediate Aging, 31.1% of cycles):* SOH $77.12\%$, Impedance $0.1442\,\Omega$, Cycle $80.0$.
     - *Cluster 2 (Degraded / High-Impedance EOL, 34.9% of cycles):* SOH $69.49\%$, Impedance $0.1565\,\Omega$, Cycle $131.7$.
   - **Elbow Method & Silhouette Validation:**
     - Review the **Inertia (WCSS) Elbow Curve** displaying the sharp inflection elbow at $K=3$ ($\text{WCSS} = 985.64$).
     - Review the Silhouette Score peak at $0.3608$ and Davies-Bouldin index of $1.0584$.
   - **Zero Label Leakage:**
     - Emphasize that K-Means was trained strictly without health category labels, proving that the algorithm naturally discovered electrochemical aging physics.
3. **Key Viva Talking Point:**
   > *"The clustering algorithm discovered the three physical stages of battery life—fresh baseline, progressive active aging, and high-impedance end-of-life—entirely through unsupervised pattern recognition."*

---

### Demonstrating Practical 7: Complete Integrated Platform & SaaS Workflows
*Integrated Feature: End-to-End Enterprise Experience*

1. **Fleet Overview Dashboard (Module 1):**
   - Click **Fleet Overview** to demonstrate real-time rollups: registered assets, average SOH, critical batteries, degradation curves, and active alerts.
2. **Battery Asset Management (Module 2):**
   - Click **Battery Assets**.
   - Show the grid of commercial assets (`B0005`, `B0006`, `B0007`, `B0018`, `EV-PACK-01`).
   - Click **"Register New Battery"**; enter ID `PACK-TEST-01`, Name `Emergency Generator Backup`, Chemistry `LFP`, Capacity `100.0`.
   - Submit and show the new battery appearing immediately in the registry and database.
   - Click **"Inspect"** to reveal the detailed technical specifications and diagnostic cycle history drawer.
3. **Alerts & Notifications Center (Module 7):**
   - Click **Alerts & Notifications**.
   - Show the active anomaly ledger.
   - Click **"Acknowledge"** on an alert, then click **"Resolve Alert"**; observe the status update persisted to SQLite in real time.
4. **Maintenance Center (Module 6):**
   - Click **Maintenance Center**.
   - Show live work orders (`TASK-B0006-01`, `TASK-B0018-02`).
   - Click **"Start"** to move task to `IN_PROGRESS`, then **"Complete"** to mark it `COMPLETED`.
5. **Reports & Exports (Module 8):**
   - Click **Reports & Exports**.
   - Click **"Export Assets CSV"** or **"Export Diagnostics CSV"**; open the downloaded CSV file to verify real structured data streams.
6. **Academic Curriculum Mapping:**
   - Click the **Academic Traceability** button in the navbar or sidebar footer.
   - Show the examiner the interactive dossier detailing all 7 practicals, exact source files, and live execution evidence.

---

## 3. High-Scoring Viva Defense Answers

**Q1: How do you guarantee there is no data leakage in your evaluation?**
> *"In time-series battery prognostics, randomly splitting cycles causes leakage because cycles from the same battery share identical physical offsets. VoltGuard AI strictly enforces a battery-wise grouped split: cells B0005, B0006, and B0007 are used exclusively for training, while cell B0018 is held out entirely as an unseen physical unit for testing."*

**Q2: What is the mathematical definition of SOH and RUL in this system?**
> *"State of Health is defined as $\text{SOH}(k) = \frac{C_{\text{discharge}}(k)}{C_{\text{nominal}}} \times 100\%$, where $C_{\text{nominal}} = 2.0\,\text{Ahr}$. Remaining Useful Life is defined as $\text{RUL}(k) = k_{\text{EOL}} - k$, where $k_{\text{EOL}}$ is the cycle index where SOH drops permanently below $70.0\%$ ($1.40\,\text{Ahr}$)."*

**Q3: Why is A* search superior to BFS in this application?**
> *"BFS is step-optimal (minimizing transition edges), not cost-optimal. In battery repair, a 4-step path involving full module teardown may cost \$205, whereas a 5-step path involving preliminary scanning and rebalancing costs only \$130. A* evaluates $f(n) = g(n) + h(n)$ with an admissible heuristic, guaranteeing discovery of the lowest dollar-cost maintenance plan."*

---
*Guide approved for student defense and examiner demonstration.*
