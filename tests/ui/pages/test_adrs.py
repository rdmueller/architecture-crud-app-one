"""Simple tests for the ADRs page."""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
from pathlib import Path
from datetime import date

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


@patch('streamlit.tabs')
def test_adrs_page_renders_header_and_tabs(mock_tabs):
    """Test that ADRs page renders tabs."""
    from ui.pages.adrs import render_adrs
    
    # Mock tabs
    tab1, tab2, tab3 = MagicMock(), MagicMock(), MagicMock()
    mock_tabs.return_value = [tab1, tab2, tab3]
    
    # Mock tab contexts
    tab1.__enter__ = MagicMock(return_value=tab1)
    tab1.__exit__ = MagicMock(return_value=None)
    
    # Mock empty ADR response
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        render_adrs()
    
    # Check tabs were created
    mock_tabs.assert_called_with(["List ADRs", "Create ADR", "Edit ADR"])


@patch('streamlit.dataframe')
@patch('streamlit.tabs')
def test_adrs_list_displays_dataframe(mock_tabs, mock_dataframe):
    """Test that ADR list displays dataframe."""
    from ui.pages.adrs import render_adrs
    
    # Mock tabs
    tab1, tab2, tab3 = MagicMock(), MagicMock(), MagicMock()
    mock_tabs.return_value = [tab1, tab2, tab3]
    
    # Mock tab contexts
    tab1.__enter__ = MagicMock(return_value=tab1)
    tab1.__exit__ = MagicMock(return_value=None)
    
    # Mock ADR response
    mock_adrs = [
        {
            "id": "ADR-001",
            "title": "Test ADR",
            "status": "accepted",
            "date": "2025-05-10",
            "authors": ["John Doe"]
        }
    ]
    
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_adrs
        mock_get.return_value = mock_response
        
        render_adrs()
    
    # Check dataframe was called
    assert mock_dataframe.called


@patch('streamlit.tabs')
@patch('streamlit.form')
def test_adrs_create_form(mock_form, mock_tabs):
    """Test that create ADR form is displayed."""
    from ui.pages.adrs import render_adrs
    
    # Mock tabs
    list_tab = MagicMock()
    create_tab = MagicMock()
    edit_tab = MagicMock()
    mock_tabs.return_value = [list_tab, create_tab, edit_tab]
    
    # Mock form
    form_context = MagicMock()
    mock_form.return_value = form_context
    form_context.__enter__ = MagicMock(return_value=form_context)
    form_context.__exit__ = MagicMock(return_value=None)
    
    # Mock tab context
    create_tab.__enter__ = MagicMock(return_value=create_tab)
    create_tab.__exit__ = MagicMock(return_value=None)
    
    render_adrs()
    
    # Check that form was created
    assert mock_form.called


@patch('requests.post')
def test_adrs_create_submits_data(mock_post):
    """Test that ADR creation submits data with direct API call."""
    from ui.pages.adrs import create_adr
    
    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response
    
    # Create test ADR data
    adr_data = {
        "id": "ADR-001",
        "title": "Test ADR",
        "status": "proposed",
        "date": "2025-05-10",
        "authors": ["John Doe"],
        "context": "Test context",
        "decision": "Test decision",
        "alternatives": {},
        "relationships": {}
    }
    
    # Call create function directly
    success = create_adr(adr_data)
    
    # Check post was called
    mock_post.assert_called_once()
    assert success


@patch('requests.get')
@patch('streamlit.error')
def test_adrs_handles_api_error(mock_error, mock_get):
    """Test that ADRs page handles API errors gracefully."""
    from ui.pages.adrs import render_adrs
    
    # Mock API error
    mock_get.side_effect = Exception("Connection refused")
    
    render_adrs()
    
    # Check error was displayed
    mock_error.assert_called()
