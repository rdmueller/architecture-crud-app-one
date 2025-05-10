"""Tests for the Qualities page."""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


@patch('streamlit.header')
@patch('streamlit.tabs')
def test_qualities_page_renders_header_and_tabs(mock_tabs, mock_header):
    """Test that Qualities page renders header and tabs."""
    from ui.pages.qualities import render_qualities
    
    # Mock tabs return value
    mock_tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
    
    render_qualities()
    
    # Check header was called
    mock_header.assert_called_with("Quality Requirements")
    
    # Check tabs were created
    mock_tabs.assert_called_with(["List Qualities", "Create Quality", "Edit Quality"])


@patch('requests.get')
@patch('streamlit.dataframe')
@patch('streamlit.tabs')
def test_qualities_list_displays_dataframe(mock_tabs, mock_dataframe, mock_get):
    """Test that Qualities list tab displays dataframe."""
    from ui.pages.qualities import render_qualities
    
    # Mock tabs to select list tab
    list_tab = MagicMock()
    create_tab = MagicMock()
    edit_tab = MagicMock()
    mock_tabs.return_value = [list_tab, create_tab, edit_tab]
    
    # Mock API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": "QA-001",
            "title": "Performance",
            "description": "High performance requirements",
            "priority": "must"
        }
    ]
    mock_get.return_value = mock_response
    
    # Mock context manager
    list_tab.__enter__ = MagicMock(return_value=list_tab)
    list_tab.__exit__ = MagicMock(return_value=None)
    
    render_qualities()
    
    # Check that dataframe was called
    assert mock_dataframe.called


@patch('streamlit.form_submit_button')
@patch('streamlit.text_input')
@patch('streamlit.text_area')
@patch('streamlit.selectbox')
@patch('streamlit.form')
@patch('streamlit.tabs')
def test_qualities_create_form(mock_tabs, mock_form, mock_selectbox, 
                             mock_text_area, mock_text_input, mock_submit):
    """Test that create Quality form is displayed."""
    from ui.pages.qualities import render_qualities
    
    # Mock tabs to select create tab
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
    
    render_qualities()
    
    # Check that form was created
    mock_form.assert_called_with("create_quality_form")
    
    # Check that form fields were created
    assert mock_text_input.called
    assert mock_text_area.called
    assert mock_selectbox.called
    assert mock_submit.called


@patch('requests.get')
@patch('streamlit.error')
@patch('streamlit.tabs')
def test_qualities_handles_api_error(mock_tabs, mock_error, mock_get):
    """Test that Qualities page handles API errors gracefully."""
    from ui.pages.qualities import render_qualities
    
    # Mock tabs
    mock_tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
    
    # Mock API error
    mock_get.side_effect = Exception("API Error")
    
    render_qualities()
    
    # Check that error was displayed
    assert mock_error.called
