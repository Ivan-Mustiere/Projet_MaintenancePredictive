import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline
from src.models.train import build_baseline_pipeline, build_rf_pipeline
from src.models.evaluate import compute_metrics


def _make_data(n=100):
    X = pd.DataFrame(np.random.rand(n, 10), columns=[f"f{i}" for i in range(10)])
    y = pd.Series(np.random.randint(0, 2, n))
    return X, y


def test_baseline_pipeline_fit_predict():
    X, y = _make_data()
    pipe = build_baseline_pipeline()
    pipe.fit(X, y)
    preds = pipe.predict(X)
    assert len(preds) == len(y)


def test_rf_pipeline_fit_predict():
    X, y = _make_data()
    pipe = build_rf_pipeline()
    pipe.fit(X, y)
    assert isinstance(pipe, Pipeline)


def test_compute_metrics_keys():
    y_true = pd.Series([0, 1, 0, 1])
    y_pred = np.array([0, 1, 1, 0])
    metrics = compute_metrics(y_true, y_pred)
    assert {"accuracy", "precision", "recall", "f1"}.issubset(metrics.keys())
