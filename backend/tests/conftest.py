"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from sagatoyai.main import app


@pytest.fixture
def client() -> TestClient:
    """Create test client for API testing."""
    return TestClient(app)
