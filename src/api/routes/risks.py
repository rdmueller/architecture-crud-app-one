"""Risk routes."""
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from src.data.repository import ArchitectureRepository
from src.api.models.risk import Risk
from src.api.dependencies import get_repository

router = APIRouter()


@router.get("", response_model=List[Risk])
async def list_risks(repo: ArchitectureRepository = Depends(get_repository)) -> List[Risk]:
    """List all risks."""
    architecture = repo.load()
    return list(architecture.risks.values())


@router.get("/{risk_id}", response_model=Risk)
async def get_risk(risk_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> Risk:
    """Get a specific risk."""
    risk = repo.get_risk(risk_id)
    if not risk:
        raise HTTPException(status_code=404, detail=f"Risk {risk_id} not found")
    return risk


@router.post("", response_model=Risk, status_code=201)
async def create_risk(risk: Risk, repo: ArchitectureRepository = Depends(get_repository)) -> Risk:
    """Create a new risk."""
    # Check if risk already exists
    existing = repo.get_risk(risk.id)
    if existing:
        raise HTTPException(status_code=409, detail=f"Risk {risk.id} already exists")
    
    repo.add_risk(risk)
    return risk


@router.put("/{risk_id}", response_model=Risk)
async def update_risk(risk_id: str, risk: Risk, repo: ArchitectureRepository = Depends(get_repository)) -> Risk:
    """Update an existing risk."""
    # Check if risk exists
    existing = repo.get_risk(risk_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Risk {risk_id} not found")
    
    # Ensure ID consistency
    if risk.id != risk_id:
        raise HTTPException(status_code=400, detail="Risk ID mismatch")
    
    repo.update_risk(risk_id, risk)
    return risk


@router.delete("/{risk_id}", status_code=204)
async def delete_risk(risk_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> None:
    """Delete a risk."""
    # Check if risk exists
    existing = repo.get_risk(risk_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Risk {risk_id} not found")
    
    repo.delete_risk(risk_id)
