#!/usr/bin/env python
"""Run all UI tests with coverage reporting."""
import sys
import pytest
import os
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def main():
    """Run all UI tests with coverage."""
    print("Running UI tests with coverage...")
    
    # Test configurations
    test_args = [
        "tests/ui",  # Test directory
        "-v",  # Verbose output
        "--cov=src/ui",  # Coverage for UI code
        "--cov-report=html:htmlcov/ui",  # HTML coverage report
        "--cov-report=term-missing",  # Terminal coverage report
        "--cov-fail-under=80",  # Fail if coverage is below 80%
    ]
    
    # Run tests
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print("\n✅ All UI tests passed!")
        print("📊 Coverage report generated in htmlcov/ui/index.html")
    else:
        print("\n❌ Some tests failed!")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
