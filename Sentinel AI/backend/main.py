from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import pandas as pd
from .pipeline import run_pipeline

app = FastAPI(title="SentinelAI")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), mission: str | None = Form(None)):
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {e}")

    result = run_pipeline(df, mission=mission)
    return result