#!/usr/bin/env python
"""Run the Streamlit UI with initialized data."""
import os
import subprocess
import sys

# Initialize data first
print("Initializing data...")
subprocess.run([sys.executable, "initialize_data.py"])

# Run the Streamlit app
print("\nStarting Streamlit UI...")
subprocess.run(["streamlit", "run", "src/ui/app.py"])
