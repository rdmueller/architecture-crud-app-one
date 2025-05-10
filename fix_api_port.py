#!/usr/bin/env python
"""Fix API port references from 8000 to 8082 in all files."""
import os
import re
from pathlib import Path


def fix_port_in_file(file_path: Path):
    """Fix port references in a single file."""
    print(f"Processing {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace port 8000 with 8082
    new_content = content.replace("http://localhost:8000", "http://localhost:8082")
    
    if new_content != content:
        print(f"  Fixed port references in {file_path}")
        with open(file_path, 'w') as f:
            f.write(new_content)
    else:
        print(f"  No changes needed in {file_path}")


def find_files_with_port_reference(directory: Path):
    """Find all Python files that might contain port references."""
    files_to_check = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                files_to_check.append(file_path)
    
    return files_to_check


def main():
    """Main function to fix all port references."""
    base_path = Path(__file__).parent
    src_path = base_path / "src"
    
    # Find all Python files in the src directory
    files_to_check = find_files_with_port_reference(src_path)
    
    # Check and fix each file
    for file_path in files_to_check:
        fix_port_in_file(file_path)
    
    print("\nPort fixing complete!")
    print("\nYour API is running on port 8082")
    print("Your UI should now connect to the correct port")


if __name__ == "__main__":
    main()
