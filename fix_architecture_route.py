#!/usr/bin/env python
"""Fix architecture route to properly return data."""
import os
import sys

def fix_architecture_route():
    """Fix the architecture route."""
    file_path = "src/api/routes/architecture.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Replace the entire route implementation
    new_content = """\"\"\"Routes for complete architecture data.\"\"\"
from fastapi import APIRouter, Depends
from typing import Dict, Any

from src.api.dependencies import get_repository
from src.api.models.architecture import Architecture
from src.data.repository import ArchitectureRepository

router = APIRouter()


@router.get("/", response_model=Architecture)
async def get_architecture(
    repo: ArchitectureRepository = Depends(get_repository)
) -> Dict[str, Any]:
    \"\"\"Get complete architecture data.\"\"\"
    print("Architecture route called")
    data = repo.load()
    print(f"Architecture route: ADRs: {len(data.adrs)}, Qualities: {len(data.qualities)}")
    
    # Convert to dict and return
    result = data.model_dump(mode='json')
    print(f"Architecture route returning: ADRs: {len(result.get('adrs', {}))}, Qualities: {len(result.get('qualities', {}))}")
    return result
"""
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed architecture route in {file_path}")

if __name__ == "__main__":
    fix_architecture_route()
    print("Architecture route fixed successfully!")
