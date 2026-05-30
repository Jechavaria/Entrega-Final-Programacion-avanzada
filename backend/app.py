import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, save_metrics, get_latest_metrics, save_prediction, get_recent_predictions
from model import load_model, predict_from_features, train_and_save_model, dataset_path, model_path
from schemas import PredictRequest, PredictResponse, MetricsResponse, PredictionRecord

app = FastAPI(title="Credit Default ML API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok", "dataset": dataset_path(), "model_path": model_path()}


@app.post("/train", response_model=MetricsResponse)
def train():
    metrics = train_and_save_model()
    save_metrics(metrics)
    latest = get_latest_metrics()
    if not latest:
        raise HTTPException(status_code=500, detail="No se guardaron las métricas")
    return latest


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    model = load_model()
    prediction = predict_from_features(model, request.dict())
    save_prediction(request.dict(), prediction["prediction"], prediction["probability"])
    return PredictResponse(**prediction)


@app.get("/metrics", response_model=MetricsResponse)
def metrics():
    latest = get_latest_metrics()
    if not latest:
        raise HTTPException(status_code=404, detail="No se han generado métricas aún")
    return latest


@app.get("/predictions", response_model=list[PredictionRecord])
def predictions():
    return get_recent_predictions(10)


@app.get("/system")
def system_info():
    return {
        "dataset_path": dataset_path(),
        "model_path": model_path(),
        "backend": "fastapi",
    }
