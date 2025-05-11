#!/usr/bin/env python
"""Fix environment variables for the Architecture CRUD application."""
import os
import sys
import json
import shutil
from datetime import datetime

def check_environment():
    """Check environment variables."""
    print("Checking environment variables...")
    
    # Check ARCHITECTURE_DATA_FILE
    data_file = os.environ.get("ARCHITECTURE_DATA_FILE")
    if data_file:
        print(f"ARCHITECTURE_DATA_FILE is set to: {data_file}")
    else:
        print("ARCHITECTURE_DATA_FILE is not set")
        
    # Check if the file exists
    if data_file and os.path.exists(data_file):
        print(f"File exists: {data_file}")
        
        # Check file size
        size = os.path.getsize(data_file)
        print(f"File size: {size} bytes")
        
        # Check file content
        try:
            with open(data_file, 'r') as f:
                data = json.load(f)
                print(f"File contains valid JSON")
                print(f"ADRs: {len(data.get('adrs', {}))}")
                print(f"Qualities: {len(data.get('qualities', {}))}")
                print(f"Risks: {len(data.get('risks', {}))}")
                print(f"Technical Debts: {len(data.get('technicalDebts', {}))}")
                print(f"Components: {len(data.get('components', {}))}")
        except Exception as e:
            print(f"Error reading file: {e}")
    elif data_file:
        print(f"File does not exist: {data_file}")
    
    return data_file

def fix_environment():
    """Fix environment variables."""
    # Set ARCHITECTURE_DATA_FILE to the absolute path
    data_file = os.path.abspath("data/architecture.json")
    os.environ["ARCHITECTURE_DATA_FILE"] = data_file
    print(f"Set ARCHITECTURE_DATA_FILE to: {data_file}")
    
    # Check if the file exists
    if not os.path.exists(data_file):
        print(f"File does not exist: {data_file}")
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        
        # Copy example data
        example_file = os.path.abspath("data/example_architecture.json")
        if os.path.exists(example_file):
            print(f"Copying example data from {example_file} to {data_file}")
            shutil.copy2(example_file, data_file)
        else:
            print(f"Example file not found: {example_file}")
            
            # Create empty architecture file
            print(f"Creating empty architecture file: {data_file}")
            with open(data_file, 'w') as f:
                json.dump({
                    "metadata": {
                        "title": "Architecture",
                        "system": "system",
                        "version": "1.0.0",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "authors": []
                    },
                    "adrs": {},
                    "qualities": {},
                    "risks": {},
                    "technicalDebts": {},
                    "components": {}
                }, f, indent=2)
    
    return data_file

def main():
    """Main function."""
    print("Architecture CRUD Environment Fixer")
    print("==================================")
    
    # Check environment
    data_file = check_environment()
    
    # Ask if user wants to fix environment
    choice = input("\nDo you want to fix the environment? (y/n): ")
    if choice.lower() == 'y':
        data_file = fix_environment()
        print(f"\nEnvironment fixed. Data file: {data_file}")
        print("Please restart the application.")
    else:
        print("\nNo changes made.")

if __name__ == "__main__":
    main()
