"""Simple fixtures for integration tests using existing running servers."""
import pytest
import requests
from datetime import datetime


# Use the existing running servers
API_SERVER_URL = "http://localhost:8082"
UI_SERVER_URL = "http://localhost:8501"


@pytest.fixture(scope="session")
def api_server():
    """Use existing running API server."""
    # Check if API server is running
    try:
        response = requests.get(f"{API_SERVER_URL}/health")
        if response.status_code == 200:
            yield API_SERVER_URL
        else:
            pytest.skip("API server not running on port 8082")
    except requests.ConnectionError:
        pytest.skip("API server not running on port 8082")


@pytest.fixture(scope="session")
def ui_server():
    """Use existing running UI server."""
    # Check if UI server is running
    try:
        response = requests.get(UI_SERVER_URL)
        if response.status_code == 200:
            yield UI_SERVER_URL
        else:
            pytest.skip("UI server not running on port 8501")
    except requests.ConnectionError:
        pytest.skip("UI server not running on port 8501")


@pytest.fixture
def clean_storage(api_server):
    """Clean storage before each test."""
    # Clear all data
    for entity_type in ["adrs", "qualities", "risks", "technical-debts", "components"]:
        response = requests.get(f"{api_server}/api/{entity_type}")
        if response.status_code == 200:
            entities = response.json()
            for entity in entities:
                entity_id = entity.get("id")
                if entity_id:
                    requests.delete(f"{api_server}/api/{entity_type}/{entity_id}")
    
    yield
    
    # Clean up after test
    for entity_type in ["adrs", "qualities", "risks", "technical-debts", "components"]:
        response = requests.get(f"{api_server}/api/{entity_type}")
        if response.status_code == 200:
            entities = response.json()
            for entity in entities:
                entity_id = entity.get("id")
                if entity_id:
                    requests.delete(f"{api_server}/api/{entity_type}/{entity_id}")


@pytest.fixture
def sample_adr():
    """Create a sample ADR for testing."""
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


@pytest.fixture
def sample_quality():
    """Create a sample quality for testing."""
    return {
        "id": "Q-001",
        "title": "Performance",
        "description": "The system must respond quickly to user requests.",
        "priority": "high",
        "metrics": [
            {
                "name": "Response Time",
                "target": "< 200ms",
                "current": "150ms"
            }
        ]
    }


@pytest.fixture
def sample_risk():
    """Create a sample risk for testing."""
    return {
        "id": "R-001",
        "title": "Database Downtime",
        "description": "The database might become unavailable.",
        "impact": "high",
        "probability": "low",
        "mitigation": "Implement caching and retry logic.",
        "status": "identified"
    }


@pytest.fixture
def sample_technical_debt():
    """Create a sample technical debt for testing."""
    return {
        "id": "TD-001",
        "title": "No Automated Testing",
        "description": "The system lacks automated tests.",
        "impact": "medium",
        "effort": "high",
        "resolution": "Implement comprehensive test suite.",
        "status": "planned"
    }


@pytest.fixture
def sample_component():
    """Create a sample component for testing."""
    return {
        "id": "C-001",
        "title": "API Service",
        "responsibility": "Handle all API requests and business logic.",
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
