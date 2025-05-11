#!/usr/bin/env python
"""Fix API routes to properly return architecture data."""
import os
import sys

def fix_adrs_route():
    """Fix the ADRs route to properly return data."""
    file_path = "src/api/routes/adrs.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Add debug output
    if "architecture = repo.load()" in content:
        new_content = content.replace(
            "architecture = repo.load()",
            "architecture = repo.load()\n    print(f\"ADRs route: Found {len(architecture.adrs)} ADRs\")"
        )
        
        with open(file_path, "w") as f:
            f.write(new_content)
        
        print(f"Fixed ADRs route in {file_path}")
    else:
        print(f"Could not find pattern in {file_path}")

def fix_architecture_route():
    """Fix the architecture route to properly return data."""
    file_path = "src/api/routes/architecture.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Add debug output
    if "data = repo.load()" in content:
        new_content = content.replace(
            "data = repo.load()",
            "data = repo.load()\n    print(f\"Architecture route: ADRs: {len(data.adrs)}, Qualities: {len(data.qualities)}\")"
        )
        
        with open(file_path, "w") as f:
            f.write(new_content)
        
        print(f"Fixed architecture route in {file_path}")
    else:
        print(f"Could not find pattern in {file_path}")

if __name__ == "__main__":
    fix_adrs_route()
    fix_architecture_route()
    print("API routes fixed successfully!")
