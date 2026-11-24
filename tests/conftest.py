"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from ai_portfolio.api.main import create_app


@pytest.fixture
def client() -> TestClient:
    """Return a FastAPI TestClient bound to a fresh application instance."""
    return TestClient(create_app())
