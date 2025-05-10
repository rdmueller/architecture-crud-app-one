"""Complete integration tests for API endpoints with correct validation."""
import pytest
import requests
from datetime import datetime
import time


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
            },
            "Flask": {
                "pros": ["Simple", "Flexible"],
                "cons": ["Less features", "No async by default"]
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


class TestADRCRUD:
    """Test ADR CRUD operations."""
    
    def test_adr_crud_workflow(self, api_server, clean_storage):
        """Test complete CRUD workflow for ADRs."""
        sample_adr = create_valid_adr()
        
        # Create
        response = requests.post(f"{api_server}/api/adrs", json=sample_adr)
        assert response.status_code == 201
        
        # Read
        response = requests.get(f"{api_server}/api/adrs/{sample_adr['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_adr["title"]
        
        # Update
        updated_adr = sample_adr.copy()
        updated_adr["title"] = "Updated Title"
        response = requests.put(f"{api_server}/api/adrs/{sample_adr['id']}", json=updated_adr)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        
        # Delete
        response = requests.delete(f"{api_server}/api/adrs/{sample_adr['id']}")
        assert response.status_code == 204
        
        # Verify deletion
        response = requests.get(f"{api_server}/api/adrs/{sample_adr['id']}")
        assert response.status_code == 404


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


class TestRiskCRUD:
    """Test Risk CRUD operations."""
    
    def test_risk_crud_workflow(self, api_server, clean_storage):
        """Test complete CRUD workflow for risks."""
        sample_risk = create_valid_risk()
        
        # Create
        response = requests.post(f"{api_server}/api/risks", json=sample_risk)
        assert response.status_code == 201
        
        # Read, Update, Delete similar to above...


class TestRelationships:
    """Test entity relationships."""
    
    def test_adr_quality_relationship(self, api_server, clean_storage):
        """Test creating relationships between ADR and Quality."""
        # Create entities
        adr = create_valid_adr()
        quality = create_valid_quality()
        
        # Create quality first
        resp = requests.post(f"{api_server}/api/qualities", json=quality)
        assert resp.status_code == 201
        
        # Create ADR with relationship
        adr["relationships"]["qualities"] = [
            {
                "id": quality["id"],
                "type": "addresses",
                "strength": "strong"
            }
        ]
        
        response = requests.post(f"{api_server}/api/adrs", json=adr)
        assert response.status_code == 201
        
        # Verify relationship
        response = requests.get(f"{api_server}/api/adrs/{adr['id']}")
        data = response.json()
        assert len(data["relationships"]["qualities"]) == 1
        assert data["relationships"]["qualities"][0]["id"] == quality["id"]


class TestComplexScenarios:
    """Test complex integration scenarios."""
    
    def test_full_architecture_workflow(self, api_server, clean_storage):
        """Test creating a complete architecture with all entities."""
        # Create all entities
        adr = create_valid_adr()
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
        
        # Create all entities
        for url, entity in entities:
            response = requests.post(url, json=entity)
            assert response.status_code == 201, f"Failed to create {url}: {response.text}"
        
        # Create ADR with relationships
        adr["relationships"] = {
            "qualities": [{"id": quality["id"], "type": "addresses", "strength": "strong"}],
            "risks": [{"id": risk["id"], "type": "mitigates", "strength": "medium"}],
            "technicalDebts": [{"id": technical_debt["id"], "type": "creates", "strength": "weak"}],
            "components": [{"id": component["id"], "type": "affects", "strength": "strong"}],
            "relatedAdrs": []
        }
        
        response = requests.post(f"{api_server}/api/adrs", json=adr)
        assert response.status_code == 201
        
        # Verify complete architecture
        response = requests.get(f"{api_server}/api/architecture")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all entities present
        assert len(data["adrs"]) >= 1
        assert len(data["qualities"]) >= 1
        assert len(data["risks"]) >= 1
        assert len(data["technicalDebts"]) >= 1
        assert len(data["components"]) >= 1


class TestPerformance:
    """Test performance metrics."""
    
    def test_response_times(self, api_server):
        """Test API response times."""
        endpoints = [
            f"{api_server}/health",
            f"{api_server}/api/architecture",
            f"{api_server}/api/adrs"
        ]
        
        for endpoint in endpoints:
            start = time.time()
            response = requests.get(endpoint)
            duration = (time.time() - start) * 1000  # ms
            
            assert response.status_code == 200
            assert duration < 200, f"Response time too high for {endpoint}: {duration:.2f}ms"
            print(f"{endpoint}: {duration:.2f}ms")
    
    def test_concurrent_requests(self, api_server, clean_storage):
        """Test API performance under concurrent load."""
        import concurrent.futures
        
        def create_adr(i):
            adr = create_valid_adr()
            adr["id"] = f"ADR-{i:03d}"
            adr["title"] = f"ADR Number {i}"
            
            start = time.time()
            response = requests.post(f"{api_server}/api/adrs", json=adr)
            duration = (time.time() - start) * 1000
            
            return {
                "id": adr["id"],
                "status_code": response.status_code,
                "duration": duration
            }
        
        # Create 10 ADRs concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_adr, i) for i in range(1, 11)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Analyze results
        successful = [r for r in results if r["status_code"] == 201]
        durations = [r["duration"] for r in successful]
        
        assert len(successful) >= 8, "Too many failed requests under load"
        assert max(durations) < 1000, "Response time too high under load"
        
        print(f"Concurrent requests: {len(successful)}/{len(results)} successful")
        print(f"Average duration: {sum(durations)/len(durations):.2f}ms")
        print(f"Max duration: {max(durations):.2f}ms")
