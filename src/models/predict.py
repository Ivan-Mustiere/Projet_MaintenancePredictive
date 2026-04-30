import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline
import joblib
from src.utils.config import MODELS_DIR


def load_model(model_name: str = "model.joblib") -> Pipeline:
    path = MODELS_DIR / model_name
    return joblib.load(path)


def predict_cycle(pipeline: Pipeline, features: pd.DataFrame) -> dict:
    """Return prediction and probability for one or more cycles."""
    proba = pipeline.predict_proba(features)[:, 1]
    label = pipeline.predict(features)
    return {
        "prediction": label.tolist(),
        "probability_optimal": proba.tolist(),
    }
