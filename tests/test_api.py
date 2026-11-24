"""API tests for the FastAPI `/health` endpoint."""

from fastapi.testclient import TestClient

from ai_portfolio import __version__
from ai_portfolio.config import get_settings


def test_health_endpoint(client: TestClient) -> None:
    """GET /health returns HTTP 200 and expected service metadata."""
    settings = get_settings()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app_name": settings.app_name,
        "version": __version__,
        "environment": settings.environment,
    }
