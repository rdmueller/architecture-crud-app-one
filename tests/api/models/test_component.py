"""Tests for Component model."""
import pytest
from pydantic import ValidationError

from src.api.models.component import Component, Interface


class TestComponentModel:
    """Test suite for Component model."""
    
    def test_valid_component_creation(self):
        """Test creation of valid Component model."""
        component_data = {
            "id": "C-001",
            "title": "Authentication Service",
            "responsibility": "Handles user authentication and authorization",
            "interfaces": [
                {
                    "name": "authenticate",
                    "description": "Authenticate user credentials",
                    "type": "REST API"
                }
            ],
            "attributes": {
                "technology": "Node.js",
                "deployment": "Container"
            },
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "relatedComponents": []
            }
        }
        
        component = Component(**component_data)
        assert component.id == "C-001"
        assert component.title == "Authentication Service"
        assert len(component.interfaces) == 1
        assert component.interfaces[0].name == "authenticate"
        assert component.attributes["technology"] == "Node.js"
    
    def test_invalid_component_id(self):
        """Test Component creation with invalid ID."""
        component_data = {
            "id": "C001",  # Invalid format
            "title": "Invalid Component",
            "responsibility": "Test responsibility",
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "relatedComponents": []
            }
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Component(**component_data)
        
        assert "String should match pattern '^C-[0-9]{3}$'" in str(exc_info.value)
    
    def test_optional_interfaces(self):
        """Test Component with optional interfaces."""
        component_data = {
            "id": "C-001",
            "title": "Simple Component",
            "responsibility": "Test responsibility",
            # No interfaces field
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "relatedComponents": []
            }
        }
        
        component = Component(**component_data)
        assert component.interfaces == []
    
    def test_optional_attributes(self):
        """Test Component with optional attributes."""
        component_data = {
            "id": "C-001",
            "title": "Simple Component",
            "responsibility": "Test responsibility",
            # No attributes field
            "relationships": {
                "adrs": [],
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "relatedComponents": []
            }
        }
        
        component = Component(**component_data)
        assert component.attributes == {}
    
    def test_interface_validation(self):
        """Test Interface model validation."""
        interface_data = {
            "name": "AP",  # Too short
            "description": "Test interface",
            "type": "REST API"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Interface(**interface_data)
        
        assert "String should have at least 3 characters" in str(exc_info.value)
        
        # Valid interface
        interface_data["name"] = "API"
        interface = Interface(**interface_data)
        assert interface.name == "API"
