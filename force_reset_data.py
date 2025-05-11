#!/usr/bin/env python
"""Force reset of architecture data."""
import os
import sys
import json
import shutil
from datetime import datetime

def force_reset_data():
    """Force reset of architecture data."""
    data_dir = "data"
    working_file = os.path.join(data_dir, "architecture.json")
    example_file = os.path.join(data_dir, "example_architecture.json")
    backup_file = os.path.join(data_dir, f"architecture_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    print(f"Forcing reset of architecture data...")
    
    # Backup existing file if it exists
    if os.path.exists(working_file):
        print(f"Backing up existing {working_file} to {backup_file}")
        shutil.copy2(working_file, backup_file)
    
    # Copy example data
    if os.path.exists(example_file):
        print(f"Copying example data from {example_file} to {working_file}")
        shutil.copy2(example_file, working_file)
        
        # Verify the copy
        try:
            with open(working_file, 'r') as f:
                data = json.load(f)
                print(f"Verification: File contains valid JSON")
                print(f"ADRs: {len(data.get('adrs', {}))}")
                print(f"Qualities: {len(data.get('qualities', {}))}")
                print(f"Risks: {len(data.get('risks', {}))}")
                print(f"Technical Debts: {len(data.get('technicalDebts', {}))}")
                print(f"Components: {len(data.get('components', {}))}")
                
                return True
        except Exception as e:
            print(f"Error verifying file: {e}")
            return False
    else:
        print(f"ERROR: Example file not found: {example_file}")
        return False

if __name__ == "__main__":
    if force_reset_data():
        print("\nData reset successfully!")
        print("Please restart the application.")
    else:
        print("\nFailed to reset data.")
