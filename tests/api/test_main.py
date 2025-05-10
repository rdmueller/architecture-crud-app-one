"""Tests for the main FastAPI application."""
import pytest
from fastapi.testclient import TestClient

from src.api.main import app


class TestFastAPIApp:
    """Test suite for FastAPI application."""
    
    def setup_method(self):
        """Set up test environment."""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Architecture CRUD API" in data["message"]
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_openapi_schema(self):
        """Test OpenAPI schema endpoint."""
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "Architecture CRUD API"
    
    def test_cors_headers(self):
        """Test CORS headers."""
        response = self.client.get("/", headers={"Origin": "http://localhost:8501"})
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "*"
