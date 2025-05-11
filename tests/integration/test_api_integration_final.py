"""Integration tests for API endpoints - final version with correct data formats."""
import pytest
import requests
from datetime import datetime


class TestAPIIntegration:
    """Test API endpoints with real server."""
    
    def test_health_check(self, api_server):
        """Test health check endpoint."""
        response = requests.get(f"{api_server}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_root_endpoint(self, api_server):
        """Test root endpoint."""
        response = requests.get(f"{api_server}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]
    
    def test_architecture_endpoint(self, api_server):
        """Test architecture retrieval."""
        response = requests.get(f"{api_server}/api/architecture")
        assert response.status_code == 200
        data = response.json()
        assert "adrs" in data
        assert "qualities" in data
        assert "risks" in data
        assert "technicalDebts" in data
        assert "components" in data


class TestADRCRUD:
    """Test ADR CRUD operations."""
    
    def test_create_adr(self, api_server, sample_adr, clean_storage):
        """Test creating an ADR."""
        response = requests.post(f"{api_server}/api/adrs", json=sample_adr)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == sample_adr["id"]
        assert data["title"] == sample_adr["title"]
    
    def test_get_adr(self, api_server, sample_adr, clean_storage):
        """Test getting an ADR."""
        # Create ADR first
        requests.post(f"{api_server}/api/adrs", json=sample_adr)
        
        # Get ADR
        response = requests.get(f"{api_server}/api/adrs/{sample_adr['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_adr["id"]
        assert data["title"] == sample_adr["title"]
    
    def test_update_adr(self, api_server, sample_adr, clean_storage):
        """Test updating an ADR."""
        # Create ADR first
        requests.post(f"{api_server}/api/adrs", json=sample_adr)
        
        # Update ADR
        updated_adr = sample_adr.copy()
        updated_adr["title"] = "Updated Title"
        response = requests.put(f"{api_server}/api/adrs/{sample_adr['id']}", json=updated_adr)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
    
    def test_delete_adr(self, api_server, sample_adr, clean_storage):
        """Test deleting an ADR."""
        # Create ADR first
        requests.post(f"{api_server}/api/adrs", json=sample_adr)
        
        # Delete ADR
        response = requests.delete(f"{api_server}/api/adrs/{sample_adr['id']}")
        assert response.status_code == 204
        
        # Verify deletion
        response = requests.get(f"{api_server}/api/adrs/{sample_adr['id']}")
        assert response.status_code == 404
    
    def test_list_adrs(self, api_server, sample_adr, clean_storage):
        """Test listing ADRs."""
        # Create multiple ADRs
        adrs = []
        for i in range(3):
            adr = sample_adr.copy()
            adr["id"] = f"ADR-00{i+1}"
            adr["title"] = f"ADR {i+1}"
            requests.post(f"{api_server}/api/adrs", json=adr)
            adrs.append(adr)
        
        # List ADRs
        response = requests.get(f"{api_server}/api/adrs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        
        # Verify all created ADRs are in the list
        ids = [adr["id"] for adr in data]
        for adr in adrs:
            assert adr["id"] in ids


def create_valid_quality():
    """Create a valid quality object with correct format."""
    return {
        "id": "QR-001",  # Fixed: Use QR- prefix
        "title": "Performance",
        "description": "The system must respond quickly to user requests.",
        "priority": "high",
        "qualityCategory": "performance",
        "metrics": [
            {
                "name": "Response Time",
                "measure": "milliseconds",  # Added missing field
                "target": "< 200ms",
                "current": "150ms"
            }
        ]
    }


class TestQualityCRUD:
    """Test Quality CRUD operations."""
    
    def test_quality_crud_workflow(self, api_server, clean_storage):
        """Test complete CRUD workflow for qualities."""
        sample_quality = create_valid_quality()
        
        # Create
        response = requests.post(f"{api_server}/api/qualities", json=sample_quality)
        assert response.status_code == 201
        
        # Read
        response = requests.get(f"{api_server}/api/qualities/{sample_quality['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == sample_quality["title"]
        
        # Update
        updated_quality = sample_quality.copy()
        updated_quality["title"] = "Updated Performance"
        response = requests.put(f"{api_server}/api/qualities/{sample_quality['id']}", json=updated_quality)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Performance"
        
        # Delete
        response = requests.delete(f"{api_server}/api/qualities/{sample_quality['id']}")
        assert response.status_code == 204
        
        # Verify deletion
        response = requests.get(f"{api_server}/api/qualities/{sample_quality['id']}")
        assert response.status_code == 404


class TestRelationships:
    """Test entity relationships."""
    
    def test_adr_quality_relationship(self, api_server, sample_adr, clean_storage):
        """Test creating relationships between ADR and Quality."""
        # Create quality first
        sample_quality = create_valid_quality()
        resp = requests.post(f"{api_server}/api/qualities", json=sample_quality)
        assert resp.status_code == 201
        
        # Create ADR with relationship to quality
        adr_with_relationship = sample_adr.copy()
        adr_with_relationship["relationships"]["qualities"] = [
            {
                "id": sample_quality["id"],
                "type": "addresses",
                "strength": "strong"
            }
        ]
        
        response = requests.post(f"{api_server}/api/adrs", json=adr_with_relationship)
        assert response.status_code == 201
        
        # Verify relationship
        response = requests.get(f"{api_server}/api/adrs/{sample_adr['id']}")
        data = response.json()
        assert len(data["relationships"]["qualities"]) == 1
        assert data["relationships"]["qualities"][0]["id"] == sample_quality["id"]


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_adr_data(self, api_server, clean_storage):
        """Test creating ADR with invalid data."""
        invalid_adr = {
            "id": "INVALID-ID",  # Invalid format
            "title": "Test",
            "status": "invalid_status"  # Invalid status
        }
        
        response = requests.post(f"{api_server}/api/adrs", json=invalid_adr)
        assert response.status_code == 422
    
    def test_nonexistent_resource(self, api_server):
        """Test getting non-existent resource."""
        response = requests.get(f"{api_server}/api/adrs/ADR-999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
    
    def test_duplicate_id(self, api_server, sample_adr, clean_storage):
        """Test creating duplicate IDs."""
        # Create first ADR
        response = requests.post(f"{api_server}/api/adrs", json=sample_adr)
        assert response.status_code == 201
        
        # Try to create duplicate
        response = requests.post(f"{api_server}/api/adrs", json=sample_adr)
        assert response.status_code == 409


def create_valid_risk():
    """Create a valid risk object."""
    return {
        "id": "R-001",
        "title": "Database Downtime",
        "description": "The database might become unavailable.",
        "impact": "high",
        "probability": "low",
        "mitigation": "Implement caching and retry logic.",
        "status": "identified",
        "category": "technical"
    }


def create_valid_technical_debt():
    """Create a valid technical debt object."""
    return {
        "id": "TD-001",
        "title": "No Automated Testing",
        "description": "The system lacks automated tests.",
        "impact": "medium",
        "effort": "high",
        "resolution": "Implement comprehensive test suite.",
        "status": "planned",
        "priority": "medium"
    }


def create_valid_component():
    """Create a valid component object."""
    return {
        "id": "C-001",
        "title": "API Service",
        "responsibility": "Handle all API requests and business logic.",
        "type": "service",
        "interfaces": [
            {
                "name": "REST API",
                "description": "RESTful API endpoints",
                "protocol": "HTTP"
            }
        ],
        "attributes": {
            "language": "Python",
            "framework": "FastAPI"
        }
    }


class TestComplexScenarios:
    """Test complex integration scenarios."""
    
    def test_full_architecture_workflow(self, api_server, sample_adr, clean_storage):
        """Test creating a complete architecture with all entities."""
        # Create all entities with valid data
        quality = create_valid_quality()
        risk = create_valid_risk()
        technical_debt = create_valid_technical_debt()
        component = create_valid_component()
        
        entities = [
            (f"{api_server}/api/qualities", quality),
            (f"{api_server}/api/risks", risk),
            (f"{api_server}/api/technical-debts", technical_debt),
            (f"{api_server}/api/components", component)
        ]
        
        for url, entity in entities:
            response = requests.post(url, json=entity)
            assert response.status_code == 201, f"Failed to create {url}: {response.text}"
        
        # Create ADR with relationships to all entities
        adr_with_relationships = sample_adr.copy()
        adr_with_relationships["relationships"] = {
            "qualities": [{"id": quality["id"], "type": "addresses", "strength": "strong"}],
            "risks": [{"id": risk["id"], "type": "mitigates", "strength": "medium"}],
            "technicalDebts": [{"id": technical_debt["id"], "type": "creates", "strength": "weak"}],
            "components": [{"id": component["id"], "type": "affects", "strength": "strong"}],
            "relatedAdrs": []
        }
        
        response = requests.post(f"{api_server}/api/adrs", json=adr_with_relationships)
        assert response.status_code == 201
        
        # Get complete architecture
        response = requests.get(f"{api_server}/api/architecture")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all entities are present
        assert len(data["adrs"]) >= 1
        assert len(data["qualities"]) >= 1
        assert len(data["risks"]) >= 1
        assert len(data["technicalDebts"]) >= 1
        assert len(data["components"]) >= 1
        
        # Verify relationships
        adr = data["adrs"][sample_adr["id"]]
        assert len(adr["relationships"]["qualities"]) == 1
        assert len(adr["relationships"]["risks"]) == 1
        assert len(adr["relationships"]["technicalDebts"]) == 1
        assert len(adr["relationships"]["components"]) == 1


class TestPerformanceMetrics:
    """Test API performance metrics."""
    
    def test_api_response_time(self, api_server):
        """Test API response times."""
        import time
        
        endpoints = [
            f"{api_server}/health",
            f"{api_server}/api/architecture",
            f"{api_server}/api/adrs"
        ]
        
        for endpoint in endpoints:
            start = time.time()
            response = requests.get(endpoint)
            end = time.time()
            
            duration = (end - start) * 1000  # milliseconds
            assert response.status_code == 200
            assert duration < 200, f"Response time too high for {endpoint}: {duration}ms"
            print(f"{endpoint}: {duration:.2f}ms")
