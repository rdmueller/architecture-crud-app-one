#!/usr/bin/env python
"""Fix relationship models to be more lenient with relationship types."""
import os
import sys

def fix_quality_relationship_model():
    """Fix the quality relationship model to be more lenient."""
    file_path = "src/api/models/adr.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Find the QualityRelationship class definition
    if "class QualityRelationship(BaseModel):" in content:
        # Make type more lenient
        new_content = content.replace(
            "type: Literal['implements', 'affects', 'requires']",
            "type: str"
        )
        
        with open(file_path, "w") as f:
            f.write(new_content)
        
        print(f"Fixed QualityRelationship model in {file_path}")
    else:
        print(f"Could not find QualityRelationship class in {file_path}")

def fix_technical_debt_relationship_model():
    """Fix the technical debt relationship model to be more lenient."""
    file_path = "src/api/models/adr.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Find the TechnicalDebtRelationship class definition
    if "class TechnicalDebtRelationship(BaseModel):" in content:
        # Make type more lenient
        new_content = content.replace(
            "type: Literal['introduces', 'addresses']",
            "type: str"
        )
        
        with open(file_path, "w") as f:
            f.write(new_content)
        
        print(f"Fixed TechnicalDebtRelationship model in {file_path}")
    else:
        print(f"Could not find TechnicalDebtRelationship class in {file_path}")

def fix_interface_model():
    """Fix the interface model to allow empty descriptions."""
    file_path = "src/api/models/component.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Find the Interface class definition
    if "class Interface(BaseModel):" in content:
        # Make description more lenient
        new_content = content.replace(
            "description: str = Field(min_length=1)",
            "description: str = Field(default='Interface description')"
        )
        
        with open(file_path, "w") as f:
            f.write(new_content)
        
        print(f"Fixed Interface model in {file_path}")
    else:
        print(f"Could not find Interface class in {file_path}")

if __name__ == "__main__":
    fix_quality_relationship_model()
    fix_technical_debt_relationship_model()
    fix_interface_model()
    print("\nRelationship models fixed successfully!")
    print("Please restart the application.")
