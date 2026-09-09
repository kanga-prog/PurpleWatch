"""Tests for the PurpleWatch API health endpoint."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_expected_contract() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "purplewatch-api",
        "version": "0.1.0",
        "environment": "development",
    }


def test_health_returns_json() -> None:
    response = client.get("/health")

    assert response.headers["content-type"].startswith("application/json")
