#!/usr/bin/env python
"""Use fixed data for the application."""
import os
import sys
import json
import shutil
from datetime import datetime

def use_fixed_data():
    """Use fixed data for the application."""
    data_dir = "data"
    fixed_file = os.path.join(data_dir, "fixed_architecture.json")
    working_file = os.path.join(data_dir, "architecture.json")
    
    # Backup existing working file if it exists
    if os.path.exists(working_file):
        backup_file = os.path.join(data_dir, f"architecture_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        shutil.copy2(working_file, backup_file)
        print(f"Backed up existing working data to {backup_file}")
    
    # Copy fixed data to working file
    shutil.copy2(fixed_file, working_file)
    print(f"Copied fixed data from {fixed_file} to {working_file}")
    
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

if __name__ == "__main__":
    if use_fixed_data():
        print("\nFixed data is now being used!")
        print("Please restart the application.")
    else:
        print("\nFailed to use fixed data.")
