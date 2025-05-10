"""Tests for the main Streamlit app."""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_app_imports():
    """Test that the app module can be imported."""
    from ui.app import main
    assert main is not None


@patch('streamlit.selectbox')
@patch('streamlit.sidebar.title')
@patch('streamlit.title')
def test_app_main_renders_title(mock_title, mock_sidebar_title, mock_selectbox):
    """Test that main app renders title."""
    from ui.app import main
    
    # Mock selectbox to return a page
    mock_selectbox.return_value = "Dashboard"
    
    # Call main function
    with patch('ui.pages.dashboard.render_dashboard') as mock_render:
        main()
    
    # Check that title was rendered
    mock_title.assert_called_with("Architecture CRUD Application")
    mock_sidebar_title.assert_called_with("Navigation")


@patch('streamlit.sidebar.selectbox')
@patch('streamlit.sidebar.title')
@patch('streamlit.title')
def test_navigation_menu(mock_title, mock_sidebar_title, mock_selectbox):
    """Test that navigation menu is created."""
    from ui.app import main
    
    # Mock selectbox to return a page
    mock_selectbox.return_value = "Dashboard"
    
    # Call main function
    with patch('ui.pages.dashboard.render_dashboard') as mock_render:
        main()
    
    # Check that selectbox was called with correct options
    mock_selectbox.assert_called_with(
        "Navigation",
        ["Dashboard", "ADRs", "Qualities", "Risks", "Technical Debts", "Components", "Relationships", "Export"],
        key="navigation"
    )


@patch('streamlit.sidebar.selectbox')
@patch('streamlit.sidebar.title')
@patch('streamlit.title')
def test_dashboard_page_rendering(mock_title, mock_sidebar_title, mock_selectbox):
    """Test that Dashboard page is rendered when selected."""
    from ui.app import main
    
    # Mock selectbox to return Dashboard
    mock_selectbox.return_value = "Dashboard"
    
    # Mock the dashboard render function
    with patch('ui.pages.dashboard.render_dashboard') as mock_render:
        main()
        mock_render.assert_called_once()


@patch('streamlit.sidebar.selectbox')
@patch('streamlit.sidebar.title')
@patch('streamlit.title')
def test_adrs_page_rendering(mock_title, mock_sidebar_title, mock_selectbox):
    """Test that ADRs page is rendered when selected."""
    from ui.app import main
    
    # Mock selectbox to return ADRs
    mock_selectbox.return_value = "ADRs"
    
    # Mock the ADRs render function
    with patch('ui.pages.adrs.render_adrs') as mock_render:
        main()
        mock_render.assert_called_once()


@patch('streamlit.sidebar.selectbox')
@patch('streamlit.sidebar.title')
@patch('streamlit.title')
def test_relationships_page_rendering(mock_title, mock_sidebar_title, mock_selectbox):
    """Test that Relationships page is rendered when selected."""
    from ui.app import main
    
    # Mock selectbox to return Relationships
    mock_selectbox.return_value = "Relationships"
    
    # Mock the Relationships render function
    with patch('ui.pages.relationships.render_relationships') as mock_render:
        main()
        mock_render.assert_called_once()


@patch('streamlit.sidebar.selectbox')
@patch('streamlit.sidebar.title')
@patch('streamlit.title')
def test_export_page_rendering(mock_title, mock_sidebar_title, mock_selectbox):
    """Test that Export page is rendered when selected."""
    from ui.app import main
    
    # Mock selectbox to return Export
    mock_selectbox.return_value = "Export"
    
    # Mock the Export render function
    with patch('ui.pages.export.render_export') as mock_render:
        main()
        mock_render.assert_called_once()


@patch('requests.get')
@patch('streamlit.error')
def test_api_connection_error_handling(mock_error, mock_get):
    """Test that API connection errors are handled gracefully."""
    from ui.utils.api_client import get_adrs
    
    # Mock API error
    mock_get.side_effect = Exception("Connection error")
    
    # Call the function
    result = get_adrs()
    
    # Check that error was handled
    assert result == {}
    mock_error.assert_called_with("Error fetching ADRs: Connection error")
