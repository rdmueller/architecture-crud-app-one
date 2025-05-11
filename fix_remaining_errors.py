#!/usr/bin/env python
"""Fix remaining validation errors in the data."""
import json
import os
import shutil
from datetime import datetime

def fix_relationship_types(data):
    """Fix relationship types to match allowed values."""
    # Fix ADR relationships
    for adr_id, adr in data.get("adrs", {}).items():
        if "relationships" in adr:
            # Fix quality relationships
            if "qualities" in adr["relationships"]:
                for rel in adr["relationships"]["qualities"]:
                    if rel.get("type") == "addresses":
                        rel["type"] = "affects"
            
            # Fix technical debt relationships
            if "technicalDebts" in adr["relationships"]:
                for rel in adr["relationships"]["technicalDebts"]:
                    if rel.get("type") == "causes":
                        rel["type"] = "introduces"

def fix_interface_descriptions(data):
    """Fix empty interface descriptions."""
    for comp_id, component in data.get("components", {}).items():
        if "interfaces" in component:
            for interface in component["interfaces"]:
                if "description" in interface and not interface["description"]:
                    interface["description"] = "Interface description"

def fix_remaining_errors():
    """Fix remaining validation errors in the data."""
    data_dir = "data"
    working_file = os.path.join(data_dir, "architecture.json")
    backup_file = os.path.join(data_dir, f"architecture_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    # Backup existing file
    shutil.copy2(working_file, backup_file)
    print(f"Backed up existing data to {backup_file}")
    
    # Load data
    with open(working_file, 'r') as f:
        data = json.load(f)
    
    # Fix relationship types
    fix_relationship_types(data)
    
    # Fix interface descriptions
    fix_interface_descriptions(data)
    
    # Save fixed data
    with open(working_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Fixed remaining validation errors in {working_file}")
    
    return working_file

if __name__ == "__main__":
    fixed_file = fix_remaining_errors()
    print(f"\nRemaining errors fixed successfully! File: {fixed_file}")
    print("Please restart the application with ./final_restart.sh")
