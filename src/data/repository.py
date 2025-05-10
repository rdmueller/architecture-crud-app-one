"""Repository layer for handling data persistence."""
import json
import os
from datetime import date
from typing import Optional, Dict, Any
from pathlib import Path

from ..api.models.architecture import Architecture, Metadata
from ..api.models.adr import ADR
from ..api.models.quality import Quality
from ..api.models.risk import Risk
from ..api.models.technical_debt import TechnicalDebt
from ..api.models.component import Component


class ArchitectureRepository:
    """Repository for managing architecture data persistence."""
    
    def __init__(self, file_path: str):
        """Initialize repository with file path."""
        self.file_path = file_path
    
    def _default_architecture(self) -> Architecture:
        """Create default empty architecture."""
        return Architecture(
            metadata=Metadata(
                title="Architecture",
                system="system",
                version="1.0.0",
                date=date.today()
            )
        )
    
    def _serialize_date(self, obj: Any) -> Any:
        """Custom JSON serializer for date objects."""
        if isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def load(self) -> Architecture:
        """Load architecture from file."""
        if not os.path.exists(self.file_path):
            return self._default_architecture()
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    return self._default_architecture()
                
                data = json.loads(content)
                return Architecture(**data)
        except (json.JSONDecodeError, ValueError):
            return self._default_architecture()
    
    def save(self, architecture: Architecture) -> None:
        """Save architecture to file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.file_path) or '.', exist_ok=True)
        
        # Convert to dict and save
        data = architecture.model_dump(mode='json')
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=self._serialize_date)
    
    def add_adr(self, adr: ADR) -> None:
        """Add a new ADR to the architecture."""
        architecture = self.load()
        architecture.adrs[adr.id] = adr
        self.save(architecture)
    
    def update_adr(self, adr_id: str, adr: ADR) -> None:
        """Update an existing ADR."""
        architecture = self.load()
        if adr_id in architecture.adrs:
            architecture.adrs[adr_id] = adr
            self.save(architecture)
    
    def delete_adr(self, adr_id: str) -> None:
        """Delete an ADR from the architecture."""
        architecture = self.load()
        if adr_id in architecture.adrs:
            del architecture.adrs[adr_id]
            self.save(architecture)
    
    def get_adr(self, adr_id: str) -> Optional[ADR]:
        """Get a specific ADR by ID."""
        architecture = self.load()
        return architecture.adrs.get(adr_id)
    
    # Similar methods for other entities (qualities, risks, etc.)
    
    def add_quality(self, quality: Quality) -> None:
        """Add a new quality requirement to the architecture."""
        architecture = self.load()
        architecture.qualities[quality.id] = quality
        self.save(architecture)
    
    def update_quality(self, quality_id: str, quality: Quality) -> None:
        """Update an existing quality requirement."""
        architecture = self.load()
        if quality_id in architecture.qualities:
            architecture.qualities[quality_id] = quality
            self.save(architecture)
    
    def delete_quality(self, quality_id: str) -> None:
        """Delete a quality requirement from the architecture."""
        architecture = self.load()
        if quality_id in architecture.qualities:
            del architecture.qualities[quality_id]
            self.save(architecture)
    
    def get_quality(self, quality_id: str) -> Optional[Quality]:
        """Get a specific quality requirement by ID."""
        architecture = self.load()
        return architecture.qualities.get(quality_id)
    
    def add_risk(self, risk: Risk) -> None:
        """Add a new risk to the architecture."""
        architecture = self.load()
        architecture.risks[risk.id] = risk
        self.save(architecture)
    
    def update_risk(self, risk_id: str, risk: Risk) -> None:
        """Update an existing risk."""
        architecture = self.load()
        if risk_id in architecture.risks:
            architecture.risks[risk_id] = risk
            self.save(architecture)
    
    def delete_risk(self, risk_id: str) -> None:
        """Delete a risk from the architecture."""
        architecture = self.load()
        if risk_id in architecture.risks:
            del architecture.risks[risk_id]
            self.save(architecture)
    
    def get_risk(self, risk_id: str) -> Optional[Risk]:
        """Get a specific risk by ID."""
        architecture = self.load()
        return architecture.risks.get(risk_id)
    
    def add_technical_debt(self, td: TechnicalDebt) -> None:
        """Add a new technical debt to the architecture."""
        architecture = self.load()
        architecture.technicalDebts[td.id] = td
        self.save(architecture)
    
    def update_technical_debt(self, td_id: str, td: TechnicalDebt) -> None:
        """Update an existing technical debt."""
        architecture = self.load()
        if td_id in architecture.technicalDebts:
            architecture.technicalDebts[td_id] = td
            self.save(architecture)
    
    def delete_technical_debt(self, td_id: str) -> None:
        """Delete a technical debt from the architecture."""
        architecture = self.load()
        if td_id in architecture.technicalDebts:
            del architecture.technicalDebts[td_id]
            self.save(architecture)
    
    def get_technical_debt(self, td_id: str) -> Optional[TechnicalDebt]:
        """Get a specific technical debt by ID."""
        architecture = self.load()
        return architecture.technicalDebts.get(td_id)
    
    def add_component(self, component: Component) -> None:
        """Add a new component to the architecture."""
        architecture = self.load()
        architecture.components[component.id] = component
        self.save(architecture)
    
    def update_component(self, component_id: str, component: Component) -> None:
        """Update an existing component."""
        architecture = self.load()
        if component_id in architecture.components:
            architecture.components[component_id] = component
            self.save(architecture)
    
    def delete_component(self, component_id: str) -> None:
        """Delete a component from the architecture."""
        architecture = self.load()
        if component_id in architecture.components:
            del architecture.components[component_id]
            self.save(architecture)
    
    def get_component(self, component_id: str) -> Optional[Component]:
        """Get a specific component by ID."""
        architecture = self.load()
        return architecture.components.get(component_id)
