#!/usr/bin/env python
"""Fix issues in frontend files - placeholders and field names."""
from pathlib import Path
import re

def fix_file_content(file_path: Path):
    """Fix issues in a single file."""
    print(f"Processing {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    modified = False
    
    # Fix placeholders and field names based on file
    if file_path.name == "adrs.py":
        # Fix alternatives structure
        new_content = content.replace(
            'alternatives[alt_key] = {"pros": pros.split("\\n"), "cons": cons.split("\\n")}',
            'alternatives[alt_key] = {"advantages": pros.split("\\n") if pros else [], "disadvantages": cons.split("\\n") if cons else []}'
        )
        
        # Better label names
        new_content = new_content.replace(
            'pros = st.text_area(f"Pros", key=f"alt_pros_{i}")',
            'advantages = st.text_area(f"Advantages", key=f"alt_advantages_{i}", placeholder="List advantages, one per line")'
        )
        new_content = new_content.replace(
            'cons = st.text_area(f"Cons", key=f"alt_cons_{i}")',
            'disadvantages = st.text_area(f"Disadvantages", key=f"alt_disadvantages_{i}", placeholder="List disadvantages, one per line")'
        )
        
        # Fix placeholder
        new_content = new_content.replace(
            'placeholder="Use microservices architecture"',
            'placeholder="Choose technology X for component Y"'
        )
        modified = new_content != content
        content = new_content
    
    elif file_path.name == "qualities.py":
        # Fix placeholder for quality ID
        new_content = content.replace(
            'placeholder="Q-001"',
            'placeholder="QA-001"'
        )
        new_content = new_content.replace(
            'help="Format: Q-XXX where XXX is a 3-digit number"',
            'help="Format: QA-XXX where XXX is a 3-digit number"'
        )
        modified = new_content != content
        content = new_content
        
    elif file_path.name == "risks.py":
        # Fix placeholder for risk ID
        new_content = content.replace(
            'placeholder="R-001"',
            'placeholder="RISK-001"'
        )
        new_content = new_content.replace(
            'help="Format: R-XXX where XXX is a 3-digit number"',
            'help="Format: RISK-XXX where XXX is a 3-digit number"'
        )
        modified = new_content != content
        content = new_content
    
    elif file_path.name == "technical_debts.py":
        # Fix placeholder for technical debt ID
        new_content = content.replace(
            'placeholder="TD-001"',
            'placeholder="TD-001"'  # This one is actually correct
        )
        modified = new_content != content
        content = new_content
        
    elif file_path.name == "components.py":
        # Fix placeholder for component ID
        new_content = content.replace(
            'placeholder="C-001"',
            'placeholder="COMP-001"'
        )
        new_content = new_content.replace(
            'help="Format: C-XXX where XXX is a 3-digit number"',
            'help="Format: COMP-XXX where XXX is a 3-digit number"'
        )
        modified = new_content != content
        content = new_content
    
    if modified:
        print(f"  Fixed issues in {file_path}")
        with open(file_path, 'w') as f:
            f.write(content)
    else:
        print(f"  No changes needed in {file_path}")


def main():
    """Main function to fix all issues."""
    base_path = Path(__file__).parent
    pages_path = base_path / "src" / "ui" / "pages"
    
    # Files to fix
    files_to_fix = [
        pages_path / "adrs.py",
        pages_path / "qualities.py",
        pages_path / "risks.py",
        pages_path / "technical_debts.py",
        pages_path / "components.py"
    ]
    
    for file_path in files_to_fix:
        if file_path.exists():
            fix_file_content(file_path)
        else:
            print(f"Warning: {file_path} not found")
    
    print("\nFrontend fixing complete!")


if __name__ == "__main__":
    main()
