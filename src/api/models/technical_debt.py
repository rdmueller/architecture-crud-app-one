"""Pydantic models for Technical Debts."""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class ADRRelationship(BaseModel):
    """Relationship to an ADR."""
    id: str
    type: Literal["introduced_by", "addressed_by"]


class QualityRelationship(BaseModel):
    """Relationship to a quality requirement."""
    id: str
    type: Literal["violates", "degrades"]


class RiskRelationship(BaseModel):
    """Relationship to a risk."""
    id: str
    type: Literal["causes", "compound"]


class ComponentRelationship(BaseModel):
    """Relationship to a component."""
    id: str
    type: Literal["affects", "located_in"]


class Relationships(BaseModel):
    """Collection of all relationships for technical debt."""
    adrs: List[ADRRelationship] = Field(default_factory=list)
    qualities: List[QualityRelationship] = Field(default_factory=list)
    risks: List[RiskRelationship] = Field(default_factory=list)
    components: List[ComponentRelationship] = Field(default_factory=list)


class TechnicalDebt(BaseModel):
    """Technical Debt model."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "TD-001",
                "title": "Legacy authentication system",
                "description": "Need to migrate from custom auth to OAuth",
                "impact": "medium",
                "effort": "high",
                "status": "identified",
                "remediation": "Implement OAuth 2.0 with OpenID Connect",
                "relationships": {}
            }
        }
    )
    
    id: str = Field(pattern="^TD-[0-9]{3}$")
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=1)
    impact: Literal["critical", "high", "medium", "low"]
    effort: Literal["high", "medium", "low"]
    status: Literal["identified", "planned", "in_progress", "resolved", "accepted"]
    remediation: Optional[str] = None
    relationships: Relationships = Field(default_factory=Relationships)
