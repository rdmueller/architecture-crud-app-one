"""Initialize the application with example data."""
import shutil
import os
import sys
import json

# Add src to path
sys.path.insert(0, 'src')

def initialize_example_data():
    """Copy example data to the working data file if it doesn't exist or is empty."""
    data_dir = "data"
    working_file = os.path.join(data_dir, "architecture.json")
    example_file = os.path.join(data_dir, "example_architecture.json")
    
    # Check if working file exists and has content
    if os.path.exists(working_file):
        with open(working_file, 'r') as f:
            content = f.read().strip()
            if content:
                try:
                    data = json.loads(content)
                    # Check if the file has actual content (not just empty structures)
                    if (data.get("adrs") and len(data.get("adrs")) > 0 and
                        data.get("qualities") and len(data.get("qualities")) > 0):
                        print(f"Working data file already exists and has content: {working_file}")
                        return
                    else:
                        print(f"Working data file exists but has no entities. Initializing with example data.")
                except json.JSONDecodeError:
                    print(f"Working data file exists but is not valid JSON. Initializing with example data.")
    
    # Copy example data
    if os.path.exists(example_file):
        shutil.copy2(example_file, working_file)
        print(f"Initialized data from {example_file} to {working_file}")
    else:
        print(f"Example file not found: {example_file}")
        
        # Try to find the arc42 architecture file as alternative
        arc42_file = os.path.join("docs", "arc42", "architecture.json")
        if os.path.exists(arc42_file):
            shutil.copy2(arc42_file, working_file)
            print(f"Initialized data from {arc42_file} to {working_file}")
        else:
            print("No example data found!")

if __name__ == "__main__":
    initialize_example_data()
