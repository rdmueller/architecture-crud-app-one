"""Component routes."""
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from src.data.repository import ArchitectureRepository
from src.api.models.component import Component
from src.api.dependencies import get_repository

router = APIRouter()


@router.get("", response_model=List[Component])
async def list_components(repo: ArchitectureRepository = Depends(get_repository)) -> List[Component]:
    """List all components."""
    architecture = repo.load()
    return list(architecture.components.values())


@router.get("/{component_id}", response_model=Component)
async def get_component(component_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> Component:
    """Get a specific component."""
    component = repo.get_component(component_id)
    if not component:
        raise HTTPException(status_code=404, detail=f"Component {component_id} not found")
    return component


@router.post("", response_model=Component, status_code=201)
async def create_component(component: Component, repo: ArchitectureRepository = Depends(get_repository)) -> Component:
    """Create a new component."""
    # Check if component already exists
    existing = repo.get_component(component.id)
    if existing:
        raise HTTPException(status_code=409, detail=f"Component {component.id} already exists")
    
    repo.add_component(component)
    return component


@router.put("/{component_id}", response_model=Component)
async def update_component(component_id: str, component: Component, repo: ArchitectureRepository = Depends(get_repository)) -> Component:
    """Update an existing component."""
    # Check if component exists
    existing = repo.get_component(component_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Component {component_id} not found")
    
    # Ensure ID consistency
    if component.id != component_id:
        raise HTTPException(status_code=400, detail="Component ID mismatch")
    
    repo.update_component(component_id, component)
    return component


@router.delete("/{component_id}", status_code=204)
async def delete_component(component_id: str, repo: ArchitectureRepository = Depends(get_repository)) -> None:
    """Delete a component."""
    # Check if component exists
    existing = repo.get_component(component_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Component {component_id} not found")
    
    repo.delete_component(component_id)
