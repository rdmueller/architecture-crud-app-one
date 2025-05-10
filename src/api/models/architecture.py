"""Main Architecture model that combines all entities."""
from datetime import date
from typing import Dict, List
from pydantic import BaseModel, Field, ConfigDict

from .adr import ADR
from .quality import Quality
from .risk import Risk
from .technical_debt import TechnicalDebt
from .component import Component


class Metadata(BaseModel):
    """Architecture metadata."""
    title: str = Field(min_length=5, max_length=200)
    system: str = Field(min_length=1)
    version: str = Field(min_length=1)
    date: date
    authors: List[str] = Field(default_factory=list)


class Architecture(BaseModel):
    """Complete architecture model containing all entities."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "metadata": {
                    "title": "My System Architecture",
                    "system": "my-system",
                    "version": "1.0.0",
                    "date": "2024-05-10",
                    "authors": ["John Doe"]
                },
                "adrs": {},
                "qualities": {},
                "risks": {},
                "technicalDebts": {},
                "components": {}
            }
        }
    )
    
    metadata: Metadata
    adrs: Dict[str, ADR] = Field(default_factory=dict)
    qualities: Dict[str, Quality] = Field(default_factory=dict)
    risks: Dict[str, Risk] = Field(default_factory=dict)
    technicalDebts: Dict[str, TechnicalDebt] = Field(default_factory=dict)
    components: Dict[str, Component] = Field(default_factory=dict)
