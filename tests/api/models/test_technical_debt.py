"""Tests for Technical Debt model."""
import pytest
from pydantic import ValidationError

from src.api.models.technical_debt import TechnicalDebt, Relationships


class TestTechnicalDebtModel:
    """Test suite for Technical Debt model."""
    
    def test_valid_technical_debt_creation(self):
        """Test creation of valid Technical Debt model."""
        td_data = {
            "id": "TD-001",
            "title": "Legacy authentication system",
            "description": "Need to migrate from custom auth to OAuth",
            "impact": "medium",
            "effort": "high",
            "status": "identified",
            "remediation": "Implement OAuth 2.0 with OpenID Connect",
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "components": []
            }
        }
        
        td = TechnicalDebt(**td_data)
        assert td.id == "TD-001"
        assert td.title == "Legacy authentication system"
        assert td.impact == "medium"
        assert td.effort == "high"
        assert td.status == "identified"
    
    def test_invalid_technical_debt_id(self):
        """Test Technical Debt creation with invalid ID."""
        td_data = {
            "id": "TD001",  # Invalid format
            "title": "Invalid Technical Debt",
            "description": "Test description",
            "impact": "medium",
            "effort": "high",
            "status": "identified",
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            TechnicalDebt(**td_data)
        
        assert "String should match pattern '^TD-[0-9]{3}$'" in str(exc_info.value)
    
    def test_invalid_impact(self):
        """Test Technical Debt creation with invalid impact."""
        td_data = {
            "id": "TD-001",
            "title": "Test Technical Debt",
            "description": "Test description",
            "impact": "invalid",  # Invalid impact
            "effort": "high",
            "status": "identified",
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            TechnicalDebt(**td_data)
        
        assert "Input should be" in str(exc_info.value)
        assert "'critical', 'high', 'medium' or 'low'" in str(exc_info.value)
    
    def test_invalid_effort(self):
        """Test Technical Debt creation with invalid effort."""
        td_data = {
            "id": "TD-001",
            "title": "Test Technical Debt",
            "description": "Test description",
            "impact": "high",
            "effort": "invalid",  # Invalid effort
            "status": "identified",
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            TechnicalDebt(**td_data)
        
        assert "Input should be" in str(exc_info.value)
        assert "'high', 'medium' or 'low'" in str(exc_info.value)
    
    def test_invalid_status(self):
        """Test Technical Debt creation with invalid status."""
        td_data = {
            "id": "TD-001",
            "title": "Test Technical Debt",
            "description": "Test description",
            "impact": "high",
            "effort": "medium",
            "status": "invalid",  # Invalid status
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            TechnicalDebt(**td_data)
        
        assert "Input should be" in str(exc_info.value)
        assert "'identified', 'planned', 'in_progress', 'resolved' or 'accepted'" in str(exc_info.value)
    
    def test_optional_remediation(self):
        """Test Technical Debt with optional remediation."""
        td_data = {
            "id": "TD-001",
            "title": "Test Technical Debt",
            "description": "Test description",
            "impact": "high",
            "effort": "medium",
            "status": "identified",
            # No remediation field
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "components": []
            }
        }
        
        td = TechnicalDebt(**td_data)
        assert td.remediation is None
