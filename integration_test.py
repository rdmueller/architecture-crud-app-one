#!/usr/bin/env python
"""Integration test for Architecture CRUD application."""
import requests
import time
import sys
import subprocess
import os
import signal


def wait_for_service(url, timeout=30):
    """Wait for a service to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    return False


def test_api():
    """Test API endpoints."""
    print("Testing API endpoints...")
    
    # Test health endpoint
    response = requests.get("http://localhost:8082/health")
    assert response.status_code == 200
    print("✓ Health endpoint works")
    
    # Test architecture endpoint
    response = requests.get("http://localhost:8082/api/architecture")
    assert response.status_code == 200
    print("✓ Architecture endpoint works")
    
    # Test creating an ADR
    adr_data = {
        "id": "ADR-001",
        "title": "Test ADR",
        "status": "proposed",
        "date": "2024-01-01",
        "authors": ["Test Author"],
        "context": "Test context",
        "decision": "Test decision",
        "alternatives": {},
        "relationships": {
            "qualities": [],
            "risks": [],
            "technicalDebts": [],
            "components": [],
            "relatedAdrs": []
        }
    }
    
    response = requests.post("http://localhost:8082/api/adrs", json=adr_data)
    assert response.status_code == 201
    print("✓ ADR creation works")
    
    # Test getting the created ADR
    response = requests.get("http://localhost:8082/api/adrs/ADR-001")
    assert response.status_code == 200
    assert response.json()["title"] == "Test ADR"
    print("✓ ADR retrieval works")
    
    return True


def test_ui():
    """Test UI availability."""
    print("Testing UI availability...")
    
    response = requests.get("http://localhost:8501")
    assert response.status_code == 200
    print("✓ UI is accessible")
    
    return True


def main():
    """Main test function."""
    print("Starting integration tests...")
    
    # Start API
    print("Starting API...")
    api_process = subprocess.Popen(
        ["python", "run_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Start UI
    print("Starting UI...")
    ui_process = subprocess.Popen(
        ["streamlit", "run", "src/ui/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for services to be ready
        print("Waiting for services to be ready...")
        if not wait_for_service("http://localhost:8082/health"):
            print("ERROR: API failed to start")
            return 1
        
        if not wait_for_service("http://localhost:8501"):
            print("ERROR: UI failed to start")
            return 1
        
        # Run tests
        api_success = test_api()
        ui_success = test_ui()
        
        if api_success and ui_success:
            print("\n✓ All tests passed!")
            return 0
        else:
            print("\n✗ Some tests failed")
            return 1
            
    finally:
        # Cleanup
        print("\nCleaning up...")
        api_process.terminate()
        ui_process.terminate()
        api_process.wait()
        ui_process.wait()


if __name__ == "__main__":
    sys.exit(main())
