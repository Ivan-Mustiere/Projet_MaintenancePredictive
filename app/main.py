from contextlib import asynccontextmanager
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator

from src.data.load import load_ps2, load_fs1
from src.features.build_features import build_features
from src.models.predict import load_model, predict_cycle

TEMPLATES = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Cache global — chargé une seule fois au démarrage
_cache: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    _cache["ps2"]      = load_ps2()
    _cache["fs1"]      = load_fs1()
    _cache["pipeline"] = load_model()
    _cache["n_cycles"] = _cache["ps2"].shape[0]
    yield
    _cache.clear()


app = FastAPI(
    title="Maintenance Prédictive — Valve Condition API",
    description="Prédit si la condition de la valve est optimale pour un cycle donné.",
    version="0.1.0",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app)


class PredictRequest(BaseModel):
    cycle_id: int = Field(..., ge=0, description="Index du cycle (0-based)")


class PredictResponse(BaseModel):
    cycle_id: int
    prediction: int = Field(..., description="1=optimal, 0=non-optimal")
    probability_optimal: float


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return TEMPLATES.TemplateResponse(request, "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "n_cycles": _cache.get("n_cycles", 0)}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    n = _cache.get("n_cycles", 0)
    if request.cycle_id >= n:
        raise HTTPException(
            status_code=404,
            detail=f"cycle_id {request.cycle_id} hors limites (max={n - 1})",
        )

    ps2 = _cache["ps2"][[request.cycle_id]]
    fs1 = _cache["fs1"][[request.cycle_id]]
    features = build_features(ps2, fs1)

    result = predict_cycle(_cache["pipeline"], features)

    return PredictResponse(
        cycle_id=request.cycle_id,
        prediction=result["prediction"][0],
        probability_optimal=result["probability_optimal"][0],
    )
