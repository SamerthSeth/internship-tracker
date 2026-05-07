"""Smoke tests for core API availability."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    """Health endpoint should be reachable."""
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_docs_endpoint() -> None:
    """OpenAPI docs endpoint should be reachable."""
    with TestClient(app) as client:
        response = client.get("/api/docs")
    assert response.status_code == 200
