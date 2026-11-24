# VoltGuard AI: End-to-End Production Deployment Guide

**Document ID:** `DEPLOY-VG-2026-V1`  
**System Name:** VoltGuard AI – Intelligent Battery Health & Predictive Maintenance Platform  
**Target Environments:** Cloud PaaS (Render / Vercel), Containerized (Docker), and Self-Hosted Linux  
**Date:** November 23, 2026  

---

## 1. Overview & Architecture Strategy

VoltGuard AI is engineered as a decoupled modern web application:
- **Backend Service:** FastAPI REST application running on Python (Uvicorn ASGI). Serves 12 API routers, executes machine learning inference, and auto-seeds the SQLite persistence layer (`voltguard.db`).
- **Frontend Client:** Single Page Application (SPA) built with React 18, Vite 6, and Tailwind CSS. Connects to the backend via `VITE_API_URL`.

### Recommended Deployment Model:
1. **Backend on Render.com** (Free Web Service)
2. **Frontend on Vercel.com or Render Static Site** (Free Global Edge CDN)

---

## 2. Step 1: Initialize Git & Push to GitHub

If your project is not yet on GitHub, run the following in your terminal (`C:\Users\Dell\Desktop\VoltGuard`):

```bash
# Initialize git repository
git init

# Configure branch name
git branch -M main

# Stage all files
git add .

# Create initial commit
git commit -m "feat: complete VoltGuard AI enterprise B2B SaaS platform"

# Link to your GitHub repository (replace with your repository URL)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/VoltGuard.git

# Push code to GitHub
git push -u origin main
```

---

## 3. Step 2: Deploy Backend to Render (Free)

Render provides free hosting for Python FastAPI web services with automatic HTTPS and auto-deployments on Git push.

### Step-by-Step Instructions:
1. Go to [Render.com](https://render.com) and log in (sign in with GitHub).
2. Click **New +** and select **Web Service**.
3. Choose **Build and deploy from a Git repository** and connect your `VoltGuard` repository.
4. Fill in the service configuration:
   - **Name:** `voltguard-backend`
   - **Region:** Any (e.g. `Oregon (US West)` or `Frankfurt (EU)`)
   - **Branch:** `main`
   - **Root Directory:** Leave blank (root of the repo)
   - **Runtime:** `Python 3`
   - **Build Command:** 
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** **Free**
5. (Optional) In **Environment Variables**, add:
   - `PYTHON_VERSION` = `3.11.9`
6. Click **Create Web Service**.
7. Wait 2–3 minutes for the build to complete. Once deployed, Render will give you a public URL, for example:
   ```
   https://voltguard-backend.onrender.com
   ```
8. **Verify Backend Deployment:**
   - Open `https://voltguard-backend.onrender.com/` in your browser. You should receive the JSON health status (`"status": "OPERATIONAL"`).
   - Open `https://voltguard-backend.onrender.com/docs` to see the interactive Swagger UI.

---

## 4. Step 3: Deploy Frontend to Vercel (Free)

Vercel provides edge hosting with ultra-fast global CDN for Vite React applications.

### Step-by-Step Instructions:
1. Go to [Vercel.com](https://vercel.com) and sign in with your GitHub account.
2. Click **Add New...** -> **Project**.
3. Import your `VoltGuard` repository.
4. Configure the Project Settings:
   - **Project Name:** `voltguard-ai`
   - **Framework Preset:** `Vite`
   - **Root Directory:** Click **Edit** and select `frontend` (crucial!).
   - **Build and Output Settings:**
     - Build Command: `npm run build`
     - Output Directory: `dist`
5. **Environment Variables:**
   - Expand the **Environment Variables** section.
   - Add:
     - **Key:** `VITE_API_URL`
     - **Value:** `https://voltguard-backend.onrender.com` *(paste your actual Render backend URL without trailing slash)*.
6. Click **Deploy**.
7. Vercel will build the frontend in ~30 seconds and provide your live application URL:
   ```
   https://voltguard-ai.vercel.app
   ```

---

## 5. Alternative Option: 1-Click Unified Render Blueprint

If you prefer to deploy both frontend and backend on Render using the included `render.yaml`:

1. In Render, click **New +** -> **Blueprint**.
2. Select your `VoltGuard` repository.
3. Render will read `render.yaml` and automatically configure:
   - `voltguard-backend` (Web Service)
   - `voltguard-frontend` (Static Site linked to backend)
4. Click **Apply**.

---

## 6. Alternative Option: Docker Container Deployment

If deploying to **Railway**, **Google Cloud Run**, **AWS App Runner**, or a **VPS**:

```bash
# Build the Docker image
docker build -t voltguard-ai:latest .

# Run the container locally or on server
docker run -d -p 8000:8000 -e PORT=8000 --name voltguard voltguard-ai:latest
```

The containerized service will be accessible at `http://localhost:8000`.

---

## 7. Post-Deployment Verification Checklist

Once deployed, verify the following features on the live URL:

| Test Item | Verification Procedure | Expected Outcome |
|:---|:---|:---|
| **API Root** | Visit `https://<backend-url>/` | Returns JSON with `"status": "OPERATIONAL"` |
| **API Docs** | Visit `https://<backend-url>/docs` | Interactive Swagger UI displays all 12 routers |
| **Frontend Health** | Open `https://<frontend-url>/` | Dashboard loads with live KPI cards and battery charts |
| **Asset Registry** | Navigate to Battery Assets | Pre-seeded NASA batteries (`B0005`, `B0006`, etc.) appear |
| **Model Predictions** | Run a test prediction in Predictive Intelligence | SOH and RUL are computed and displayed |
| **Maintenance Work Orders** | Check Maintenance Center | Active tasks and A* path planning operate seamlessly |
| **CSV Reports** | Click Export CSV in Reports Center | Clean CSV file downloads immediately |
