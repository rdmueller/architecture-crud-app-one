#!/usr/bin/env python
"""Run the FastAPI application with debug output."""
import os
import sys
import json
import uvicorn

def check_data_file():
    """Check if the data file exists and has content."""
    data_file = os.environ.get("ARCHITECTURE_DATA_FILE", "data/architecture.json")
    
    # Convert to absolute path if not already
    if not os.path.isabs(data_file):
        data_file = os.path.abspath(data_file)
    
    print(f"Checking data file: {data_file}")
    
    if not os.path.exists(data_file):
        print(f"ERROR: Data file does not exist: {data_file}")
        return False
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            print(f"Data file contains valid JSON")
            print(f"ADRs: {len(data.get('adrs', {}))}")
            print(f"Qualities: {len(data.get('qualities', {}))}")
            print(f"Risks: {len(data.get('risks', {}))}")
            print(f"Technical Debts: {len(data.get('technicalDebts', {}))}")
            print(f"Components: {len(data.get('components', {}))}")
            return True
    except Exception as e:
        print(f"ERROR: Failed to read data file: {e}")
        return False

if __name__ == "__main__":
    print("Starting API server with debug output...")
    
    # Set data file to absolute path
    data_file = os.path.abspath("data/architecture.json")
    os.environ["ARCHITECTURE_DATA_FILE"] = data_file
    print(f"Set ARCHITECTURE_DATA_FILE to: {data_file}")
    
    # Check data file
    check_data_file()
    
    # Run API
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8082,
        reload=False,
        workers=1
    )
