# import json
from fastapi.testclient import TestClient

from model_server import InferenceServer


def test_predict_endpoint() -> None:
    server = InferenceServer(name="test")
    client = TestClient(server.app)
    response = client.get("/predict")
    assert response.status_code == 200
    data = response.json()
    assert "relevance_scores" in data
    assert data["relevance_scores"] == "test"


def test_missing_endpoint() -> None:
    server = InferenceServer(name="test")
    client = TestClient(server.app)
    response = client.get("/nonexistent")
    assert response.status_code == 404
