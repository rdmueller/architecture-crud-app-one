"""Test all routes are registered."""
import pytest
from fastapi.testclient import TestClient

from src.api.main import app


class TestAllRoutes:
    """Test suite to verify all routes are registered."""
    
    def setup_method(self):
        """Set up test environment."""
        self.client = TestClient(app)
    
    def test_all_entity_routes_exist(self):
        """Test that all entity routes are registered."""
        # Test list endpoints
        endpoints = [
            "/api/adrs",
            "/api/qualities",
            "/api/risks",
            "/api/technical-debts",
            "/api/components"
        ]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            assert response.status_code == 200
            assert isinstance(response.json(), list)
    
    def test_openapi_shows_all_routes(self):
        """Test that OpenAPI schema includes all routes."""
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        paths = schema["paths"]
        
        # Check that all entity endpoints are present
        expected_paths = [
            "/api/adrs",
            "/api/adrs/{adr_id}",
            "/api/qualities",
            "/api/qualities/{quality_id}",
            "/api/risks",
            "/api/risks/{risk_id}",
            "/api/technical-debts",
            "/api/technical-debts/{td_id}",
            "/api/components",
            "/api/components/{component_id}"
        ]
        
        for path in expected_paths:
            assert path in paths, f"Path {path} not found in OpenAPI schema"
