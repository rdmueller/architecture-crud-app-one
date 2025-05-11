#!/usr/bin/env python
"""Fix models to be more lenient with data formats."""
import os
import sys

def fix_quality_model():
    """Fix the quality model to accept QA- prefix."""
    file_path = "src/api/models/quality.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Make ID pattern more lenient
    new_content = content.replace(
        "id: str = Field(pattern=r'^QR-[0-9]{3}$')",
        "id: str = Field(pattern=r'^Q[AR]-[0-9]{3}$')"
    )
    
    # Make priority more lenient
    new_content = new_content.replace(
        "priority: Literal['high', 'medium', 'low']",
        "priority: str"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed quality model in {file_path}")

def fix_component_model():
    """Fix the component model to accept COMP- prefix."""
    file_path = "src/api/models/component.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Make ID pattern more lenient
    new_content = content.replace(
        "id: str = Field(pattern=r'^C-[0-9]{3}$')",
        "id: str = Field(pattern=r'^(C|COMP)-[0-9]{3}$')"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed component model in {file_path}")

def fix_risk_model():
    """Fix the risk model to accept monitoring status."""
    file_path = "src/api/models/risk.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Make status more lenient
    new_content = content.replace(
        "status: Literal['identified', 'mitigated', 'accepted', 'closed']",
        "status: str"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed risk model in {file_path}")

def fix_technical_debt_model():
    """Fix the technical debt model to accept backlog status."""
    file_path = "src/api/models/technical_debt.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Make status more lenient
    new_content = content.replace(
        "status: Literal['identified', 'planned', 'in_progress', 'resolved', 'accepted']",
        "status: str"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed technical debt model in {file_path}")

def fix_repository():
    """Fix the repository to be more lenient with data loading."""
    file_path = "src/data/repository.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Add more detailed error handling
    new_content = content.replace(
        "except (json.JSONDecodeError, ValueError):",
        "except (json.JSONDecodeError, ValueError) as e:\n            print(f\"Error loading architecture: {e}\")\n            print(\"Returning default architecture\")"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed repository in {file_path}")

if __name__ == "__main__":
    fix_quality_model()
    fix_component_model()
    fix_risk_model()
    fix_technical_debt_model()
    fix_repository()
    print("\nModels fixed successfully!")
    print("Please restart the application.")
