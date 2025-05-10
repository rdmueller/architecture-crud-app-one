"""Tests for the Components page."""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


@patch('streamlit.header')
@patch('streamlit.tabs')
def test_components_page_renders_header_and_tabs(mock_tabs, mock_header):
    """Test that Components page renders header and tabs."""
    from ui.pages.components import render_components
    
    # Mock tabs return value
    mock_tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
    
    render_components()
    
    # Check header was called
    mock_header.assert_called_with("Components")
    
    # Check tabs were created
    mock_tabs.assert_called_with(["List Components", "Create Component", "Edit Component"])
