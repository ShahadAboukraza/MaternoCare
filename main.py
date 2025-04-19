from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import numpy as np
from io import StringIO
import re
from typing import List
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

# ================== COLUMN DETECTION ================== #
def detect_sample_column(columns: List[str]) -> str:
    """Identify sample ID column from common naming patterns"""
    patterns = [
        r'sample', r'id', r'patient', r'subject',
        r'case', r'no', r'number', r'code',
        r'^pid', r'^sp', r'^pt', r'^lab'
    ]

    for col in columns:
        col_lower = col.lower()
        if any(re.search(pattern, col_lower) for pattern in patterns):
            return col

    for col in columns:
        if re.match(r'^[a-z]+\d*$', col.lower()):
            return col

    raise ValueError("Cannot identify sample ID column")

def detect_pcb_columns(columns: List[str]) -> List[str]:
    """Identify all PCB-related columns"""
    pcb_cols = []
    for col in columns:
        col_lower = col.lower()
        if any(x in col_lower for x in ['date', 'time', 'id', 'sample']):
            continue
        if (re.search(r'pcb|congener|biphenyl', col_lower) or
            re.search(r'\d{2,3}', col_lower) or
            re.search(r'_\d+[a-z]?$', col_lower)):
            pcb_cols.append(col)

    if not pcb_cols:
        raise ValueError("No PCB columns detected")
    return pcb_cols

# ================== RISK CALCULATION ================== #
def compute_pcb_risk(df: pd.DataFrame, pcb_cols: List[str]) -> pd.DataFrame:
    """Calculate PCB risk metrics"""
    for col in pcb_cols:
        df[col] = (
            df[col].astype(str)
            .str.replace('[<,>]', '', regex=True)
            .astype(float)
        )

    df['Total_PCB'] = df[pcb_cols].sum(axis=1)
    df['ADD'] = df['Total_PCB'] / 1000
    df['LADD'] = df['ADD']
    df['HQ'] = df['ADD'] / 2e-5
    df['CR_high'] = df['LADD'] * 2.0

    # Adjusted thresholds for less sensitivity
    conditions = [
        (df['HQ'] > 5) | (df['CR_high'] > 5e-4),
        df['CR_high'] > 1e-5
    ]
    choices = ['At Risk', 'Needs Monitoring']
    df['Status'] = np.select(conditions, choices, default='Safe')

    # Log actual classification counts
    risk_counts = df['Status'].value_counts().to_dict()
    print("\n🔍 Risk Level Summary:", risk_counts)

    # Debug sample values
    print("\n📊 Sample Risk Values (first 5 rows):")
    print(df[['sample_id', 'Total_PCB', 'ADD', 'HQ', 'CR_high', 'Status']].head())

    return df

# ================== API ENDPOINT ================== #
@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    try:
        try:
            df = pd.read_csv(file.file)
            if df.empty:
                raise HTTPException(400, "Empty CSV file")
        except Exception as e:
            raise HTTPException(400, f"CSV parsing error: {str(e)}")

        try:
            sample_col = detect_sample_column(df.columns.tolist())
            pcb_cols = detect_pcb_columns(df.columns.tolist())
            df = df.rename(columns={sample_col: 'sample_id'})
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Column detection failed: {str(e)}. "
                      f"Available columns: {df.columns.tolist()}"
            )

        result_df = compute_pcb_risk(df, pcb_cols)

        output = StringIO()
        result_df.to_csv(output, index=False)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=risk_analysis.csv"}
        )

    except pd.errors.ParserError:
        raise HTTPException(400, "Invalid CSV format")
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise HTTPException(500, f"Processing error: {str(e)}")

@app.get("/")
def health_check():
    return {"status": "active", "version": "1.0"}
