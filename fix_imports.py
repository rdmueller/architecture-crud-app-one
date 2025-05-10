#!/usr/bin/env python
"""Fix imports in all Python files to use absolute imports based on src package."""
import os
import re
from pathlib import Path


def fix_imports_in_file(file_path: Path):
    """Fix imports in a single file."""
    print(f"Processing {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Patterns to replace
    replacements = [
        # Routes files
        (r'from \.\.\.data\.repository', 'from src.data.repository'),
        (r'from \.\.models\.', 'from src.api.models.'),
        (r'from \.\.dependencies', 'from src.api.dependencies'),
        
        # Models files
        (r'from \.\.\.data\.models', 'from src.data.models'),
        
        # Dependencies file
        (r'from \.\.data\.repository', 'from src.data.repository'),
        
        # API files that import from routes
        (r'from api\.dependencies', 'from src.api.dependencies'),
        (r'from api\.models', 'from src.api.models'),
        (r'from data\.repository', 'from src.data.repository'),
        (r'from data\.models', 'from src.data.models'),
        (r'from generator\.generator', 'from src.generator.generator'),
    ]
    
    modified = False
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            modified = True
    
    if modified:
        print(f"  Fixed imports in {file_path}")
        with open(file_path, 'w') as f:
            f.write(content)
    else:
        print(f"  No changes needed in {file_path}")


def main():
    """Main function to fix all imports."""
    base_path = Path(__file__).parent
    src_path = base_path / "src"
    
    # Files to fix
    files_to_fix = [
        # API routes
        src_path / "api" / "routes" / "adrs.py",
        src_path / "api" / "routes" / "qualities.py",
        src_path / "api" / "routes" / "risks.py",
        src_path / "api" / "routes" / "technical_debts.py",
        src_path / "api" / "routes" / "components.py",
        src_path / "api" / "routes" / "architecture.py",
        src_path / "api" / "routes" / "export.py",
        
        # Dependencies
        src_path / "api" / "dependencies.py",
        
        # Models
        src_path / "api" / "models" / "__init__.py",
    ]
    
    for file_path in files_to_fix:
        if file_path.exists():
            fix_imports_in_file(file_path)
        else:
            print(f"Warning: {file_path} not found")
    
    print("\nImport fixing complete!")
    print("\nYou can now run the API with:")
    print("python run_api.py")


if __name__ == "__main__":
    main()
