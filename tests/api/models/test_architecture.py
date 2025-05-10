"""Tests for the main Architecture model."""
import pytest
from datetime import date

from src.api.models.architecture import Architecture


class TestArchitectureModel:
    """Test suite for Architecture model."""
    
    def test_valid_architecture_creation(self):
        """Test creation of valid Architecture model."""
        arch_data = {
            "metadata": {
                "title": "Architecture CRUD Application",
                "system": "architecture-crud-app",
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
        
        architecture = Architecture(**arch_data)
        assert architecture.metadata.title == "Architecture CRUD Application"
        assert len(architecture.adrs) == 1
        assert "ADR-001" in architecture.adrs
        assert architecture.adrs["ADR-001"].title == "Use FastAPI for backend"
    
    def test_empty_architecture(self):
        """Test creation of architecture with minimal data."""
        arch_data = {
            "metadata": {
                "title": "Minimal Architecture",
                "system": "test-system",
                "version": "1.0.0",
                "date": "2024-05-10"
            }
        }
        
        architecture = Architecture(**arch_data)
        assert architecture.metadata.title == "Minimal Architecture"
        assert architecture.adrs == {}
        assert architecture.qualities == {}
        assert architecture.risks == {}
        assert architecture.technicalDebts == {}
        assert architecture.components == {}
    
    def test_metadata_validation(self):
        """Test metadata field validation."""
        arch_data = {
            "metadata": {
                "title": "Test",  # Too short
                "system": "test-system",
                "version": "1.0.0",
                "date": "2024-05-10"
            }
        }
        
        with pytest.raises(Exception) as exc_info:
            Architecture(**arch_data)
        
        assert "at least 5 characters" in str(exc_info.value).lower()
