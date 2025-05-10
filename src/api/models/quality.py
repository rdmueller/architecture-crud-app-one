"""Pydantic models for Quality Requirements."""
from typing import List, Literal
from pydantic import BaseModel, Field, ConfigDict


class ADRRelationship(BaseModel):
    """Relationship to an ADR."""
    id: str
    type: Literal["addresses", "affects", "violates"]


class RiskRelationship(BaseModel):
    """Relationship to a risk."""
    id: str
    type: Literal["addresses", "causes"]


class TechnicalDebtRelationship(BaseModel):
    """Relationship to technical debt."""
    id: str
    type: Literal["causes", "resolved_by"]


class ComponentRelationship(BaseModel):
    """Relationship to a component."""
    id: str
    type: Literal["applies_to", "satisfied_by"]


class Relationships(BaseModel):
    """Collection of all relationships for a quality requirement."""
    adrs: List[ADRRelationship] = Field(default_factory=list)
    risks: List[RiskRelationship] = Field(default_factory=list)
    technicalDebts: List[TechnicalDebtRelationship] = Field(default_factory=list)
    components: List[ComponentRelationship] = Field(default_factory=list)


class Metric(BaseModel):
    """Metric for measuring quality requirement."""
    name: str = Field(min_length=3, max_length=100)
    target: str = Field(min_length=1)
    measure: str = Field(min_length=1)


class Quality(BaseModel):
    """Quality Requirement model."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
                "relationships": {}
            }
        }
    )
    
    id: str = Field(pattern="^QR-[0-9]{3}$")
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=1)
    metrics: List[Metric] = Field(default_factory=list)
    priority: Literal["high", "medium", "low"]
    relationships: Relationships = Field(default_factory=Relationships)
