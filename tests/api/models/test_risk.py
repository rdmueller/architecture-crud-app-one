"""Tests for Risk model."""
import pytest
from pydantic import ValidationError

from src.api.models.risk import Risk, Relationships


class TestRiskModel:
    """Test suite for Risk model."""
    
    def test_valid_risk_creation(self):
        """Test creation of valid Risk model."""
        risk_data = {
            "id": "RISK-001",
            "title": "Database downtime risk",
            "description": "Risk of database unavailability",
            "impact": "high",
            "probability": "medium",
            "status": "identified",
            "mitigation": "Implement database clustering",
            "relationships": {
                "adrs": [],
                "qualities": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        risk = Risk(**risk_data)
        assert risk.id == "RISK-001"
        assert risk.title == "Database downtime risk"
        assert risk.impact == "high"
        assert risk.probability == "medium"
        assert risk.status == "identified"
    
    def test_invalid_risk_id(self):
        """Test Risk creation with invalid ID."""
        risk_data = {
            "id": "RISK001",  # Invalid format
            "title": "Invalid Risk",
            "description": "Test description",
            "impact": "high",
            "probability": "medium",
            "status": "identified",
            "relationships": {
                "adrs": [],
                "qualities": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Risk(**risk_data)
        
        assert "String should match pattern '^RISK-[0-9]{3}$'" in str(exc_info.value)
    
    def test_invalid_impact(self):
        """Test Risk creation with invalid impact."""
        risk_data = {
            "id": "RISK-001",
            "title": "Test Risk",
            "description": "Test description",
            "impact": "invalid",  # Invalid impact
            "probability": "medium",
            "status": "identified",
            "relationships": {
                "adrs": [],
                "qualities": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Risk(**risk_data)
        
        assert "Input should be" in str(exc_info.value)
        assert "'critical', 'high', 'medium' or 'low'" in str(exc_info.value)
    
    def test_invalid_status(self):
        """Test Risk creation with invalid status."""
        risk_data = {
            "id": "RISK-001",
            "title": "Test Risk",
            "description": "Test description",
            "impact": "high",
            "probability": "medium",
            "status": "invalid",  # Invalid status
            "relationships": {
                "adrs": [],
                "qualities": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Risk(**risk_data)
        
        assert "Input should be" in str(exc_info.value)
        assert "'identified', 'mitigated', 'accepted' or 'closed'" in str(exc_info.value)
    
    def test_optional_mitigation(self):
        """Test Risk with optional mitigation."""
        risk_data = {
            "id": "RISK-001",
            "title": "Test Risk",
            "description": "Test description",
            "impact": "high",
            "probability": "medium",
            "status": "identified",
            # No mitigation field
            "relationships": {
                "adrs": [],
                "qualities": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        risk = Risk(**risk_data)
        assert risk.mitigation is None
