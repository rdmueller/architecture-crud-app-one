#!/usr/bin/env python
"""Fix repository to properly load data."""
import os
import sys
import json

def fix_repository():
    """Fix the repository."""
    file_path = "src/data/repository.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Add debug output to load method
    new_content = content.replace(
        "def load(self) -> Architecture:",
        "def load(self) -> Architecture:\n        \"\"\"Load architecture from file.\"\"\"\n        print(f\"Loading architecture from {self.file_path}\")"
    )
    
    # Add more detailed error handling
    new_content = new_content.replace(
        "except (json.JSONDecodeError, ValueError):",
        "except (json.JSONDecodeError, ValueError) as e:\n            print(f\"Error loading architecture: {e}\")"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed repository in {file_path}")

def test_repository():
    """Test the repository directly."""
    from src.data.repository import ArchitectureRepository
    
    # Create repository with absolute path
    data_file = os.path.abspath("data/architecture.json")
    repo = ArchitectureRepository(data_file)
    
    # Load architecture
    print(f"Testing repository with file: {data_file}")
    architecture = repo.load()
    
    # Print architecture details
    print(f"Architecture loaded:")
    print(f"- Metadata: {architecture.metadata.title}")
    print(f"- ADRs: {len(architecture.adrs)}")
    print(f"- Qualities: {len(architecture.qualities)}")
    print(f"- Risks: {len(architecture.risks)}")
    print(f"- Technical Debts: {len(architecture.technicalDebts)}")
    print(f"- Components: {len(architecture.components)}")
    
    # Print first ADR if available
    if architecture.adrs:
        first_adr_id = next(iter(architecture.adrs))
        first_adr = architecture.adrs[first_adr_id]
        print(f"\nFirst ADR:")
        print(f"- ID: {first_adr.id}")
        print(f"- Title: {first_adr.title}")
        print(f"- Status: {first_adr.status}")

if __name__ == "__main__":
    fix_repository()
    print("Repository fixed successfully!")
    
    # Test repository
    print("\nTesting repository...")
    try:
        # Add src to path
        sys.path.insert(0, os.path.abspath("."))
        test_repository()
    except Exception as e:
        print(f"Error testing repository: {e}")
