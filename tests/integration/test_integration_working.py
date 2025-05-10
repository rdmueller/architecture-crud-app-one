"""Working integration tests with correct relationship types."""
import pytest
import requests
from datetime import datetime
import time


class TestIntegration:
    """Complete integration test suite."""
    
    def test_health_check(self, api_server):
        """Test health check endpoint."""
        response = requests.get(f"{api_server}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_architecture_endpoint(self, api_server):
        """Test architecture retrieval."""
        response = requests.get(f"{api_server}/api/architecture")
        assert response.status_code == 200
        data = response.json()
        assert all(key in data for key in ["adrs", "qualities", "risks", "technicalDebts", "components"])
    
    def test_adr_crud(self, api_server, clean_storage):
        """Test ADR CRUD operations."""
        adr = {
            "id": "ADR-001",
            "title": "Use FastAPI",
            "status": "accepted",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "authors": ["Test Author"],
            "context": "Need to choose a framework",
            "decision": "Use FastAPI for performance",
            "alternatives": {},
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        # Create
        response = requests.post(f"{api_server}/api/adrs", json=adr)
        assert response.status_code == 201
        
        # Read
        response = requests.get(f"{api_server}/api/adrs/{adr['id']}")
        assert response.status_code == 200
        
        # Update
        adr["title"] = "Updated Title"
        response = requests.put(f"{api_server}/api/adrs/{adr['id']}", json=adr)
        assert response.status_code == 200
        
        # Delete
        response = requests.delete(f"{api_server}/api/adrs/{adr['id']}")
        assert response.status_code == 204
    
    def test_quality_crud(self, api_server, clean_storage):
        """Test Quality CRUD operations."""
        quality = {
            "id": "QR-001",
            "title": "Performance",
            "description": "System must be fast",
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
        
        # Create
        response = requests.post(f"{api_server}/api/qualities", json=quality)
        assert response.status_code == 201
        
        # Read
        response = requests.get(f"{api_server}/api/qualities/{quality['id']}")
        assert response.status_code == 200
        
        # Update
        quality["title"] = "Updated Performance"
        response = requests.put(f"{api_server}/api/qualities/{quality['id']}", json=quality)
        assert response.status_code == 200
        
        # Delete
        response = requests.delete(f"{api_server}/api/qualities/{quality['id']}")
        assert response.status_code == 204
    
    def test_risk_crud(self, api_server, clean_storage):
        """Test Risk CRUD operations."""
        risk = {
            "id": "RISK-001",
            "title": "Database Downtime",
            "description": "Database might be unavailable",
            "impact": "high",
            "probability": "low",
            "mitigation": "Use caching",
            "status": "identified",
            "category": "technical"
        }
        
        # Create
        response = requests.post(f"{api_server}/api/risks", json=risk)
        assert response.status_code == 201
        
        # Read
        response = requests.get(f"{api_server}/api/risks/{risk['id']}")
        assert response.status_code == 200
        
        # Update
        risk["title"] = "Updated Risk"
        response = requests.put(f"{api_server}/api/risks/{risk['id']}", json=risk)
        assert response.status_code == 200
        
        # Delete
        response = requests.delete(f"{api_server}/api/risks/{risk['id']}")
        assert response.status_code == 204
    
    def test_technical_debt_crud(self, api_server, clean_storage):
        """Test Technical Debt CRUD operations."""
        td = {
            "id": "TD-001",
            "title": "Missing Tests",
            "description": "No automated tests",
            "impact": "medium",
            "effort": "high",
            "resolution": "Add tests",
            "status": "planned",
            "priority": "medium"
        }
        
        # Create
        response = requests.post(f"{api_server}/api/technical-debts", json=td)
        assert response.status_code == 201
        
        # Read
        response = requests.get(f"{api_server}/api/technical-debts/{td['id']}")
        assert response.status_code == 200
        
        # Update
        td["title"] = "Updated Technical Debt"
        response = requests.put(f"{api_server}/api/technical-debts/{td['id']}", json=td)
        assert response.status_code == 200
        
        # Delete
        response = requests.delete(f"{api_server}/api/technical-debts/{td['id']}")
        assert response.status_code == 204
    
    def test_component_crud(self, api_server, clean_storage):
        """Test Component CRUD operations."""
        component = {
            "id": "C-001",
            "title": "API Service",
            "responsibility": "Handle API requests",
            "type": "service",
            "interfaces": [
                {
                    "name": "REST API",
                    "description": "RESTful endpoints",
                    "protocol": "HTTP",
                    "type": "synchronous"
                }
            ],
            "attributes": {
                "language": "Python",
                "framework": "FastAPI"
            }
        }
        
        # Create
        response = requests.post(f"{api_server}/api/components", json=component)
        assert response.status_code == 201
        
        # Read
        response = requests.get(f"{api_server}/api/components/{component['id']}")
        assert response.status_code == 200
        
        # Update
        component["title"] = "Updated Component"
        response = requests.put(f"{api_server}/api/components/{component['id']}", json=component)
        assert response.status_code == 200
        
        # Delete
        response = requests.delete(f"{api_server}/api/components/{component['id']}")
        assert response.status_code == 204
    
    def test_adr_quality_relationship(self, api_server, clean_storage):
        """Test ADR-Quality relationship with correct type."""
        # Create quality
        quality = {
            "id": "QR-001",
            "title": "Performance",
            "description": "System performance",
            "priority": "high",
            "qualityCategory": "performance",
            "metrics": []
        }
        response = requests.post(f"{api_server}/api/qualities", json=quality)
        assert response.status_code == 201
        
        # Create ADR with relationship using correct type
        adr = {
            "id": "ADR-001",
            "title": "Performance Decision",
            "status": "accepted",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "authors": ["Test Author"],
            "context": "Need performance",
            "decision": "Optimize for speed",
            "alternatives": {},
            "relationships": {
                "qualities": [
                    {
                        "id": quality["id"],
                        "type": "implements",  # Use valid type for quality relationship
                        "strength": "strong"
                    }
                ],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        response = requests.post(f"{api_server}/api/adrs", json=adr)
        assert response.status_code == 201
        
        # Verify relationship
        response = requests.get(f"{api_server}/api/adrs/{adr['id']}")
        data = response.json()
        assert len(data["relationships"]["qualities"]) == 1
        assert data["relationships"]["qualities"][0]["id"] == quality["id"]
        assert data["relationships"]["qualities"][0]["type"] == "implements"
    
    def test_full_architecture_workflow(self, api_server, clean_storage):
        """Test creating a complete architecture with correct relationship types."""
        # Create all entities
        quality = {
            "id": "QR-001",
            "title": "Performance",
            "description": "System performance",
            "priority": "high",
            "qualityCategory": "performance",
            "metrics": []
        }
        
        risk = {
            "id": "RISK-001",
            "title": "Database Risk",
            "description": "Database issues",
            "impact": "high",
            "probability": "low",
            "mitigation": "Use caching",
            "status": "identified",
            "category": "technical"
        }
        
        technical_debt = {
            "id": "TD-001",
            "title": "Testing Debt",
            "description": "Missing tests",
            "impact": "medium",
            "effort": "high",
            "resolution": "Add tests",
            "status": "planned",
            "priority": "medium"
        }
        
        component = {
            "id": "C-001",
            "title": "API Service",
            "responsibility": "Handle API",
            "type": "service",
            "interfaces": [
                {
                    "name": "REST API",
                    "description": "RESTful API",
                    "protocol": "HTTP",
                    "type": "synchronous"
                }
            ],
            "attributes": {"language": "Python"}
        }
        
        # Create all entities
        entities = [
            (f"{api_server}/api/qualities", quality),
            (f"{api_server}/api/risks", risk),
            (f"{api_server}/api/technical-debts", technical_debt),
            (f"{api_server}/api/components", component)
        ]
        
        for url, entity in entities:
            response = requests.post(url, json=entity)
            assert response.status_code == 201
        
        # Create ADR with all relationships using correct types
        adr = {
            "id": "ADR-001",
            "title": "Architecture Decision",
            "status": "accepted",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "authors": ["Test Author"],
            "context": "Architecture context",
            "decision": "Architecture decision",
            "alternatives": {},
            "relationships": {
                "qualities": [{"id": quality["id"], "type": "implements", "strength": "strong"}],
                "risks": [{"id": risk["id"], "type": "mitigates", "strength": "medium"}],
                "technicalDebts": [{"id": technical_debt["id"], "type": "creates", "strength": "weak"}],
                "components": [{"id": component["id"], "type": "affects", "strength": "strong"}],
                "relatedAdrs": []
            }
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
        
        # Verify relationships
        adr_data = data["adrs"][adr["id"]]
        assert len(adr_data["relationships"]["qualities"]) == 1
        assert len(adr_data["relationships"]["risks"]) == 1
        assert len(adr_data["relationships"]["technicalDebts"]) == 1
        assert len(adr_data["relationships"]["components"]) == 1
    
    def test_performance(self, api_server):
        """Test API performance."""
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
            max_time = max(times)
            print(f"{endpoint}: avg={avg_time:.2f}ms, max={max_time:.2f}ms")
            assert avg_time < 200, f"Average response time too high: {avg_time:.2f}ms"
