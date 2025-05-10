#!/usr/bin/env python
"""Run the FastAPI application with initialized data."""
import os
import subprocess
import sys

# Initialize data first
print("Initializing data...")
subprocess.run([sys.executable, "initialize_data.py"])

# Set default data file if not specified
if "ARCHITECTURE_DATA_FILE" not in os.environ:
    os.environ["ARCHITECTURE_DATA_FILE"] = "data/architecture.json"

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Run the API
print("\nStarting API server...")
import uvicorn
uvicorn.run(
    "src.api.main:app",
    host="0.0.0.0",
    port=8082,
    reload=True
)
