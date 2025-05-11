#!/usr/bin/env python
"""Run integration tests for Architecture CRUD Application."""
import sys
import os
import subprocess
import pytest
import time
import shutil
import tempfile
import json


def setup_test_environment():
    """Set up a clean test environment."""
    print("Setting up test environment...")
    
    # Create temporary directory for test data
    temp_dir = tempfile.mkdtemp(prefix="arch_crud_test_")
    data_dir = os.path.join(temp_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Create empty architecture file
    arch_file = os.path.join(data_dir, "architecture.json")
    with open(arch_file, "w") as f:
        json.dump({
            "adrs": {},
            "qualities": {},
            "risks": {},
            "technicalDebts": {},
            "components": {}
        }, f, indent=2)
    
    # Set environment variable for test data path
    os.environ["ARCHITECTURE_DATA_PATH"] = arch_file
    
    return temp_dir


def cleanup_test_environment(temp_dir):
    """Clean up test environment."""
    print("Cleaning up test environment...")
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Warning: Could not remove temp directory: {e}")


def run_integration_tests():
    """Run all integration tests."""
    print("=" * 60)
    print("Running Integration Tests")
    print("=" * 60)
    
    temp_dir = None
    try:
        # Set up test environment
        temp_dir = setup_test_environment()
        print(f"Test data directory: {temp_dir}")
        
        # Run pytest with integration tests
        print("\nRunning integration tests...")
        result = pytest.main([
            "tests/integration",
            "-v",
            "--tb=short",
            "--durations=5",
            "-m", "not skip",  # Skip Selenium tests by default
            "--color=yes"
        ])
        
        print("\n" + "=" * 60)
        if result == 0:
            print("✅ All integration tests passed!")
        else:
            print("❌ Some integration tests failed")
        print("=" * 60)
        
        return result
        
    finally:
        if temp_dir:
            cleanup_test_environment(temp_dir)


def run_simple_integration_check():
    """Run a simple integration check without full test setup."""
    print("=" * 60)
    print("Simple Integration Check")
    print("=" * 60)
    
    # Start API server
    print("Starting API server...")
    api_process = subprocess.Popen(
        [sys.executable, "run_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Start UI server
    print("Starting UI server...")
    ui_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "src/ui/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for services to start
        time.sleep(5)
        
        # Simple health check
        import requests
        
        print("\nChecking API health...")
        try:
            response = requests.get("http://localhost:8082/health")
            if response.status_code == 200:
                print("✅ API is healthy")
            else:
                print(f"❌ API health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ API not accessible: {e}")
        
        print("\nChecking UI accessibility...")
        try:
            response = requests.get("http://localhost:8501")
            if response.status_code == 200:
                print("✅ UI is accessible")
            else:
                print(f"❌ UI check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ UI not accessible: {e}")
        
    finally:
        # Clean up
        print("\nStopping services...")
        api_process.terminate()
        ui_process.terminate()
        api_process.wait()
        ui_process.wait()
        print("Services stopped")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run integration tests")
    parser.add_argument("--simple", action="store_true", 
                      help="Run simple integration check without full test suite")
    parser.add_argument("--selenium", action="store_true",
                      help="Include Selenium tests (requires Chrome)")
    
    args = parser.parse_args()
    
    if args.simple:
        run_simple_integration_check()
        return 0
    
    # Check for required packages
    required_packages = ["pytest", "requests"]
    if args.selenium:
        required_packages.extend(["selenium", "webdriver-manager"])
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return 1
    
    # Run full integration tests
    if args.selenium:
        # Remove the skip marker for Selenium tests
        os.environ["RUN_SELENIUM_TESTS"] = "1"
    
    return run_integration_tests()


if __name__ == "__main__":
    sys.exit(main())
