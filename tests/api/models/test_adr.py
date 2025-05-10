"""Tests for ADR model."""
import pytest
from datetime import date
from pydantic import ValidationError

from src.api.models.adr import ADR, Relationships, QualityRelationship


class TestADRModel:
    """Test suite for ADR model."""
    
    def test_valid_adr_creation(self):
        """Test creation of valid ADR model."""
        adr_data = {
            "id": "ADR-001",
            "title": "Use FastAPI for backend",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "We need to choose a web framework",
            "decision": "We will use FastAPI",
            "alternatives": {
                "FastAPI": {
                    "pros": ["Fast", "Type-safe"],
                    "cons": ["Smaller community"],
                    "score": {"performance": 9, "ease_of_use": 8}
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
        
        adr = ADR(**adr_data)
        assert adr.id == "ADR-001"
        assert adr.title == "Use FastAPI for backend"
        assert adr.status == "accepted"
        assert adr.date == date(2024, 5, 10)
        assert adr.authors == ["John Doe"]
        
    def test_invalid_adr_id(self):
        """Test ADR creation with invalid ID."""
        adr_data = {
            "id": "ADR001",  # Invalid format - missing hyphen
            "title": "Invalid ADR",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "Test context",
            "decision": "Test decision",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ADR(**adr_data)
        
        assert "String should match pattern '^ADR-[0-9]{3}$'" in str(exc_info.value)
    
    def test_invalid_status(self):
        """Test ADR creation with invalid status."""
        adr_data = {
            "id": "ADR-001",
            "title": "Invalid status ADR",
            "status": "invalid_status",  # Invalid status
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "Test context",
            "decision": "Test decision",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ADR(**adr_data)
            
        assert "Input should be" in str(exc_info.value)
        assert "'proposed', 'accepted', 'rejected', 'deprecated' or 'superseded'" in str(exc_info.value)
    
    def test_relationships(self):
        """Test ADR relationships."""
        adr_data = {
            "id": "ADR-001",
            "title": "Test ADR with relationships",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "Test context",
            "decision": "Test decision",
            "relationships": {
                "qualities": [
                    {
                        "id": "QR-001",
                        "type": "implements",
                        "strength": "strong"
                    }
                ],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        adr = ADR(**adr_data)
        assert len(adr.relationships.qualities) == 1
        assert adr.relationships.qualities[0].id == "QR-001"
        assert adr.relationships.qualities[0].type == "implements"
        assert adr.relationships.qualities[0].strength == "strong"
    
    def test_title_length_validation(self):
        """Test title length validation."""
        # Title too short
        adr_data = {
            "id": "ADR-001",
            "title": "Hi",  # Too short - minimum is 5
            "status": "accepted",
            "date": "2024-05-10",
            "authors": ["John Doe"],
            "context": "Test context",
            "decision": "Test decision",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ADR(**adr_data)
        
        assert "String should have at least 5 characters" in str(exc_info.value)
        
        # Title too long
        adr_data["title"] = "X" * 101  # Too long - maximum is 100
        
        with pytest.raises(ValidationError) as exc_info:
            ADR(**adr_data)
        
        assert "String should have at most 100 characters" in str(exc_info.value)
    
    def test_empty_authors_list(self):
        """Test ADR with empty authors list."""
        adr_data = {
            "id": "ADR-001",
            "title": "Test ADR",
            "status": "accepted",
            "date": "2024-05-10",
            "authors": [],  # Empty authors list
            "context": "Test context",
            "decision": "Test decision",
            "relationships": {
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ADR(**adr_data)
        
        assert "List should have at least 1 item" in str(exc_info.value)
