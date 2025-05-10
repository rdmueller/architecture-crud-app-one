#!/usr/bin/env python
"""Run UI tests without HTML coverage report."""
import sys
import pytest
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def main():
    """Run all UI tests."""
    print("Running UI tests...")
    
    # Test configurations
    test_args = [
        "tests/ui",  # Test directory
        "-v",  # Verbose output
        "--cov=src/ui",  # Coverage for UI code
        "--cov-report=term-missing",  # Terminal coverage report only
    ]
    
    # Run tests
    exit_code = pytest.main(test_args)
    
    if exit_code == 0:
        print("\n✅ All UI tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
