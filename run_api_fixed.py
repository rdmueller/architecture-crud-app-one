#!/usr/bin/env python
"""Run the FastAPI application."""
import os
import sys
import uvicorn
from pathlib import Path

if __name__ == "__main__":
    # Add src directory to Python path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    # Set default data file if not specified
    if "ARCHITECTURE_DATA_FILE" not in os.environ:
        os.environ["ARCHITECTURE_DATA_FILE"] = "data/architecture.json"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8082,
        reload=True
    )
