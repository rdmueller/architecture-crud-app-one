#!/usr/bin/env python
"""Fix API client to properly handle data from the API."""
import os
import sys

def fix_api_client():
    """Fix the API client."""
    file_path = "src/ui/utils/api_client.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Fix the get_architecture function
    new_content = content.replace(
        "def get_architecture() -> Optional[Dict[str, Any]]:",
        "def get_architecture() -> Dict[str, Any]:"
    )
    
    new_content = new_content.replace(
        "return handle_response(response)",
        "data = handle_response(response)\n        print(f\"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}\") \n        return data"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed API client in {file_path}")

if __name__ == "__main__":
    fix_api_client()
    print("API client fixed successfully!")
