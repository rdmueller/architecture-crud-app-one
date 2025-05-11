"""Fixtures for integration tests."""
import pytest
import subprocess
import time
import requests
import shutil
import tempfile
import os
import sys  # Added missing import
from datetime import datetime
import json


# Ports for test instances
TEST_API_PORT = 8092
TEST_UI_PORT = 8511


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary data directory for tests."""
    temp_dir = tempfile.mkdtemp()
    
    # Copy schema file to temp directory
    src_schema = os.path.join("src", "json", "architecture-schema.json")
    if os.path.exists(src_schema):
        os.makedirs(os.path.join(temp_dir, "src", "json"), exist_ok=True)
        shutil.copy(src_schema, os.path.join(temp_dir, "src", "json", "architecture-schema.json"))
    
    # Create empty data directory
    data_dir = os.path.join(temp_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Create initial empty architecture file
    architecture_file = os.path.join(data_dir, "architecture.json")
    with open(architecture_file, "w") as f:
        json.dump({
            "adrs": {},
            "qualities": {},
            "risks": {},
            "technicalDebts": {},
            "components": {}
        }, f)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def api_server(test_data_dir):
    """Start the API server for testing."""
    env = os.environ.copy()
    env["ARCHITECTURE_DATA_PATH"] = os.path.join(test_data_dir, "data", "architecture.json")
    
    # Create test API script
    test_api_script = os.path.join(test_data_dir, "test_api.py")
    with open(test_api_script, "w") as f:
        f.write(f"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from src.api.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port={TEST_API_PORT})
""")
    
    api_process = subprocess.Popen(
        [sys.executable, test_api_script],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for API to be ready
    start_time = time.time()
    while time.time() - start_time < 30:
        try:
            response = requests.get(f"http://localhost:{TEST_API_PORT}/health")
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass
        time.sleep(0.5)
    else:
        api_process.terminate()
        raise RuntimeError("API server failed to start")
    
    yield f"http://localhost:{TEST_API_PORT}"
    
    # Cleanup
    api_process.terminate()
    api_process.wait()


@pytest.fixture(scope="session")
def ui_server(test_data_dir, api_server):
    """Start the UI server for testing."""
    env = os.environ.copy()
    env["API_BASE_URL"] = api_server
    
    # Create test UI script
    test_ui_script = os.path.join(test_data_dir, "test_ui.py")
    with open(test_ui_script, "w") as f:
        f.write(f"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", os.path.join("src", "ui", "app.py"), 
                "--server.port={TEST_UI_PORT}", 
                "--server.headless=true"]
    stcli.main()
""")
    
    ui_process = subprocess.Popen(
        [sys.executable, test_ui_script],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for UI to be ready
    start_time = time.time()
    while time.time() - start_time < 30:
        try:
            response = requests.get(f"http://localhost:{TEST_UI_PORT}")
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass
        time.sleep(0.5)
    else:
        ui_process.terminate()
        raise RuntimeError("UI server failed to start")
    
    yield f"http://localhost:{TEST_UI_PORT}"
    
    # Cleanup
    ui_process.terminate()
    ui_process.wait()


@pytest.fixture
def sample_adr():
    """Create a sample ADR for testing."""
    return {
        "id": "ADR-001",
        "title": "Use FastAPI for Backend",
        "status": "accepted",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "authors": ["Test Author"],
        "context": "We need to choose a backend framework.",
        "decision": "We decided to use FastAPI for its performance and type safety.",
        "alternatives": {
            "Django": {
                "pros": ["Mature framework", "Built-in admin"],
                "cons": ["Slower", "More complex"]
            },
            "Flask": {
                "pros": ["Simple", "Flexible"],
                "cons": ["Less features", "No async by default"]
            }
        },
        "relationships": {
            "qualities": [],
            "risks": [],
            "technicalDebts": [],
            "components": [],
            "relatedAdrs": []
        }
    }


@pytest.fixture
def sample_quality():
    """Create a sample quality for testing."""
    return {
        "id": "Q-001",
        "title": "Performance",
        "description": "The system must respond quickly to user requests.",
        "priority": "high",
        "metrics": [
            {
                "name": "Response Time",
                "target": "< 200ms",
                "current": "150ms"
            }
        ]
    }


@pytest.fixture
def sample_risk():
    """Create a sample risk for testing."""
    return {
        "id": "R-001",
        "title": "Database Downtime",
        "description": "The database might become unavailable.",
        "impact": "high",
        "probability": "low",
        "mitigation": "Implement caching and retry logic.",
        "status": "identified"
    }


@pytest.fixture
def sample_technical_debt():
    """Create a sample technical debt for testing."""
    return {
        "id": "TD-001",
        "title": "No Automated Testing",
        "description": "The system lacks automated tests.",
        "impact": "medium",
        "effort": "high",
        "resolution": "Implement comprehensive test suite.",
        "status": "planned"
    }


@pytest.fixture
def sample_component():
    """Create a sample component for testing."""
    return {
        "id": "C-001",
        "title": "API Service",
        "responsibility": "Handle all API requests and business logic.",
        "interfaces": [
            {
                "name": "REST API",
                "description": "RESTful API endpoints",
                "protocol": "HTTP"
            }
        ],
        "attributes": {
            "language": "Python",
            "framework": "FastAPI"
        }
    }
