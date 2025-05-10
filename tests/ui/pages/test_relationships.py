"""Tests for the Relationships page."""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


@patch('streamlit.info')
@patch('streamlit.header')
def test_relationships_page_renders_header_and_tabs(mock_header, mock_info):
    """Test that Relationships page renders header and tabs."""
    from ui.pages.relationships import render_relationships
    
    # Mock empty fetch
    with patch('ui.pages.relationships.fetch_architecture_data') as mock_fetch:
        mock_fetch.return_value = {}
        
        render_relationships()
    
    # Check header was called
    mock_header.assert_called_with("Architecture Relationships")
    
    # Check that info message was shown for empty data
    mock_info.assert_called_with("No architecture data available. Please create some entities first.")


@patch('requests.get')
@patch('streamlit.dataframe')
@patch('streamlit.tabs')
@patch('streamlit.subheader')
@patch('streamlit.download_button')
@patch('streamlit.info')
def test_relationships_matrix_displays_dataframe(mock_info, mock_download, mock_subheader, 
                                                 mock_tabs, mock_dataframe, mock_get):
    """Test that Relationships matrix tab displays dataframe."""
    from ui.pages.relationships import render_relationships
    
    # Mock tabs to select matrix tab
    matrix_tab = MagicMock()
    graph_tab = MagicMock()
    manage_tab = MagicMock()
    mock_tabs.return_value = [matrix_tab, graph_tab, manage_tab]
    
    # Mock API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "adrs": {
            "ADR-001": {
                "id": "ADR-001",
                "title": "Test ADR",
                "relationships": {
                    "qualities": [
                        {"targetId": "Q-001", "type": "addresses"}
                    ]
                }
            }
        },
        "qualities": {
            "Q-001": {
                "id": "Q-001",
                "title": "Performance"
            }
        }
    }
    mock_get.return_value = mock_response
    
    # Mock context manager
    matrix_tab.__enter__ = MagicMock(return_value=matrix_tab)
    matrix_tab.__exit__ = MagicMock(return_value=None)
    graph_tab.__enter__ = MagicMock(return_value=graph_tab)
    graph_tab.__exit__ = MagicMock(return_value=None)
    manage_tab.__enter__ = MagicMock(return_value=manage_tab)
    manage_tab.__exit__ = MagicMock(return_value=None)
    
    render_relationships()
    
    # Check that dataframe was called
    assert mock_dataframe.called


@patch('streamlit.plotly_chart')
@patch('requests.get')
@patch('streamlit.tabs')
@patch('streamlit.subheader')
@patch('streamlit.markdown')
@patch('streamlit.columns')
def test_relationships_graph_displays_network(mock_columns, mock_markdown, mock_subheader, 
                                              mock_tabs, mock_get, mock_plotly_chart):
    """Test that Relationships graph tab displays network diagram."""
    from ui.pages.relationships import render_relationships
    
    # Mock tabs to select graph tab
    matrix_tab = MagicMock()
    graph_tab = MagicMock()
    manage_tab = MagicMock()
    mock_tabs.return_value = [matrix_tab, graph_tab, manage_tab]
    
    # Mock API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "adrs": {
            "ADR-001": {"id": "ADR-001", "title": "Test ADR"}
        },
        "qualities": {
            "Q-001": {"id": "Q-001", "title": "Performance"}
        }
    }
    mock_get.return_value = mock_response
    
    # Mock context manager
    matrix_tab.__enter__ = MagicMock(return_value=matrix_tab)
    matrix_tab.__exit__ = MagicMock(return_value=None)
    graph_tab.__enter__ = MagicMock(return_value=graph_tab)
    graph_tab.__exit__ = MagicMock(return_value=None)
    manage_tab.__enter__ = MagicMock(return_value=manage_tab)
    manage_tab.__exit__ = MagicMock(return_value=None)
    
    # Mock columns
    col_mock = MagicMock()
    col_mock.__enter__ = lambda self: self
    col_mock.__exit__ = lambda self, *args: None
    mock_columns.return_value = [col_mock, col_mock]
    
    render_relationships()
    
    # Check that plotly chart was called
    assert mock_plotly_chart.called


@patch('requests.get')
@patch('streamlit.error')
def test_relationships_handles_api_error(mock_error, mock_get):
    """Test that Relationships page handles API errors gracefully."""
    from ui.pages.relationships import render_relationships
    
    # Mock API error
    mock_get.side_effect = Exception("API Error")
    
    render_relationships()
    
    # Check that error was displayed
    mock_error.assert_called_with("Error connecting to API: API Error")


@patch('streamlit.info')
@patch('requests.get')
def test_relationships_handles_empty_data(mock_get, mock_info):
    """Test that Relationships page handles empty data."""
    from ui.pages.relationships import render_relationships
    
    # Mock empty API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response
    
    render_relationships()
    
    # Check that info message was shown
    mock_info.assert_called_with("No architecture data available. Please create some entities first.")
