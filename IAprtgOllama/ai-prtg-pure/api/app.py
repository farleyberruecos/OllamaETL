from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import duckdb
import pandas as pd
from datetime import datetime
import asyncio

from core.intelligent_analyzer import IntelligentAnalyzer
from core.data_processor import DataProcessor

app = FastAPI(title="AI-PRTG Pure Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = IntelligentAnalyzer(model="deepseek-coder:6.7b")
data_processor = DataProcessor()

class AnalysisRequest(BaseModel):
    process_name: str
    lookback_days: int = 7

@app.on_event("startup")
async def startup_event():
    await analyzer.initialize()

@app.get("/")
async def root():
    return {"message": "AI-PRTG - Análisis 100% por IA", "version": "1.0"}

@app.post("/analyze")
async def analyze_process(request: AnalysisRequest):
    """Análisis puro por IA"""
    try:
        data = data_processor.get_detailed_data(request.process_name, request.lookback_days)
        
        if data.empty:
            raise HTTPException(404, f"No hay datos para: {request.process_name}")
        
        analysis = await analyzer.analyze_process_intelligently(data, request.process_name)
        
        return {
            "process": request.process_name,
            "timestamp": datetime.now().isoformat(),
            "data_points": len(data),
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.post("/detect-anomalies")
async def detect_anomalies(request: AnalysisRequest):
    """Detección pura por IA"""
    try:
        data = data_processor.get_detailed_data(request.process_name, request.lookback_days)
        
        if data.empty:
            raise HTTPException(404, "No hay datos")
        
        anomalies = await analyzer.detect_anomalies_intelligently(data, request.process_name)
        
        return {
            "process": request.process_name,
            "anomalies": anomalies
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.post("/predict")
async def predict_trend(request: AnalysisRequest):
    """Predicción pura por IA"""
    try:
        data = data_processor.get_detailed_data(request.process_name, request.lookback_days)
        
        if data.empty:
            raise HTTPException(404, "No hay datos")
        
        prediction = await analyzer.predict_trend_intelligently(data, request.process_name)
        
        return {
            "process": request.process_name,
            "prediction": prediction
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    try:
        conn = duckdb.connect('./data/processing.db')
        db_ok = conn.execute("SELECT 1").fetchone() is not None
        conn.close()
        
        ollama_ok = await analyzer.health_check()
        
        return {
            "status": "healthy" if all([db_ok, ollama_ok]) else "degraded",
            "database": "online" if db_ok else "offline",
            "ollama": "online" if ollama_ok else "offline"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
