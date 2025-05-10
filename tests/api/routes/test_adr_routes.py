"""Tests for ADR API routes."""
import pytest
from datetime import date
from fastapi.testclient import TestClient
import tempfile
import os

from src.api.main import app
from src.data.repository import ArchitectureRepository
from src.api.models.adr import ADR


class TestADRRoutes:
    """Test suite for ADR routes."""
    
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
    
    def test_create_adr(self):
        """Test creating a new ADR."""
        adr_data = {
            "id": "ADR-001",
            "title": "Use FastAPI for backend",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "We need to choose a web framework",
            "decision": "We will use FastAPI",
            "alternatives": {},
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        response = self.client.post("/api/adrs", json=adr_data)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == "ADR-001"
        assert data["title"] == "Use FastAPI for backend"
    
    def test_create_adr_duplicate(self):
        """Test creating a duplicate ADR."""
        adr_data = {
            "id": "ADR-001",
            "title": "Use FastAPI for backend",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "We need to choose a web framework",
            "decision": "We will use FastAPI",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        # Create first ADR
        response = self.client.post("/api/adrs", json=adr_data)
        assert response.status_code == 201
        
        # Try to create duplicate
        response = self.client.post("/api/adrs", json=adr_data)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]
    
    def test_get_adr(self):
        """Test getting a specific ADR."""
        # First create an ADR
        adr_data = {
            "id": "ADR-001",
            "title": "Use FastAPI for backend",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "We need to choose a web framework",
            "decision": "We will use FastAPI",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        self.client.post("/api/adrs", json=adr_data)
        
        # Now get it
        response = self.client.get("/api/adrs/ADR-001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "ADR-001"
        assert data["title"] == "Use FastAPI for backend"
    
    def test_get_adr_not_found(self):
        """Test getting a non-existent ADR."""
        response = self.client.get("/api/adrs/ADR-999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_list_adrs(self):
        """Test listing all ADRs."""
        # Create a couple of ADRs
        adr1_data = {
            "id": "ADR-001",
            "title": "Use FastAPI for backend",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "We need to choose a web framework",
            "decision": "We will use FastAPI",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        adr2_data = {
            "id": "ADR-002",
            "title": "Use Streamlit for frontend",
            "status": "accepted",
            "date": "2024-05-11",
            "authors": ["Jane Doe"],
            "context": "We need to choose a frontend framework",
            "decision": "We will use Streamlit",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        self.client.post("/api/adrs", json=adr1_data)
        self.client.post("/api/adrs", json=adr2_data)
        
        # List all ADRs
        response = self.client.get("/api/adrs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(adr["id"] == "ADR-001" for adr in data)
        assert any(adr["id"] == "ADR-002" for adr in data)
    
    def test_update_adr(self):
        """Test updating an ADR."""
        # Create an ADR
        adr_data = {
            "id": "ADR-001",
            "title": "Use FastAPI for backend",
            "status": "proposed",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "We need to choose a web framework",
            "decision": "We will use FastAPI",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        self.client.post("/api/adrs", json=adr_data)
        
        # Update it
        updated_data = adr_data.copy()
        updated_data["status"] = "accepted"
        updated_data["decision"] = "We have decided to use FastAPI"
        
        response = self.client.put("/api/adrs/ADR-001", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert data["decision"] == "We have decided to use FastAPI"
    
    def test_update_adr_not_found(self):
        """Test updating a non-existent ADR."""
        adr_data = {
            "id": "ADR-999",
            "title": "Non-existent ADR",
            "status": "proposed",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "Context",
            "decision": "Decision",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        response = self.client.put("/api/adrs/ADR-999", json=adr_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_delete_adr(self):
        """Test deleting an ADR."""
        # Create an ADR
        adr_data = {
            "id": "ADR-001",
            "title": "Use FastAPI for backend",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "We need to choose a web framework",
            "decision": "We will use FastAPI",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        self.client.post("/api/adrs", json=adr_data)
        
        # Delete it
        response = self.client.delete("/api/adrs/ADR-001")
        assert response.status_code == 204
        
        # Verify it's gone
        response = self.client.get("/api/adrs/ADR-001")
        assert response.status_code == 404
    
    def test_delete_adr_not_found(self):
        """Test deleting a non-existent ADR."""
        response = self.client.delete("/api/adrs/ADR-999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
