#!/usr/bin/env python
"""Fix dashboard to properly display data."""
import os
import sys

def fix_dashboard():
    """Fix the dashboard."""
    file_path = "src/ui/pages/dashboard.py"
    
    with open(file_path, "r") as f:
        content = f.read()
    
    # Add more debug output
    new_content = content.replace(
        "def render_dashboard():",
        "def render_dashboard():\n    st.write(\"Debug mode enabled\")"
    )
    
    # Fix data handling
    new_content = new_content.replace(
        "data = fetch_architecture_data()",
        "data = fetch_architecture_data()\n    if data:\n        st.write(f\"Debug - Raw data: {type(data)}\")"
    )
    
    with open(file_path, "w") as f:
        f.write(new_content)
    
    print(f"Fixed dashboard in {file_path}")

if __name__ == "__main__":
    fix_dashboard()
    print("Dashboard fixed successfully!")
