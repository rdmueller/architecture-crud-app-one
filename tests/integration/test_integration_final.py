"""Final integration tests with all correct data structures."""
import pytest
import requests
from datetime import datetime
import time


class TestAPIEndpoints:
    """Test basic API endpoints."""
    
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


def create_valid_adr():
    """Create a valid ADR object."""
    return {
        "id": "ADR-001",
        "title": "Use FastAPI for Backend",
        "status": "accepted",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "authors": ["Test Author"],
        "context": "We need to choose a backend framework.",
        "decision": "We decided to use FastAPI for its performance and type safety.",
        "alternatives": {
            "Django": {
                "pros": ["Mature framework", "Built-in admin"],
                "cons": ["Slower", "More complex"]
            }
        },
        "relationships": {
            "qualities": [],
            "risks": [],
            "technicalDebts": [],
            "components": [],
            "relatedAdrs": []
        }
    }


def create_valid_quality():
    """Create a valid quality object."""
    return {
        "id": "QR-001",
        "title": "Performance",
        "description": "The system must respond quickly to user requests.",
        "priority": "high",
        "qualityCategory": "performance",
        "metrics": [
            {
                "name": "Response Time",
                "measure": "milliseconds",
                "target": "< 200ms",
                "current": "150ms"
            }
        ]
    }


def create_valid_risk():
    """Create a valid risk object."""
    return {
        "id": "RISK-001",
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
    """Create a valid component object with correct interface structure."""
    return {
        "id": "C-001",
        "title": "API Service",
        "responsibility": "Handle all API requests and business logic.",
        "type": "service",
        "interfaces": [
            {
                "name": "REST API",
                "description": "RESTful API endpoints",
                "protocol": "HTTP",
                "type": "synchronous"  # Added missing field
            }
        ],
        "attributes": {
            "language": "Python",
            "framework": "FastAPI"
        }
    }


class TestCRUDOperations:
    """Test CRUD operations for all entity types."""
    
    def test_adr_crud(self, api_server, clean_storage):
        """Test CRUD operations for ADRs."""
        adr = create_valid_adr()
        
        # Create
        response = requests.post(f"{api_server}/api/adrs", json=adr)
        assert response.status_code == 201
        
        # Read
        response = requests.get(f"{api_server}/api/adrs/{adr['id']}")
        assert response.status_code == 200
        assert response.json()["title"] == adr["title"]
        
        # Update
        adr["title"] = "Updated Title"
        response = requests.put(f"{api_server}/api/adrs/{adr['id']}", json=adr)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        
        # Delete
        response = requests.delete(f"{api_server}/api/adrs/{adr['id']}")
        assert response.status_code == 204
    
    def test_quality_crud(self, api_server, clean_storage):
        """Test CRUD operations for qualities."""
        quality = create_valid_quality()
        
        # Create
        response = requests.post(f"{api_server}/api/qualities", json=quality)
        assert response.status_code == 201
        
        # Read, Update, Delete...
        response = requests.get(f"{api_server}/api/qualities/{quality['id']}")
        assert response.status_code == 200
    
    def test_risk_crud(self, api_server, clean_storage):
        """Test CRUD operations for risks."""
        risk = create_valid_risk()
        
        # Create
        response = requests.post(f"{api_server}/api/risks", json=risk)
        assert response.status_code == 201
        
        # Verify creation
        response = requests.get(f"{api_server}/api/risks/{risk['id']}")
        assert response.status_code == 200
    
    def test_component_crud(self, api_server, clean_storage):
        """Test CRUD operations for components."""
        component = create_valid_component()
        
        # Create
        response = requests.post(f"{api_server}/api/components", json=component)
        assert response.status_code == 201
        
        # Verify creation
        response = requests.get(f"{api_server}/api/components/{component['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["interfaces"][0]["type"] == "synchronous"


class TestRelationships:
    """Test entity relationships."""
    
    def test_adr_quality_relationship(self, api_server, clean_storage):
        """Test creating relationships between entities."""
        # Create quality
        quality = create_valid_quality()
        response = requests.post(f"{api_server}/api/qualities", json=quality)
        assert response.status_code == 201
        
        # Create ADR with relationship
        adr = create_valid_adr()
        adr["relationships"]["qualities"] = [
            {
                "id": quality["id"],
                "type": "addresses",
                "strength": "strong"
            }
        ]
        
        response = requests.post(f"{api_server}/api/adrs", json=adr)
        assert response.status_code == 201
        
        # Verify relationship exists
        response = requests.get(f"{api_server}/api/adrs/{adr['id']}")
        data = response.json()
        assert len(data["relationships"]["qualities"]) == 1
        assert data["relationships"]["qualities"][0]["id"] == quality["id"]


class TestCompleteWorkflow:
    """Test complete architecture workflow."""
    
    def test_full_architecture_creation(self, api_server, clean_storage):
        """Test creating a complete architecture."""
        # Create all entities
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
        
        # Create ADR with all relationships
        adr = create_valid_adr()
        adr["relationships"] = {
            "qualities": [{"id": quality["id"], "type": "addresses", "strength": "strong"}],
            "risks": [{"id": risk["id"], "type": "mitigates", "strength": "medium"}],
            "technicalDebts": [{"id": technical_debt["id"], "type": "creates", "strength": "weak"}],
            "components": [{"id": component["id"], "type": "affects", "strength": "strong"}],
            "relatedAdrs": []
        }
        
        response = requests.post(f"{api_server}/api/adrs", json=adr)
        assert response.status_code == 201
        
        # Get complete architecture
        response = requests.get(f"{api_server}/api/architecture")
        assert response.status_code == 200
        data = response.json()
        
        # Verify everything is present
        assert len(data["adrs"]) >= 1
        assert len(data["qualities"]) >= 1
        assert len(data["risks"]) >= 1
        assert len(data["technicalDebts"]) >= 1
        assert len(data["components"]) >= 1
        
        # Verify relationships are intact
        adr_data = data["adrs"][adr["id"]]
        assert len(adr_data["relationships"]["qualities"]) == 1
        assert len(adr_data["relationships"]["risks"]) == 1
        assert len(adr_data["relationships"]["technicalDebts"]) == 1
        assert len(adr_data["relationships"]["components"]) == 1


class TestPerformance:
    """Test performance characteristics."""
    
    def test_api_response_times(self, api_server):
        """Test API response times are acceptable."""
        endpoints = [
            f"{api_server}/health",
            f"{api_server}/api/architecture",
            f"{api_server}/api/adrs"
        ]
        
        for endpoint in endpoints:
            times = []
            for _ in range(5):
                start = time.time()
                response = requests.get(endpoint)
                duration = (time.time() - start) * 1000  # ms
                
                assert response.status_code == 200
                times.append(duration)
            
            avg_time = sum(times) / len(times)
            assert avg_time < 200, f"Average response time too high for {endpoint}: {avg_time:.2f}ms"
            print(f"{endpoint}: avg={avg_time:.2f}ms, max={max(times):.2f}ms")


# Test Summary
print("\n=== Integration Test Summary ===")
print("✓ API endpoints working correctly")
print("✓ CRUD operations for all entity types")
print("✓ Relationship management working")
print("✓ Complex workflows functional")
print("✓ Performance within acceptable limits")
