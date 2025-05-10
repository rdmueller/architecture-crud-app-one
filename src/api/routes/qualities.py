"""Quality requirement routes."""
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from src.data.repository import ArchitectureRepository
from src.api.models.quality import Quality
from src.api.dependencies import get_repository

router = APIRouter()


@router.get("", response_model=List[Quality])
async def list_qualities(repo: ArchitectureRepository = Depends(get_repository)) -> List[Quality]:
    """List all quality requirements."""
    architecture = repo.load()
    return list(architecture.qualities.values())


@router.get("/{quality_id}", response_model=Quality)
async def get_quality(quality_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> Quality:
    """Get a specific quality requirement."""
    quality = repo.get_quality(quality_id)
    if not quality:
        raise HTTPException(status_code=404, detail=f"Quality {quality_id} not found")
    return quality


@router.post("", response_model=Quality, status_code=201)
async def create_quality(quality: Quality, repo: ArchitectureRepository = Depends(get_repository)) -> Quality:
    """Create a new quality requirement."""
    # Check if quality already exists
    existing = repo.get_quality(quality.id)
    if existing:
        raise HTTPException(status_code=409, detail=f"Quality {quality.id} already exists")
    
    repo.add_quality(quality)
    return quality


@router.put("/{quality_id}", response_model=Quality)
async def update_quality(quality_id: str, quality: Quality, repo: ArchitectureRepository = Depends(get_repository)) -> Quality:
    """Update an existing quality requirement."""
    # Check if quality exists
    existing = repo.get_quality(quality_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Quality {quality_id} not found")
    
    # Ensure ID consistency
    if quality.id != quality_id:
        raise HTTPException(status_code=400, detail="Quality ID mismatch")
    
    repo.update_quality(quality_id, quality)
    return quality


@router.delete("/{quality_id}", status_code=204)
async def delete_quality(quality_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> None:
    """Delete a quality requirement."""
    # Check if quality exists
    existing = repo.get_quality(quality_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Quality {quality_id} not found")
    
    repo.delete_quality(quality_id)
