"""Tests for Quality Requirement model."""
import pytest
from pydantic import ValidationError

from src.api.models.quality import Quality, Metric, Relationships


class TestQualityModel:
    """Test suite for Quality Requirement model."""
    
    def test_valid_quality_creation(self):
        """Test creation of valid Quality model."""
        quality_data = {
            "id": "QR-001",
            "title": "Performance Requirements",
            "description": "System should respond within 200ms",
            "metrics": [
                {
                    "name": "Response Time",
                    "target": "< 200ms",
                    "measure": "Average response time"
                }
            ],
            "priority": "high",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        quality = Quality(**quality_data)
        assert quality.id == "QR-001"
        assert quality.title == "Performance Requirements"
        assert quality.priority == "high"
        assert len(quality.metrics) == 1
        assert quality.metrics[0].name == "Response Time"
    
    def test_invalid_quality_id(self):
        """Test Quality creation with invalid ID."""
        quality_data = {
            "id": "QR001",  # Invalid format
            "title": "Invalid Quality",
            "description": "Test description",
            "priority": "high",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Quality(**quality_data)
        
        assert "String should match pattern '^QR-[0-9]{3}$'" in str(exc_info.value)
    
    def test_invalid_priority(self):
        """Test Quality creation with invalid priority."""
        quality_data = {
            "id": "QR-001",
            "title": "Test Quality",
            "description": "Test description",
            "priority": "invalid",  # Invalid priority
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Quality(**quality_data)
        
        assert "Input should be" in str(exc_info.value)
        assert "'high', 'medium' or 'low'" in str(exc_info.value)
    
    def test_empty_metrics(self):
        """Test Quality with empty metrics list."""
        quality_data = {
            "id": "QR-001",
            "title": "Test Quality",
            "description": "Test description",
            "metrics": [],
            "priority": "high",
            "relationships": {
                "adrs": [],
                "risks": [],
                "technicalDebts": [],
                "components": []
            }
        }
        
        quality = Quality(**quality_data)
        assert quality.metrics == []
    
    def test_metric_validation(self):
        """Test Metric model validation."""
        metric_data = {
            "name": "M",  # Too short
            "target": "100%",
            "measure": "Percentage of successful requests"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Metric(**metric_data)
        
        assert "String should have at least 3 characters" in str(exc_info.value)
        
        # Valid metric
        metric_data["name"] = "Success Rate"
        metric = Metric(**metric_data)
        assert metric.name == "Success Rate"
