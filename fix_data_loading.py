#!/usr/bin/env python
"""Fix data loading issues in the Architecture CRUD application."""
import os
import sys
import json
import shutil
from datetime import datetime

def debug_architecture_file():
    """Debug the architecture.json file."""
    data_file = "data/architecture.json"
    
    print(f"Checking {data_file}...")
    
    if not os.path.exists(data_file):
        print(f"ERROR: {data_file} does not exist!")
        return False
    
    try:
        with open(data_file, 'r') as f:
            content = f.read()
            
        if not content.strip():
            print(f"ERROR: {data_file} is empty!")
            return False
            
        data = json.loads(content)
        
        # Check if data has the expected structure
        if not isinstance(data, dict):
            print(f"ERROR: {data_file} does not contain a JSON object!")
            return False
            
        # Check for required fields
        required_fields = ["metadata", "adrs", "qualities", "risks", "technicalDebts", "components"]
        for field in required_fields:
            if field not in data:
                print(f"ERROR: {data_file} is missing required field '{field}'!")
                return False
        
        # Check if there are any ADRs
        if not data["adrs"]:
            print(f"WARNING: No ADRs found in {data_file}")
        else:
            print(f"Found {len(data['adrs'])} ADRs")
            
        # Check if there are any qualities
        if not data["qualities"]:
            print(f"WARNING: No qualities found in {data_file}")
        else:
            print(f"Found {len(data['qualities'])} qualities")
            
        # Check if there are any risks
        if not data["risks"]:
            print(f"WARNING: No risks found in {data_file}")
        else:
            print(f"Found {len(data['risks'])} risks")
            
        # Check if there are any technical debts
        if not data["technicalDebts"]:
            print(f"WARNING: No technical debts found in {data_file}")
        else:
            print(f"Found {len(data['technicalDebts'])} technical debts")
            
        # Check if there are any components
        if not data["components"]:
            print(f"WARNING: No components found in {data_file}")
        else:
            print(f"Found {len(data['components'])} components")
            
        print(f"{data_file} appears to be valid.")
        return True
        
    except json.JSONDecodeError as e:
        print(f"ERROR: {data_file} contains invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to process {data_file}: {e}")
        return False

def reset_example_data():
    """Reset the architecture.json file with example data."""
    data_dir = "data"
    working_file = os.path.join(data_dir, "architecture.json")
    example_file = os.path.join(data_dir, "example_architecture.json")
    backup_file = os.path.join(data_dir, f"architecture_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    # Backup existing file if it exists
    if os.path.exists(working_file):
        print(f"Backing up existing {working_file} to {backup_file}")
        shutil.copy2(working_file, backup_file)
    
    # Copy example data
    if os.path.exists(example_file):
        print(f"Copying example data from {example_file} to {working_file}")
        shutil.copy2(example_file, working_file)
        return True
    else:
        print(f"ERROR: Example file not found: {example_file}")
        return False

def main():
    """Main function."""
    print("Architecture CRUD Data Fixer")
    print("===========================")
    
    # First, debug the current architecture file
    if debug_architecture_file():
        choice = input("\nDo you want to reset the data with example data? (y/n): ")
        if choice.lower() == 'y':
            if reset_example_data():
                print("\nData reset successfully!")
                print("Please restart the application.")
            else:
                print("\nFailed to reset data.")
        else:
            print("\nNo changes made.")
    else:
        print("\nThe architecture.json file appears to be invalid.")
        choice = input("Do you want to reset it with example data? (y/n): ")
        if choice.lower() == 'y':
            if reset_example_data():
                print("\nData reset successfully!")
                print("Please restart the application.")
            else:
                print("\nFailed to reset data.")
        else:
            print("\nNo changes made.")

if __name__ == "__main__":
    main()
