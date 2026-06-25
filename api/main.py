"""
FastAPI server:
uvicorn api.main:app --reload
"""

from fastapi import Depends, FastAPI, Header, HTTPException

from api import services
from api.schemas import (
    DailyMetricItem,
    HealthResponse,
    MetricsResponse,
    PredictRequest,
    PredictResponse,
    PredictionItem,
)
from config.settings import settings

app = FastAPI(
    title="Sales Forecast API",
    description="ETL + ML pipeline API for sales prediction",
    version="1.0.0",
)


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    db_ok = services.check_database()
    model_info = services.get_model_info()

    return HealthResponse(
        status="ok" if db_ok and model_info["loaded"] else "degraded",
        database="connected" if db_ok else "disconnected",
        model="loaded" if model_info["loaded"] else "not_found",
        model_version=model_info["version"],
    )


@app.get("/metrics", response_model=MetricsResponse, tags=["ML"])
def get_metrics(_: None = Depends(verify_api_key)):
    try:
        return MetricsResponse(**services.compute_metrics())
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.get("/latest-data", response_model=list[DailyMetricItem], tags=["Data"])
def latest_data(limit: int = 10, _: None = Depends(verify_api_key)):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    return services.get_latest_metrics(limit=limit)


@app.get("/predictions", response_model=list[PredictionItem], tags=["ML"])
def predictions(limit: int = 10, _: None = Depends(verify_api_key)):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    return services.get_predictions(limit=limit)


@app.post("/predict", response_model=PredictResponse, tags=["ML"])
def predict(request: PredictRequest, _: None = Depends(verify_api_key)):
    try:
        return PredictResponse(**services.predict_sales(request.model_dump()))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.get("/predict/latest", tags=["ML"])
def predict_latest(_: None = Depends(verify_api_key)):
    try:
        return services.predict_from_latest_day()
    except (FileNotFoundError, ValueError) as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
