from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI(title="Horizon Bed Forecast API")

model = joblib.load(Path("artifacts/model.pkl"))

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
    X = pd.DataFrame([req.dict()])
    y_hat = model.predict(X)[0]
    return ForecastResponse(prediction=float(y_hat))