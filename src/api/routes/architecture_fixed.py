"""Routes for complete architecture data."""
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
    """Get complete architecture data."""
    data = repo.load()
    # data is already an Architecture object
    return data.model_dump()
