"""JSON schema validator for architecture data."""
import json
import re
from typing import Dict, Any, Set
from pathlib import Path

from ..api.models.architecture import Architecture


class ArchitectureValidator:
    """Validator for architecture data using JSON schema and custom rules."""
    
    def __init__(self):
        """Initialize validator."""
        self._load_schema()
    
    def _load_schema(self):
        """Load JSON schema from file."""
        schema_path = Path(__file__).parent.parent / "json" / "architecture-schema.json"
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
        else:
            self.schema = None
    
    def validate(self, data: Dict[str, Any]) -> None:
        """
        Validate architecture data.
        
        Args:
            data: Architecture data to validate
            
        Raises:
            ValueError: If validation fails
        """
        # First, validate IDs before Pydantic parsing (which is stricter)
        self._validate_ids(data)
        
        # Then, try to parse with Pydantic for basic validation
        try:
            architecture = Architecture(**data)
        except Exception as e:
            raise ValueError(f"Invalid architecture data: {str(e)}")
        
        # Additional custom validations
        self._validate_relationships(data)
    
    def _validate_ids(self, data: Dict[str, Any]) -> None:
        """Validate ID formats for all entities."""
        # ADR IDs
        if "adrs" in data:
            for adr_id, adr in data["adrs"].items():
                if not re.match(r"^ADR-[0-9]{3}$", adr_id):
                    raise ValueError(f"Invalid ADR ID format: {adr_id}")
                if adr.get("id") != adr_id:
                    raise ValueError(f"Mismatched ADR ID: {adr_id} != {adr.get('id')}")
        
        # Quality IDs
        if "qualities" in data:
            for quality_id, quality in data["qualities"].items():
                if not re.match(r"^QR-[0-9]{3}$", quality_id):
                    raise ValueError(f"Invalid Quality ID format: {quality_id}")
                if quality.get("id") != quality_id:
                    raise ValueError(f"Mismatched Quality ID: {quality_id} != {quality.get('id')}")
        
        # Risk IDs
        if "risks" in data:
            for risk_id, risk in data["risks"].items():
                if not re.match(r"^RISK-[0-9]{3}$", risk_id):
                    raise ValueError(f"Invalid Risk ID format: {risk_id}")
                if risk.get("id") != risk_id:
                    raise ValueError(f"Mismatched Risk ID: {risk_id} != {risk.get('id')}")
        
        # Technical Debt IDs
        if "technicalDebts" in data:
            for td_id, td in data["technicalDebts"].items():
                if not re.match(r"^TD-[0-9]{3}$", td_id):
                    raise ValueError(f"Invalid Technical Debt ID format: {td_id}")
                if td.get("id") != td_id:
                    raise ValueError(f"Mismatched Technical Debt ID: {td_id} != {td.get('id')}")
        
        # Component IDs
        if "components" in data:
            for component_id, component in data["components"].items():
                if not re.match(r"^C-[0-9]{3}$", component_id):
                    raise ValueError(f"Invalid Component ID format: {component_id}")
                if component.get("id") != component_id:
                    raise ValueError(f"Mismatched Component ID: {component_id} != {component.get('id')}")
    
    def _validate_relationships(self, data: Dict[str, Any]) -> None:
        """Validate that all relationship references exist."""
        # Collect all existing IDs
        existing_ids = {
            "adrs": set(data.get("adrs", {}).keys()),
            "qualities": set(data.get("qualities", {}).keys()),
            "risks": set(data.get("risks", {}).keys()),
            "technicalDebts": set(data.get("technicalDebts", {}).keys()),
            "components": set(data.get("components", {}).keys())
        }
        
        # Check ADR relationships
        for adr_id, adr in data.get("adrs", {}).items():
            relationships = adr.get("relationships", {})
            
            # Check quality relationships
            for rel in relationships.get("qualities", []):
                if rel["id"] not in existing_ids["qualities"]:
                    raise ValueError(f"ADR {adr_id} references non-existent quality: {rel['id']}")
            
            # Check risk relationships
            for rel in relationships.get("risks", []):
                if rel["id"] not in existing_ids["risks"]:
                    raise ValueError(f"ADR {adr_id} references non-existent risk: {rel['id']}")
            
            # Check technical debt relationships
            for rel in relationships.get("technicalDebts", []):
                if rel["id"] not in existing_ids["technicalDebts"]:
                    raise ValueError(f"ADR {adr_id} references non-existent technical debt: {rel['id']}")
            
            # Check component relationships
            for rel in relationships.get("components", []):
                if rel["id"] not in existing_ids["components"]:
                    raise ValueError(f"ADR {adr_id} references non-existent component: {rel['id']}")
            
            # Check ADR relationships
            for rel in relationships.get("relatedAdrs", []):
                if rel["id"] not in existing_ids["adrs"]:
                    raise ValueError(f"ADR {adr_id} references non-existent ADR: {rel['id']}")
        
        # Similar checks for other entity types
        self._validate_quality_relationships(data, existing_ids)
        self._validate_risk_relationships(data, existing_ids)
        self._validate_technical_debt_relationships(data, existing_ids)
        self._validate_component_relationships(data, existing_ids)
    
    def _validate_quality_relationships(self, data: Dict[str, Any], existing_ids: Dict[str, Set[str]]) -> None:
        """Validate quality relationships."""
        for quality_id, quality in data.get("qualities", {}).items():
            relationships = quality.get("relationships", {})
            
            for rel in relationships.get("adrs", []):
                if rel["id"] not in existing_ids["adrs"]:
                    raise ValueError(f"Quality {quality_id} references non-existent ADR: {rel['id']}")
            
            for rel in relationships.get("risks", []):
                if rel["id"] not in existing_ids["risks"]:
                    raise ValueError(f"Quality {quality_id} references non-existent risk: {rel['id']}")
                    
            for rel in relationships.get("technicalDebts", []):
                if rel["id"] not in existing_ids["technicalDebts"]:
                    raise ValueError(f"Quality {quality_id} references non-existent technical debt: {rel['id']}")
                    
            for rel in relationships.get("components", []):
                if rel["id"] not in existing_ids["components"]:
                    raise ValueError(f"Quality {quality_id} references non-existent component: {rel['id']}")
    
    def _validate_risk_relationships(self, data: Dict[str, Any], existing_ids: Dict[str, Set[str]]) -> None:
        """Validate risk relationships."""
        for risk_id, risk in data.get("risks", {}).items():
            relationships = risk.get("relationships", {})
            
            for rel in relationships.get("adrs", []):
                if rel["id"] not in existing_ids["adrs"]:
                    raise ValueError(f"Risk {risk_id} references non-existent ADR: {rel['id']}")
            
            for rel in relationships.get("qualities", []):
                if rel["id"] not in existing_ids["qualities"]:
                    raise ValueError(f"Risk {risk_id} references non-existent quality: {rel['id']}")
                    
            for rel in relationships.get("technicalDebts", []):
                if rel["id"] not in existing_ids["technicalDebts"]:
                    raise ValueError(f"Risk {risk_id} references non-existent technical debt: {rel['id']}")
                    
            for rel in relationships.get("components", []):
                if rel["id"] not in existing_ids["components"]:
                    raise ValueError(f"Risk {risk_id} references non-existent component: {rel['id']}")
    
    def _validate_technical_debt_relationships(self, data: Dict[str, Any], existing_ids: Dict[str, Set[str]]) -> None:
        """Validate technical debt relationships."""
        for td_id, td in data.get("technicalDebts", {}).items():
            relationships = td.get("relationships", {})
            
            for rel in relationships.get("adrs", []):
                if rel["id"] not in existing_ids["adrs"]:
                    raise ValueError(f"Technical debt {td_id} references non-existent ADR: {rel['id']}")
            
            for rel in relationships.get("qualities", []):
                if rel["id"] not in existing_ids["qualities"]:
                    raise ValueError(f"Technical debt {td_id} references non-existent quality: {rel['id']}")
                    
            for rel in relationships.get("risks", []):
                if rel["id"] not in existing_ids["risks"]:
                    raise ValueError(f"Technical debt {td_id} references non-existent risk: {rel['id']}")
                    
            for rel in relationships.get("components", []):
                if rel["id"] not in existing_ids["components"]:
                    raise ValueError(f"Technical debt {td_id} references non-existent component: {rel['id']}")
    
    def _validate_component_relationships(self, data: Dict[str, Any], existing_ids: Dict[str, Set[str]]) -> None:
        """Validate component relationships."""
        for component_id, component in data.get("components", {}).items():
            relationships = component.get("relationships", {})
            
            for rel in relationships.get("adrs", []):
                if rel["id"] not in existing_ids["adrs"]:
                    raise ValueError(f"Component {component_id} references non-existent ADR: {rel['id']}")
            
            for rel in relationships.get("qualities", []):
                if rel["id"] not in existing_ids["qualities"]:
                    raise ValueError(f"Component {component_id} references non-existent quality: {rel['id']}")
                    
            for rel in relationships.get("risks", []):
                if rel["id"] not in existing_ids["risks"]:
                    raise ValueError(f"Component {component_id} references non-existent risk: {rel['id']}")
                    
            for rel in relationships.get("technicalDebts", []):
                if rel["id"] not in existing_ids["technicalDebts"]:
                    raise ValueError(f"Component {component_id} references non-existent technical debt: {rel['id']}")
                    
            for rel in relationships.get("relatedComponents", []):
                if rel["id"] not in existing_ids["components"]:
                    raise ValueError(f"Component {component_id} references non-existent component: {rel['id']}")
