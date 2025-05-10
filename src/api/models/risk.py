"""Pydantic models for Risks."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class ADRRelationship(BaseModel):
    """Relationship to an ADR."""
    id: str
    type: Literal["mitigated_by", "causes", "accepts"]


class QualityRelationship(BaseModel):
    """Relationship to a quality requirement."""
    id: str
    type: Literal["threatens", "mitigated_by"]


class TechnicalDebtRelationship(BaseModel):
    """Relationship to technical debt."""
    id: str
    type: Literal["results_from", "causes"]


class ComponentRelationship(BaseModel):
    """Relationship to a component."""
    id: str
    type: Literal["affects", "originates_from"]


class Relationships(BaseModel):
    """Collection of all relationships for a risk."""
    adrs: List[ADRRelationship] = Field(default_factory=list)
    qualities: List[QualityRelationship] = Field(default_factory=list)
    technicalDebts: List[TechnicalDebtRelationship] = Field(default_factory=list)
    components: List[ComponentRelationship] = Field(default_factory=list)


class Risk(BaseModel):
    """Risk model."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "RISK-001",
                "title": "Database downtime risk",
                "description": "Risk of database unavailability",
                "impact": "high",
                "probability": "medium",
                "status": "identified",
                "mitigation": "Implement database clustering",
                "relationships": {}
            }
        }
    )
    
    id: str = Field(pattern="^RISK-[0-9]{3}$")
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=1)
    impact: Literal["critical", "high", "medium", "low"]
    probability: Literal["high", "medium", "low"]
    status: Literal["identified", "mitigated", "accepted", "closed"]
    mitigation: Optional[str] = None
    relationships: Relationships = Field(default_factory=Relationships)
