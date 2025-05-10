"""Tests for the JSON schema validator."""
import pytest
import json
from pathlib import Path

from src.data.validator import ArchitectureValidator


class TestArchitectureValidator:
    """Test suite for ArchitectureValidator."""
    
    def setup_method(self):
        """Set up test environment."""
        self.validator = ArchitectureValidator()
    
    def test_validate_valid_architecture(self):
        """Test validation of valid architecture data."""
        valid_data = {
            "metadata": {
                "title": "Test Architecture",
                "system": "test-system",
                "version": "1.0.0",
                "date": "2024-05-10",
                "authors": ["John Doe"]
            },
            "adrs": {
                "ADR-001": {
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
            },
            "qualities": {},
            "risks": {},
            "technicalDebts": {},
            "components": {}
        }
        
        # Should not raise any exception
        self.validator.validate(valid_data)
    
    def test_validate_invalid_adr_id(self):
        """Test validation fails for invalid ADR ID format."""
        invalid_data = {
            "metadata": {
                "title": "Test Architecture",
                "system": "test-system",
                "version": "1.0.0",
                "date": "2024-05-10"
            },
            "adrs": {
                "ADR001": {  # Invalid ID format (missing hyphen)
                    "id": "ADR001",
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
            },
            "qualities": {},
            "risks": {},
            "technicalDebts": {},
            "components": {}
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.validator.validate(invalid_data)
        
        assert "ADR ID" in str(exc_info.value)
    
    def test_validate_invalid_status(self):
        """Test validation fails for invalid status."""
        invalid_data = {
            "metadata": {
                "title": "Test Architecture",
                "system": "test-system",
                "version": "1.0.0",
                "date": "2024-05-10"
            },
            "adrs": {
                "ADR-001": {
                    "id": "ADR-001",
                    "title": "Use FastAPI for backend",
                    "status": "invalid_status",  # Invalid status
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
            },
            "qualities": {},
            "risks": {},
            "technicalDebts": {},
            "components": {}
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.validator.validate(invalid_data)
        
        assert "invalid" in str(exc_info.value).lower()
    
    def test_validate_missing_required_field(self):
        """Test validation fails for missing required field."""
        invalid_data = {
            "metadata": {
                "title": "Test Architecture",
                "system": "test-system",
                "version": "1.0.0",
                "date": "2024-05-10"
            },
            "adrs": {
                "ADR-001": {
                    "id": "ADR-001",
                    # Missing "title" field
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
            },
            "qualities": {},
            "risks": {},
            "technicalDebts": {},
            "components": {}
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.validator.validate(invalid_data)
        
        assert "missing" in str(exc_info.value).lower() or "required" in str(exc_info.value).lower()
    
    def test_validate_relationship_reference(self):
        """Test validation of relationship references."""
        data_with_invalid_ref = {
            "metadata": {
                "title": "Test Architecture",
                "system": "test-system",
                "version": "1.0.0",
                "date": "2024-05-10"
            },
            "adrs": {
                "ADR-001": {
                    "id": "ADR-001",
                    "title": "Use FastAPI for backend",
                    "status": "accepted",
                    "date": "2024-05-10",
                    "authors": ["John Doe"],
                    "context": "We need to choose a web framework",
                    "decision": "We will use FastAPI",
                    "relationships": {
                        "qualities": [
                            {
                                "id": "QR-999",  # Non-existent quality
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
            },
            "qualities": {},  # No QR-999 exists
            "risks": {},
            "technicalDebts": {},
            "components": {}
        }
        
        with pytest.raises(ValueError) as exc_info:
            self.validator.validate(data_with_invalid_ref)
        
        assert "QR-999" in str(exc_info.value) or "reference" in str(exc_info.value).lower()
