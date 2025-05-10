"""Technical debt routes."""
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from src.data.repository import ArchitectureRepository
from src.api.models.technical_debt import TechnicalDebt
from src.api.dependencies import get_repository

router = APIRouter()


@router.get("", response_model=List[TechnicalDebt])
async def list_technical_debts(repo: ArchitectureRepository = Depends(get_repository)) -> List[TechnicalDebt]:
    """List all technical debts."""
    architecture = repo.load()
    return list(architecture.technicalDebts.values())


@router.get("/{td_id}", response_model=TechnicalDebt)
async def get_technical_debt(td_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> TechnicalDebt:
    """Get a specific technical debt."""
    td = repo.get_technical_debt(td_id)
    if not td:
        raise HTTPException(status_code=404, detail=f"Technical debt {td_id} not found")
    return td


@router.post("", response_model=TechnicalDebt, status_code=201)
async def create_technical_debt(td: TechnicalDebt, repo: ArchitectureRepository = Depends(get_repository)) -> TechnicalDebt:
    """Create a new technical debt."""
    # Check if technical debt already exists
    existing = repo.get_technical_debt(td.id)
    if existing:
        raise HTTPException(status_code=409, detail=f"Technical debt {td.id} already exists")
    
    repo.add_technical_debt(td)
    return td


@router.put("/{td_id}", response_model=TechnicalDebt)
async def update_technical_debt(td_id: str, td: TechnicalDebt, repo: ArchitectureRepository = Depends(get_repository)) -> TechnicalDebt:
    """Update an existing technical debt."""
    # Check if technical debt exists
    existing = repo.get_technical_debt(td_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Technical debt {td_id} not found")
    
    # Ensure ID consistency
    if td.id != td_id:
        raise HTTPException(status_code=400, detail="Technical debt ID mismatch")
    
    repo.update_technical_debt(td_id, td)
    return td


@router.delete("/{td_id}", status_code=204)
async def delete_technical_debt(td_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> None:
    """Delete a technical debt."""
    # Check if technical debt exists
    existing = repo.get_technical_debt(td_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Technical debt {td_id} not found")
    
    repo.delete_technical_debt(td_id)
