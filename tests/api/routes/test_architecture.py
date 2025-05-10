"""Tests for the architecture endpoint."""
import pytest
from fastapi.testclient import TestClient
from datetime import date
from pathlib import Path
import sys

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from api.main import app
from data.repository import ArchitectureRepository
from api.models.architecture import Architecture
from tests.api.conftest import mock_repo, mock_validator

client = TestClient(app)


def test_get_architecture_success(mock_repo):
    """Test successful retrieval of complete architecture."""
    # Mock data
    test_data = {
        "adrs": {
            "ADR-001": {
                "id": "ADR-001",
                "title": "Test ADR",
                "status": "accepted",
                "date": "2025-05-10",
                "authors": ["John Doe"],
                "context": "Test context",
                "decision": "Test decision",
                "alternatives": {},
                "relationships": {
                    "qualities": [],
                    "risks": [],
                    "technicalDebts": [],
                    "components": [],
                    "relatedAdrs": []
                }
            }
        },
        "qualities": {},
        "risks": {},
        "technicalDebts": {},
        "components": {}
    }
    
    mock_repo.load.return_value = test_data
    
    # Make request
    response = client.get("/api/architecture")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "adrs" in data
    assert "ADR-001" in data["adrs"]
    assert data["adrs"]["ADR-001"]["title"] == "Test ADR"


def test_get_architecture_empty_data(mock_repo):
    """Test retrieval when no data exists."""
    # Mock empty data
    mock_repo.load.return_value = {
        "adrs": {},
        "qualities": {},
        "risks": {},
        "technicalDebts": {},
        "components": {}
    }
    
    # Make request
    response = client.get("/api/architecture")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["adrs"] == {}
    assert data["qualities"] == {}
    assert data["risks"] == {}
    assert data["technicalDebts"] == {}
    assert data["components"] == {}


def test_get_architecture_with_all_entities(mock_repo):
    """Test retrieval with all entity types."""
    # Mock complete data
    test_data = {
        "adrs": {
            "ADR-001": {
                "id": "ADR-001",
                "title": "Test ADR",
                "status": "accepted",
                "date": "2025-05-10",
                "authors": ["John Doe"],
                "context": "Test context",
                "decision": "Test decision",
                "alternatives": {},
                "relationships": {
                    "qualities": [],
                    "risks": [],
                    "technicalDebts": [],
                    "components": [],
                    "relatedAdrs": []
                }
            }
        },
        "qualities": {
            "Q-001": {
                "id": "Q-001",
                "title": "Performance",
                "description": "System must be fast",
                "metrics": [],
                "priority": "must"
            }
        },
        "risks": {
            "RISK-001": {
                "id": "RISK-001",
                "title": "Data Loss",
                "description": "Risk of data loss",
                "impact": "high",
                "likelihood": "low",
                "mitigationStrategy": "Backup strategy",
                "status": "mitigated",
                "owner": "Team Lead"
            }
        },
        "technicalDebts": {
            "TD-001": {
                "id": "TD-001",
                "title": "Legacy Code",
                "description": "Old code needs refactoring",
                "impact": "medium",
                "effort": "high",
                "repaymentPlan": "Refactor in Q2",
                "status": "acknowledged"
            }
        },
        "components": {
            "COMP-001": {
                "id": "COMP-001",
                "title": "API Gateway",
                "responsibility": "Route requests",
                "interfaces": [],
                "attributes": []
            }
        }
    }
    
    mock_repo.load.return_value = test_data
    
    # Make request
    response = client.get("/api/architecture")
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert len(data["adrs"]) == 1
    assert len(data["qualities"]) == 1
    assert len(data["risks"]) == 1
    assert len(data["technicalDebts"]) == 1
    assert len(data["components"]) == 1
