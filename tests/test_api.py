import numpy as np
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

N_CYCLES = 10
FAKE_PS2 = np.random.rand(N_CYCLES, 6000).astype(np.float32)
FAKE_FS1 = np.random.rand(N_CYCLES, 600).astype(np.float32)

FAKE_PIPELINE = MagicMock()
FAKE_PIPELINE.predict.return_value = np.array([1])
FAKE_PIPELINE.predict_proba.return_value = np.array([[0.1, 0.9]])


@pytest.fixture
def client():
    with patch("app.main.load_ps2", return_value=FAKE_PS2), \
         patch("app.main.load_fs1", return_value=FAKE_FS1), \
         patch("app.main.load_model", return_value=FAKE_PIPELINE):
        from app.main import app
        with TestClient(app) as c:
            yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["n_cycles"] == N_CYCLES


def test_index_returns_html(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Maintenance" in r.text


def test_predict_valid_cycle(client):
    r = client.post("/predict", json={"cycle_id": 0})
    assert r.status_code == 200
    body = r.json()
    assert body["cycle_id"] == 0
    assert body["prediction"] in (0, 1)
    assert 0.0 <= body["probability_optimal"] <= 1.0


def test_predict_last_cycle(client):
    r = client.post("/predict", json={"cycle_id": N_CYCLES - 1})
    assert r.status_code == 200


def test_predict_out_of_bounds(client):
    r = client.post("/predict", json={"cycle_id": N_CYCLES})
    assert r.status_code == 404
    assert "hors limites" in r.json()["detail"]


def test_predict_negative_cycle(client):
    r = client.post("/predict", json={"cycle_id": -1})
    assert r.status_code == 422


def test_predict_missing_body(client):
    r = client.post("/predict", json={})
    assert r.status_code == 422
