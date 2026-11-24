"""
VoltGuard AI - Dataset API Router
Provides endpoints for dataset inspection, summary statistics, and CSV uploads.
"""

import os
import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Dict, Any, List, Optional

from backend.app.config import CLEANED_CSV_PATH
from backend.app.schemas.battery import DatasetSummaryResponse
from backend.ml.preprocessing.data_loader import load_cleaned_dataset, NOMINAL_CAPACITY, EOL_CAPACITY_THRESHOLD

router = APIRouter(prefix="/api/dataset", tags=["Dataset"])


@router.get("/summary", response_model=DatasetSummaryResponse)
def get_dataset_summary():
    """
    Returns summary statistics for the benchmark NASA battery dataset.
    """
    df = load_cleaned_dataset()
    cat_counts = df["health_category"].value_counts().to_dict()

    return DatasetSummaryResponse(
        total_records=len(df),
        batteries=sorted(df["battery_id"].unique().tolist()),
        features_count=len(df.columns),
        average_soh=round(float(df["soh"].mean()), 2),
        average_rul=round(float(df["rul"].mean()), 1),
        health_distribution=cat_counts,
        nominal_capacity=NOMINAL_CAPACITY,
        eol_threshold_soh=round((EOL_CAPACITY_THRESHOLD / NOMINAL_CAPACITY) * 100.0, 1)
    )


@router.get("/records")
def get_dataset_records(
    battery_id: Optional[str] = Query(None, description="Filter by battery ID (e.g. B0005)"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0)
):
    """
    Returns paginated battery cycle records.
    """
    df = load_cleaned_dataset()
    if battery_id:
        df = df[df["battery_id"] == battery_id]

    total = len(df)
    subset = df.iloc[offset:offset + limit]

    return {
        "total_records": total,
        "offset": offset,
        "limit": limit,
        "records": subset.to_dict(orient="records")
    }


@router.post("/upload-csv")
async def upload_battery_csv(file: UploadFile = File(...)):
    """
    Validates and processes an uploaded battery cycle CSV file.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files (.csv) are accepted.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        required_cols = ["voltage_mean", "temperature_max", "discharge_duration", "internal_impedance"]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise HTTPException(status_code=422, detail=f"Missing essential battery telemetry columns: {missing}")

        return {
            "filename": file.filename,
            "status": "VALID",
            "rows_detected": len(df),
            "columns": df.columns.tolist(),
            "preview": df.head(5).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
