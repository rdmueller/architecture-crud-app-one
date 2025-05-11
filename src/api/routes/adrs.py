"""ADR routes."""
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from src.data.repository import ArchitectureRepository
from src.api.models.adr import ADR
from src.api.dependencies import get_repository

router = APIRouter()


@router.get("", response_model=List[ADR])
async def list_adrs(repo: ArchitectureRepository = Depends(get_repository)) -> List[ADR]:
    """List all ADRs."""
    architecture = repo.load()
    print(f"ADRs route: Found {len(architecture.adrs)} ADRs")
    return list(architecture.adrs.values())


@router.get("/{adr_id}", response_model=ADR)
async def get_adr(adr_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> ADR:
    """Get a specific ADR."""
    adr = repo.get_adr(adr_id)
    if not adr:
        raise HTTPException(status_code=404, detail=f"ADR {adr_id} not found")
    return adr


@router.post("", response_model=ADR, status_code=201)
async def create_adr(adr: ADR, repo: ArchitectureRepository = Depends(get_repository)) -> ADR:
    """Create a new ADR."""
    # Check if ADR already exists
    existing = repo.get_adr(adr.id)
    if existing:
        raise HTTPException(status_code=409, detail=f"ADR {adr.id} already exists")
    
    repo.add_adr(adr)
    return adr


@router.put("/{adr_id}", response_model=ADR)
async def update_adr(adr_id: str, adr: ADR, repo: ArchitectureRepository = Depends(get_repository)) -> ADR:
    """Update an existing ADR."""
    # Check if ADR exists
    existing = repo.get_adr(adr_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"ADR {adr_id} not found")
    
    # Ensure ID consistency
    if adr.id != adr_id:
        raise HTTPException(status_code=400, detail="ADR ID mismatch")
    
    repo.update_adr(adr_id, adr)
    return adr


@router.delete("/{adr_id}", status_code=204)
async def delete_adr(adr_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> None:
    """Delete an ADR."""
    # Check if ADR exists
    existing = repo.get_adr(adr_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"ADR {adr_id} not found")
    
    repo.delete_adr(adr_id)
