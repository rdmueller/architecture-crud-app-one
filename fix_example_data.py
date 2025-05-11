#!/usr/bin/env python
"""Fix example data to match the expected schema."""
import json
import os
import shutil
from datetime import datetime

def transform_alternatives(alternatives):
    """Transform alternatives from advantages/disadvantages to pros/cons."""
    result = {}
    for key, value in alternatives.items():
        result[key] = {
            "pros": value.get("advantages", []),
            "cons": value.get("disadvantages", [])
        }
    return result

def transform_relationships(relationships):
    """Transform relationships from string lists to object lists."""
    result = {}
    for rel_type, rel_list in relationships.items():
        if rel_type == "qualities":
            result[rel_type] = [{"id": qid, "type": "addresses", "strength": "medium"} for qid in rel_list]
        elif rel_type == "risks":
            result[rel_type] = [{"id": rid, "type": "mitigates", "impact": "medium"} for rid in rel_list]
        elif rel_type == "technicalDebts":
            result[rel_type] = [{"id": tid, "type": "causes", "impact": "medium"} for tid in rel_list]
        elif rel_type == "components":
            result[rel_type] = [{"id": cid, "type": "implements", "responsibility": "primary"} for cid in rel_list]
        elif rel_type == "relatedAdrs":
            result[rel_type] = [{"id": aid, "type": "extends", "description": ""} for aid in rel_list]
        else:
            result[rel_type] = rel_list
    return result

def transform_metrics(metrics):
    """Transform metrics from metricName/targetValue to name/target/measure."""
    return [
        {
            "name": m.get("metricName", ""),
            "target": m.get("targetValue", ""),
            "measure": m.get("unit", "")
        }
        for m in metrics
    ]

def fix_example_data():
    """Fix example data to match the expected schema."""
    data_dir = "data"
    example_file = os.path.join(data_dir, "example_architecture.json")
    fixed_file = os.path.join(data_dir, "fixed_architecture.json")
    
    # Backup original file
    backup_file = os.path.join(data_dir, f"example_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    shutil.copy2(example_file, backup_file)
    print(f"Backed up original example data to {backup_file}")
    
    # Load example data
    with open(example_file, 'r') as f:
        data = json.load(f)
    
    # Transform ADRs
    for adr_id, adr in data.get("adrs", {}).items():
        # Fix alternatives
        if "alternatives" in adr:
            adr["alternatives"] = transform_alternatives(adr["alternatives"])
        
        # Fix relationships
        if "relationships" in adr:
            adr["relationships"] = transform_relationships(adr["relationships"])
    
    # Transform Qualities
    new_qualities = {}
    for q_id, quality in data.get("qualities", {}).items():
        # Fix ID pattern
        new_id = q_id.replace("QA-", "QR-")
        
        # Fix metrics
        if "metrics" in quality:
            quality["metrics"] = transform_metrics(quality["metrics"])
        
        # Fix priority
        if quality.get("priority") == "must":
            quality["priority"] = "high"
        elif quality.get("priority") == "should":
            quality["priority"] = "medium"
        
        quality["id"] = new_id
        new_qualities[new_id] = quality
    
    data["qualities"] = new_qualities
    
    # Transform Risks
    for risk_id, risk in data.get("risks", {}).items():
        # Add probability field
        if "likelihood" in risk and "probability" not in risk:
            risk["probability"] = risk["likelihood"]
        
        # Fix status
        if risk.get("status") == "monitoring":
            risk["status"] = "identified"
    
    # Transform Technical Debts
    for td_id, td in data.get("technicalDebts", {}).items():
        # Fix status
        if td.get("status") == "backlog":
            td["status"] = "identified"
    
    # Transform Components
    new_components = {}
    for comp_id, component in data.get("components", {}).items():
        # Fix ID pattern
        new_id = comp_id.replace("COMP-", "C-")
        
        # Fix interfaces
        if "interfaces" in component:
            component["interfaces"] = [
                {"name": interface, "description": "", "type": "provided"}
                for interface in component["interfaces"]
            ]
        
        component["id"] = new_id
        new_components[new_id] = component
    
    data["components"] = new_components
    
    # Save fixed data
    with open(fixed_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Fixed example data saved to {fixed_file}")
    
    # Replace original file with fixed data
    shutil.copy2(fixed_file, example_file)
    print(f"Replaced original example data with fixed data")
    
    return fixed_file

if __name__ == "__main__":
    fixed_file = fix_example_data()
    print(f"\nExample data fixed successfully! File: {fixed_file}")
    print("Please run force_reset_data.py and restart the application.")
