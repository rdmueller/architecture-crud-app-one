"""Pydantic models for Architecture Decision Records."""
from datetime import date
from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer


class QualityRelationship(BaseModel):
    """Relationship to a quality requirement."""
    id: str
    type: Literal["implements", "affects", "requires"]
    strength: Literal["strong", "medium", "weak"]


class RiskRelationship(BaseModel):
    """Relationship to a risk."""
    id: str
    type: Literal["results_from", "mitigates", "accepts"]


class TechnicalDebtRelationship(BaseModel):
    """Relationship to technical debt."""
    id: str  
    type: Literal["introduces", "addresses"]


class ComponentRelationship(BaseModel):
    """Relationship to a component."""
    id: str
    type: Literal["affects", "implements", "uses"]


class ADRRelationship(BaseModel):
    """Relationship to another ADR."""
    id: str
    type: Literal["supersedes", "deprecates", "amends", "depends_on", "relates_to"]


class Relationships(BaseModel):
    model_config = ConfigDict(extra='allow')
    """Collection of all relationships for an entity."""
    qualities: List[QualityRelationship] = Field(default_factory=list)
    risks: List[RiskRelationship] = Field(default_factory=list)
    technicalDebts: List[TechnicalDebtRelationship] = Field(default_factory=list)
    components: List[ComponentRelationship] = Field(default_factory=list)
    relatedAdrs: List[ADRRelationship] = Field(default_factory=list)


class AlternativeScore(BaseModel):
    """Score for an alternative."""
    performance: Optional[int] = Field(None, ge=1, le=10)
    ease_of_use: Optional[int] = Field(None, ge=1, le=10)
    maintainability: Optional[int] = Field(None, ge=1, le=10)
    cost: Optional[int] = Field(None, ge=1, le=10)
    scalability: Optional[int] = Field(None, ge=1, le=10)
    security: Optional[int] = Field(None, ge=1, le=10)


class Alternative(BaseModel):
    """Alternative considered for a decision."""
    pros: List[str]
    cons: List[str]
    score: Optional[AlternativeScore] = None


class ADR(BaseModel):
    """Architecture Decision Record model."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "ADR-001",
                "title": "Use FastAPI for backend",
                "status": "accepted",
                "date": "2024-05-10",
                "authors": ["John Doe"],
                "context": "We need to choose a web framework",
                "decision": "We will use FastAPI",
                "alternatives": {},
                "relationships": {},
            }
        }
    )
    
    id: str = Field(pattern="^ADR-[0-9]{3}$")
    title: str = Field(min_length=5, max_length=100)
    status: Literal["proposed", "accepted", "rejected", "deprecated", "superseded"]
    date: date
    authors: List[str] = Field(min_length=1)
    context: str = Field(min_length=1)
    decision: str = Field(min_length=1)
    alternatives: Dict[str, Alternative] = Field(default_factory=dict)
    relationships: Relationships = Field(default_factory=Relationships)
    
    @field_serializer('date')
    def serialize_date(self, date: date, _info):
        return date.isoformat()
