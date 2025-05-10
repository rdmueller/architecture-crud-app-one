"""Pydantic models for Components."""
from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict


class ADRRelationship(BaseModel):
    """Relationship to an ADR."""
    id: str
    type: Literal["implements", "affected_by", "structured_by"]


class QualityRelationship(BaseModel):
    """Relationship to a quality requirement."""
    id: str
    type: Literal["satisfies", "constrains"]


class RiskRelationship(BaseModel):
    """Relationship to a risk."""
    id: str
    type: Literal["hosts", "shares", "mitigates"]


class TechnicalDebtRelationship(BaseModel):
    """Relationship to technical debt."""
    id: str
    type: Literal["contains", "propagates"]


class ComponentRelationship(BaseModel):
    """Relationship to another component."""
    id: str
    type: Literal["depends_on", "provides_to", "interacts_with"]


class Relationships(BaseModel):
    """Collection of all relationships for a component."""
    adrs: List[ADRRelationship] = Field(default_factory=list)
    qualities: List[QualityRelationship] = Field(default_factory=list)
    risks: List[RiskRelationship] = Field(default_factory=list)
    technicalDebts: List[TechnicalDebtRelationship] = Field(default_factory=list)
    relatedComponents: List[ComponentRelationship] = Field(default_factory=list)


class Interface(BaseModel):
    """Component interface definition."""
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=1)
    type: str = Field(min_length=1)


class Component(BaseModel):
    """Component model."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
                "relationships": {}
            }
        }
    )
    
    id: str = Field(pattern="^C-[0-9]{3}$")
    title: str = Field(min_length=5, max_length=100)
    responsibility: str = Field(min_length=1)
    interfaces: List[Interface] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    relationships: Relationships = Field(default_factory=Relationships)
