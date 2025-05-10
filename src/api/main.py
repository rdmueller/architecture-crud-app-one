"""Main FastAPI application."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any

# Import routers
from .routes import adrs, qualities, risks, technical_debts, components, architecture, export

app = FastAPI(
    title="Architecture CRUD API",
    description="API for managing architecture decision records and related entities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(architecture.router, prefix="/api/architecture", tags=["Architecture"])
app.include_router(adrs.router, prefix="/api/adrs", tags=["ADRs"])
app.include_router(qualities.router, prefix="/api/qualities", tags=["Qualities"])
app.include_router(risks.router, prefix="/api/risks", tags=["Risks"])
app.include_router(technical_debts.router, prefix="/api/technical-debts", tags=["Technical Debts"])
app.include_router(components.router, prefix="/api/components", tags=["Components"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])


@app.get("/", tags=["root"])
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to Architecture CRUD API"}


@app.get("/health", tags=["health"])
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors."""
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
            "status_code": 400
        },
    )
