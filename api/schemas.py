from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    database: str
    model: str
    model_version: str | None = None


class MetricsResponse(BaseModel):
    mae: float
    rmse: float
    test_rows: int
    model_version: str


class DailyMetricItem(BaseModel):
    metric_date: str
    total_sales: float
    total_profit: float | None
    total_quantity: int
    order_count: int
    avg_order_value: float | None


class PredictionItem(BaseModel):
    predict_date: str
    predicted_sales: float
    actual_sales: float | None
    model_version: str


class PredictRequest(BaseModel):
    day_of_week: int = Field(ge=0, le=6, description="0=Monday, 6=Sunday")
    month: int = Field(ge=1, le=12)
    lag_sales_1: float = Field(ge=0)
    lag_sales_7: float = Field(ge=0)
    rolling_mean_7: float = Field(ge=0)
    order_count: int = Field(ge=1)
    total_quantity: int = Field(ge=1)


class PredictResponse(BaseModel):
    predicted_sales: float
    model_version: str
