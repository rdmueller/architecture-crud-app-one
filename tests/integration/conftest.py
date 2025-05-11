"""Configuration for integration tests."""
import pytest
import os


def pytest_configure(config):
    """Configure pytest for integration tests."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "selenium: mark test as requiring Selenium"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on environment."""
    # Skip Selenium tests unless explicitly requested
    if os.environ.get("RUN_SELENIUM_TESTS") != "1":
        skip_selenium = pytest.mark.skip(reason="Selenium tests not enabled")
        for item in items:
            if "selenium" in item.keywords:
                item.add_marker(skip_selenium)


# Import simple fixtures by default
from .test_fixtures_simple import *
