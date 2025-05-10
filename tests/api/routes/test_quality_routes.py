"""Tests for Quality API routes."""
import pytest
from fastapi.testclient import TestClient
import tempfile
import os

from src.api.main import app
from src.data.repository import ArchitectureRepository


class TestQualityRoutes:
    """Test suite for Quality routes."""
    
    def setup_method(self):
        """Set up test environment."""
        self.client = TestClient(app)
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        
        # Mock the repository to use the temporary file
        from src.api.dependencies import get_repository
        self.test_repo = ArchitectureRepository(self.temp_file.name)
        app.dependency_overrides[get_repository] = lambda: self.test_repo
    
    def teardown_method(self):
        """Clean up test environment."""
        app.dependency_overrides.clear()
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_quality(self):
        """Test creating a new quality requirement."""
        quality_data = {
            "id": "QR-001",
            "title": "Performance Requirements",
            "description": "System should respond within 200ms",
            "metrics": [
                {
                    "name": "Response Time",
                    "target": "< 200ms",
                    "measure": "Average response time"
                }
            ],
            "priority": "high",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        response = self.client.post("/api/qualities", json=quality_data)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "QR-001"
        assert data["title"] == "Performance Requirements"
    
    def test_get_quality(self):
        """Test getting a specific quality requirement."""
        # First create a quality
        quality_data = {
            "id": "QR-001",
            "title": "Performance Requirements",
            "description": "System should respond within 200ms",
            "metrics": [],
            "priority": "high",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        self.client.post("/api/qualities", json=quality_data)
        
        # Now get it
        response = self.client.get("/api/qualities/QR-001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "QR-001"
        assert data["title"] == "Performance Requirements"
    
    def test_update_quality(self):
        """Test updating a quality requirement."""
        # Create a quality
        quality_data = {
            "id": "QR-001",
            "title": "Performance Requirements",
            "description": "System should respond within 200ms",
            "priority": "medium",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        self.client.post("/api/qualities", json=quality_data)
        
        # Update it
        updated_data = quality_data.copy()
        updated_data["priority"] = "high"
        updated_data["description"] = "System should respond within 100ms"
        
        response = self.client.put("/api/qualities/QR-001", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["priority"] == "high"
        assert data["description"] == "System should respond within 100ms"
    
    def test_delete_quality(self):
        """Test deleting a quality requirement."""
        # Create a quality
        quality_data = {
            "id": "QR-001",
            "title": "Performance Requirements",
            "description": "System should respond within 200ms",
            "priority": "high",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        self.client.post("/api/qualities", json=quality_data)
        
        # Delete it
        response = self.client.delete("/api/qualities/QR-001")
        assert response.status_code == 204
        
        # Verify it's gone
        response = self.client.get("/api/qualities/QR-001")
        assert response.status_code == 404
    
    def test_list_qualities(self):
        """Test listing all quality requirements."""
        # Create a couple of qualities
        quality1_data = {
            "id": "QR-001",
            "title": "Performance Requirements",
            "description": "System should respond within 200ms",
            "priority": "high",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        quality2_data = {
            "id": "QR-002",
            "title": "Security Requirements",
            "description": "System should be secure",
            "priority": "high",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        self.client.post("/api/qualities", json=quality1_data)
        self.client.post("/api/qualities", json=quality2_data)
        
        # List all qualities
        response = self.client.get("/api/qualities")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(quality["id"] == "QR-001" for quality in data)
        assert any(quality["id"] == "QR-002" for quality in data)
