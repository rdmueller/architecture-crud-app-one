#!/usr/bin/env python
"""Fix relationship models to be more lenient with data formats."""
import os
import sys

def fix_adr_model():
    """Fix the ADR model to be more lenient with relationships."""
    file_path = "src/api/models/adr.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Find the Relationships class definition
    if "class Relationships(BaseModel):" in content:
        # Make relationships more lenient
        new_content = content.replace(
            "class Relationships(BaseModel):",
            """class Relationships(BaseModel):
    model_config = ConfigDict(extra='allow')"""
        )
        
        with open(file_path, "w") as f:
            f.write(new_content)
        
        print(f"Fixed ADR model in {file_path}")
    else:
        print(f"Could not find Relationships class in {file_path}")

def fix_alternative_model():
    """Fix the Alternative model to accept advantages/disadvantages."""
    file_path = "src/api/models/adr.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Find the Alternative class definition
    if "class Alternative(BaseModel):" in content:
        # Replace the Alternative class with a more lenient version
        old_alternative = """class Alternative(BaseModel):
    \"\"\"Alternative solution considered in an ADR.\"\"\"
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)"""
        
        new_alternative = """class Alternative(BaseModel):
    \"\"\"Alternative solution considered in an ADR.\"\"\"
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    advantages: List[str] = Field(default_factory=list)  # For backward compatibility
    disadvantages: List[str] = Field(default_factory=list)  # For backward compatibility
    
    model_config = ConfigDict(extra='allow')
    
    def model_post_init(self, __context):
        \"\"\"Convert advantages/disadvantages to pros/cons.\"\"\"
        if not self.pros and self.advantages:
            self.pros = self.advantages
        if not self.cons and self.disadvantages:
            self.cons = self.disadvantages"""
        
        new_content = content.replace(old_alternative, new_alternative)
        
        with open(file_path, "w") as f:
            f.write(new_content)
        
        print(f"Fixed Alternative model in {file_path}")
    else:
        print(f"Could not find Alternative class in {file_path}")

def fix_metric_model():
    """Fix the Metric model to accept metricName/targetValue."""
    file_path = "src/api/models/quality.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Find the Metric class definition
    if "class Metric(BaseModel):" in content:
        # Replace the Metric class with a more lenient version
        old_metric = """class Metric(BaseModel):
    \"\"\"Metric for measuring a quality requirement.\"\"\"
    name: str = Field(min_length=1, max_length=100)
    target: str = Field(min_length=1, max_length=100)
    measure: str = Field(min_length=1, max_length=100)"""
        
        new_metric = """class Metric(BaseModel):
    \"\"\"Metric for measuring a quality requirement.\"\"\"
    name: str = Field(min_length=1, max_length=100, default="")
    target: str = Field(min_length=1, max_length=100, default="")
    measure: str = Field(min_length=1, max_length=100, default="")
    metricName: str = Field(min_length=0, max_length=100, default="")  # For backward compatibility
    targetValue: str = Field(min_length=0, max_length=100, default="")  # For backward compatibility
    unit: str = Field(min_length=0, max_length=100, default="")  # For backward compatibility
    
    model_config = ConfigDict(extra='allow')
    
    def model_post_init(self, __context):
        \"\"\"Convert metricName/targetValue/unit to name/target/measure.\"\"\"
        if not self.name and self.metricName:
            self.name = self.metricName
        if not self.target and self.targetValue:
            self.target = self.targetValue
        if not self.measure and self.unit:
            self.measure = self.unit"""
        
        new_content = content.replace(old_metric, new_metric)
        
        with open(file_path, "w") as f:
            f.write(new_content)
        
        print(f"Fixed Metric model in {file_path}")
    else:
        print(f"Could not find Metric class in {file_path}")

def add_config_import():
    """Add ConfigDict import to models."""
    files = [
        "src/api/models/adr.py",
        "src/api/models/quality.py"
    ]
    
    for file_path in files:
        with open(file_path, "r") as f:
            content = f.read()
        
        if "from pydantic import BaseModel, Field" in content and "ConfigDict" not in content:
            new_content = content.replace(
                "from pydantic import BaseModel, Field",
                "from pydantic import BaseModel, Field, ConfigDict"
            )
            
            with open(file_path, "w") as f:
                f.write(new_content)
            
            print(f"Added ConfigDict import to {file_path}")

if __name__ == "__main__":
    add_config_import()
    fix_adr_model()
    fix_alternative_model()
    fix_metric_model()
    print("\nRelationship models fixed successfully!")
    print("Please restart the application.")
