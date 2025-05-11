"""Test fixtures for API tests."""
import pytest
from unittest.mock import MagicMock
from pathlib import Path
import sys

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import after path setup
from src.api.dependencies import get_repository


@pytest.fixture
def mock_repo():
    """Mock repository for testing."""
    mock = MagicMock()
    # Override the get_repository dependency
    get_repository.dependency = lambda: mock
    return mock


@pytest.fixture
def mock_validator():
    """Mock validator for testing."""
    mock = MagicMock()
    return mock


@pytest.fixture
def mock_repo():
    """Mock repository for testing."""
    mock = MagicMock()
    # Override the get_repository dependency
    get_repository.dependency = lambda: mock
    return mock


@pytest.fixture
def mock_validator():
    """Mock validator for testing."""
    mock = MagicMock()
    # Override the get_validator dependency
    get_validator.dependency = lambda: mock
    return mock
