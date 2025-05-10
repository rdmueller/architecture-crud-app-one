"""AsciiDoc generator for architecture documentation."""
from typing import Dict, Any, List
from datetime import datetime
import jinja2
import os


class AsciiDocGenerator:
    """Generator for converting architecture data to AsciiDoc format."""
    
    def __init__(self, template_dir: str = None):
        """Initialize the generator with template directory."""
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), "templates")
        
        self.template_dir = template_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate(self, data: Dict[str, Any]) -> str:
        """Generate complete AsciiDoc document from architecture data."""
        template = self.env.get_template("architecture.adoc.j2")
        
        # Prepare context
        context = {
            "data": data,
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "adrs": data.get("adrs", {}),
            "qualities": data.get("qualities", {}),
            "risks": data.get("risks", {}),
            "technical_debts": data.get("technicalDebts", {}),
            "components": data.get("components", {})
        }
        
        return template.render(context)
    
    def generate_adrs(self, adrs: Dict[str, Any]) -> str:
        """Generate ADRs chapter."""
        template = self.env.get_template("adrs.adoc.j2")
        return template.render(adrs=adrs)
    
    def generate_qualities(self, qualities: Dict[str, Any]) -> str:
        """Generate quality requirements chapter."""
        template = self.env.get_template("qualities.adoc.j2")
        return template.render(qualities=qualities)
    
    def generate_risks(self, risks: Dict[str, Any]) -> str:
        """Generate risks chapter."""
        template = self.env.get_template("risks.adoc.j2")
        return template.render(risks=risks)
    
    def generate_technical_debts(self, technical_debts: Dict[str, Any]) -> str:
        """Generate technical debts chapter."""
        template = self.env.get_template("technical_debts.adoc.j2")
        return template.render(technical_debts=technical_debts)
    
    def generate_components(self, components: Dict[str, Any]) -> str:
        """Generate components chapter."""
        template = self.env.get_template("components.adoc.j2")
        return template.render(components=components)
    
    def generate_relationships_matrix(self, data: Dict[str, Any]) -> str:
        """Generate relationships matrix."""
        # Create matrix data structure
        entities = []
        relationships = {}
        
        # Collect all entities
        for entity_type, entities_dict in data.items():
            for entity_id, entity_data in entities_dict.items():
                entities.append({
                    "id": entity_id,
                    "type": entity_type,
                    "title": entity_data.get("title", entity_id)
                })
        
        # Build relationships matrix
        for source in entities:
            relationships[source["id"]] = {}
            for target in entities:
                relationships[source["id"]][target["id"]] = []
        
        # Fill relationships
        for entity_type, entities_dict in data.items():
            for entity_id, entity_data in entities_dict.items():
                if "relationships" in entity_data:
                    for rel_type, rel_list in entity_data["relationships"].items():
                        for rel in rel_list:
                            target_id = rel.get("targetId")
                            if target_id and target_id in relationships.get(entity_id, {}):
                                relationships[entity_id][target_id].append({
                                    "type": rel.get("type", rel_type),
                                    "strength": rel.get("strength", "medium")
                                })
        
        template = self.env.get_template("relationships.adoc.j2")
        return template.render(entities=entities, relationships=relationships)
