from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import joblib
import pandas as pd

from horizon_forecast.features.demand_aggregation import build_demand_timeseries

app = FastAPI(title="Horizon Bed Forecast API")

MODEL_PATH = Path("artifacts/model.pkl")
model = joblib.load(MMODEL_PATH)

class ForecastRequest(BaseModel):
    ed_arrivals: float
    elective_surgeries: float
    dow: int
    month: int
    is_weekend: int

class ForecastResponse(BaseModel):
    prediction: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=ForecastResponse)
def predict(req: ForecastRequest):
    data = pd.DataFrame([{
        "ed_arrivals": req.ed_arrivals,
        "elective_surgeries": req.elective_surgeries,
        "dow": req.dow,
        "month": req.month,
        "is_weekend": req.is_weekend,
    }])
    y_hat = model.predict(data)[0]
    return ForecastResponse(prediction=float(y_hat))