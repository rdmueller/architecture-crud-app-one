"""Mock API server for testing."""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import json
from datetime import datetime


app = FastAPI()


# In-memory storage
storage: Dict[str, Dict[str, Any]] = {
    "adrs": {},
    "qualities": {},
    "risks": {},
    "technicalDebts": {},
    "components": {}
}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Architecture CRUD API",
        "description": "API for managing architecture documentation"
    }


@app.get("/api/architecture")
async def get_architecture():
    """Get complete architecture."""
    return storage


@app.get("/api/{entity_type}")
async def list_entities(entity_type: str):
    """List all entities of a type."""
    if entity_type not in storage:
        raise HTTPException(status_code=404, detail=f"Entity type {entity_type} not found")
    return list(storage[entity_type].values())


@app.get("/api/{entity_type}/{entity_id}")
async def get_entity(entity_type: str, entity_id: str):
    """Get a specific entity."""
    if entity_type not in storage:
        raise HTTPException(status_code=404, detail=f"Entity type {entity_type} not found")
    if entity_id not in storage[entity_type]:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    return storage[entity_type][entity_id]


@app.post("/api/{entity_type}")
async def create_entity(entity_type: str, entity: Dict[str, Any]):
    """Create a new entity."""
    if entity_type not in storage:
        raise HTTPException(status_code=404, detail=f"Entity type {entity_type} not found")
    
    entity_id = entity.get("id")
    if not entity_id:
        raise HTTPException(status_code=422, detail="Entity must have an id")
    
    if entity_id in storage[entity_type]:
        raise HTTPException(status_code=409, detail=f"Entity {entity_id} already exists")
    
    storage[entity_type][entity_id] = entity
    return JSONResponse(status_code=201, content=entity)


@app.put("/api/{entity_type}/{entity_id}")
async def update_entity(entity_type: str, entity_id: str, entity: Dict[str, Any]):
    """Update an existing entity."""
    if entity_type not in storage:
        raise HTTPException(status_code=404, detail=f"Entity type {entity_type} not found")
    if entity_id not in storage[entity_type]:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    
    entity["id"] = entity_id  # Ensure ID consistency
    storage[entity_type][entity_id] = entity
    return entity


@app.delete("/api/{entity_type}/{entity_id}")
async def delete_entity(entity_type: str, entity_id: str):
    """Delete an entity."""
    if entity_type not in storage:
        raise HTTPException(status_code=404, detail=f"Entity type {entity_type} not found")
    if entity_id not in storage[entity_type]:
        raise HTTPException(status_code=404, detail=f"Entity {entity_id} not found")
    
    del storage[entity_type][entity_id]
    return JSONResponse(status_code=204, content=None)


@app.post("/api/export/asciidoc")
async def export_asciidoc():
    """Export architecture as AsciiDoc."""
    # Simple mock implementation
    return {
        "status": "success",
        "message": "Export completed",
        "files": ["architecture.adoc"]
    }


# Fix for kebab-case endpoints
@app.get("/api/technical-debts")
async def list_technical_debts():
    """List all technical debts."""
    return await list_entities("technicalDebts")


@app.get("/api/technical-debts/{debt_id}")
async def get_technical_debt(debt_id: str):
    """Get a specific technical debt."""
    return await get_entity("technicalDebts", debt_id)


@app.post("/api/technical-debts")
async def create_technical_debt(debt: Dict[str, Any]):
    """Create a new technical debt."""
    return await create_entity("technicalDebts", debt)


@app.put("/api/technical-debts/{debt_id}")
async def update_technical_debt(debt_id: str, debt: Dict[str, Any]):
    """Update an existing technical debt."""
    return await update_entity("technicalDebts", debt_id, debt)


@app.delete("/api/technical-debts/{debt_id}")
async def delete_technical_debt(debt_id: str):
    """Delete a technical debt."""
    return await delete_entity("technicalDebts", debt_id)
