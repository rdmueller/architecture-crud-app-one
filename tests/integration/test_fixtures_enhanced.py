"""Enhanced fixtures for integration tests."""
import pytest
import subprocess
import time
import requests
import shutil
import tempfile
import os
import sys
from datetime import datetime
import json
import uvicorn
from multiprocessing import Process


# Ports for test instances
TEST_API_PORT = 8092
TEST_UI_PORT = 8511


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary data directory for tests."""
    temp_dir = tempfile.mkdtemp()
    
    # Copy necessary project files to temp directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    # Copy src directory
    src_dir = os.path.join(project_root, "src")
    temp_src_dir = os.path.join(temp_dir, "src")
    if os.path.exists(src_dir):
        shutil.copytree(src_dir, temp_src_dir)
    
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


@pytest.fixture(scope="session", params=["real", "mock"])
def api_server(request, test_data_dir):
    """Start either real or mock API server for testing."""
    if request.param == "mock":
        # Use mock API
        from .mock_api import app
        
        def run_mock_server():
            uvicorn.run(app, host="0.0.0.0", port=TEST_API_PORT)
        
        server_process = Process(target=run_mock_server)
        server_process.start()
        
        # Wait for mock server to be ready
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                response = requests.get(f"http://localhost:{TEST_API_PORT}/health")
                if response.status_code == 200:
                    break
            except requests.ConnectionError:
                pass
            time.sleep(0.5)
        else:
            server_process.terminate()
            raise RuntimeError("Mock API server failed to start")
        
        yield f"http://localhost:{TEST_API_PORT}"
        
        # Cleanup
        server_process.terminate()
        server_process.join()
    
    else:
        # Use real API
        env = os.environ.copy()
        env["ARCHITECTURE_DATA_PATH"] = os.path.join(test_data_dir, "data", "architecture.json")
        
        # Create test API script
        test_api_script = os.path.join(test_data_dir, "test_api.py")
        with open(test_api_script, "w") as f:
            f.write(f"""
import os
import sys
sys.path.insert(0, r'{test_data_dir}')

from src.api.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port={TEST_API_PORT})
""")
        
        api_process = subprocess.Popen(
            [sys.executable, test_api_script],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=test_data_dir
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
def ui_server_real(test_data_dir, api_server):
    """Start the real UI server for testing."""
    if "mock" in str(api_server):
        pytest.skip("UI server only tested with real API")
    
    env = os.environ.copy()
    env["API_BASE_URL"] = api_server
    
    # Create test UI script
    test_ui_script = os.path.join(test_data_dir, "test_ui.py")
    with open(test_ui_script, "w") as f:
        f.write(f"""
import os
import sys
sys.path.insert(0, r'{test_data_dir}')

import streamlit.web.cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", os.path.join(r'{test_data_dir}', "src", "ui", "app.py"), 
                "--server.port={TEST_UI_PORT}", 
                "--server.headless=true"]
    stcli.main()
""")
    
    ui_process = subprocess.Popen(
        [sys.executable, test_ui_script],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=test_data_dir
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
def ui_server(request, api_server):
    """Provide UI server URL if testing with real API, skip if mock."""
    if hasattr(request, 'param_index') and "mock" in request.param_index[request.fixturenames.index("api_server")]:
        pytest.skip("UI tests skipped for mock API")
    else:
        return request.getfixturevalue("ui_server_real")


@pytest.fixture
def clean_storage(api_server):
    """Clean storage before each test."""
    # Clear all data
    for entity_type in ["adrs", "qualities", "risks", "technical-debts", "components"]:
        response = requests.get(f"{api_server}/api/{entity_type}")
        if response.status_code == 200:
            entities = response.json()
            for entity in entities:
                entity_id = entity.get("id")
                if entity_id:
                    requests.delete(f"{api_server}/api/{entity_type}/{entity_id}")
    
    yield
    
    # Clean up after test
    for entity_type in ["adrs", "qualities", "risks", "technical-debts", "components"]:
        response = requests.get(f"{api_server}/api/{entity_type}")
        if response.status_code == 200:
            entities = response.json()
            for entity in entities:
                entity_id = entity.get("id")
                if entity_id:
                    requests.delete(f"{api_server}/api/{entity_type}/{entity_id}")


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
