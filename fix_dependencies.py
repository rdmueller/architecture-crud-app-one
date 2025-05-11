#!/usr/bin/env python
"""Fix dependencies to properly load data."""
import os
import sys

def fix_dependencies():
    """Fix the dependencies."""
    file_path = "src/api/dependencies.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Add debug output to get_repository function
    new_content = content.replace(
        "def get_repository() -> ArchitectureRepository:",
        "def get_repository() -> ArchitectureRepository:\n    \"\"\"Get repository instance.\"\"\"\n    print(\"get_repository called\")"
    )
    
    # Add more detailed path handling
    new_content = new_content.replace(
        "data_file = os.environ.get(\"ARCHITECTURE_DATA_FILE\", \"data/architecture.json\")",
        "data_file = os.environ.get(\"ARCHITECTURE_DATA_FILE\", \"data/architecture.json\")\n    # Convert to absolute path if not already\n    if not os.path.isabs(data_file):\n        data_file = os.path.abspath(data_file)\n    print(f\"Using data file: {data_file}\")"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed dependencies in {file_path}")

if __name__ == "__main__":
    fix_dependencies()
    print("Dependencies fixed successfully!")
