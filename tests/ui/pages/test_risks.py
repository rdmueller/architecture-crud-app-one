"""Tests for the Risks page."""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


@patch('streamlit.header')
@patch('streamlit.tabs')
def test_risks_page_renders_header_and_tabs(mock_tabs, mock_header):
    """Test that Risks page renders header and tabs."""
    from ui.pages.risks import render_risks
    
    # Mock tabs return value
    mock_tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
    
    render_risks()
    
    # Check header was called
    mock_header.assert_called_with("Risks")
    
    # Check tabs were created
    mock_tabs.assert_called_with(["List Risks", "Create Risk", "Edit Risk"])
