"""Tests for the dashboard page."""
import pytest
from unittest.mock import patch, MagicMock, call
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


@patch('streamlit.columns')
@patch('streamlit.markdown')
@patch('requests.get')
@patch('streamlit.metric')
@patch('streamlit.header')
def test_dashboard_renders_metrics(mock_header, mock_metric, mock_get, mock_markdown, mock_columns):
    """Test that dashboard renders metric cards."""
    from ui.pages.dashboard import render_dashboard
    
    # Mock API responses
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "adrs": {"ADR-001": {"id": "ADR-001", "title": "Test ADR", "status": "accepted", "date": "2025-05-10"}},
        "qualities": {"Q-001": {"id": "Q-001", "title": "Test Quality"}},
        "risks": {},
        "technicalDebts": {},
        "components": {}
    }
    mock_get.return_value = mock_response
    
    # Mock columns to return correct number of columns
    col_mock = MagicMock()
    col_mock.__enter__ = lambda self: self
    col_mock.__exit__ = lambda self, *args: None
    
    # First call returns 5 columns for metrics
    # Second call returns 2 columns for recent items
    mock_columns.side_effect = [
        [col_mock, col_mock, col_mock, col_mock, col_mock],  # metrics columns
        [col_mock, col_mock],  # recent items columns
        [col_mock, col_mock],  # visualization columns
    ]
    
    # Call render function
    render_dashboard()
    
    # Check that header was called
    mock_header.assert_called_with("Architecture Overview")
    
    # Check that metrics were called
    assert mock_metric.call_count >= 5  # At least 5 metric cards


@patch('streamlit.info')
@patch('streamlit.columns')
@patch('streamlit.markdown')
@patch('requests.get')
@patch('streamlit.subheader')
@patch('streamlit.dataframe')
@patch('streamlit.header')
@patch('streamlit.metric')
def test_dashboard_renders_recent_items(mock_metric, mock_header, mock_dataframe, mock_subheader, 
                                        mock_get, mock_markdown, mock_columns, mock_info):
    """Test that dashboard renders recent items section."""
    from ui.pages.dashboard import render_dashboard
    
    # Mock API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "adrs": {
            "ADR-001": {
                "id": "ADR-001",
                "title": "Test ADR",
                "date": "2025-05-10",
                "status": "accepted"
            }
        },
        "qualities": {},
        "risks": {},
        "technicalDebts": {},
        "components": {}
    }
    mock_get.return_value = mock_response
    
    # Mock columns to return correct number
    col_mock = MagicMock()
    col_mock.__enter__ = lambda self: self
    col_mock.__exit__ = lambda self, *args: None
    
    mock_columns.side_effect = [
        [col_mock, col_mock, col_mock, col_mock, col_mock],  # metrics columns
        [col_mock, col_mock],  # recent items columns
        [col_mock, col_mock],  # visualization columns
    ]
    
    # Call render function
    render_dashboard()
    
    # Check that recent items section is rendered
    mock_subheader.assert_any_call("Recent ADRs")
    
    # Check that dataframe was called for recent items
    assert mock_dataframe.called


@patch('requests.get')
@patch('streamlit.error')
def test_dashboard_handles_api_error(mock_error, mock_get):
    """Test that dashboard handles API errors gracefully."""
    from ui.pages.dashboard import render_dashboard
    
    # Mock API error
    mock_get.side_effect = Exception("API Error")
    
    # Call render function
    render_dashboard()
    
    # Check that error was displayed
    mock_error.assert_called_with("Error connecting to API: API Error")


@patch('streamlit.info')
@patch('streamlit.subheader')
@patch('streamlit.plotly_chart')
@patch('streamlit.columns')
@patch('streamlit.markdown')
@patch('requests.get')
@patch('streamlit.header')
@patch('streamlit.metric')
@patch('streamlit.dataframe')
def test_dashboard_renders_charts(mock_dataframe, mock_metric, mock_header, mock_get, mock_markdown, 
                                  mock_columns, mock_plotly_chart, mock_subheader, mock_info):
    """Test that dashboard renders visualization charts."""
    from ui.pages.dashboard import render_dashboard
    
    # Mock API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "adrs": {"ADR-001": {"id": "ADR-001", "status": "accepted", "title": "Test ADR", "date": "2025-05-10"}},
        "qualities": {},
        "risks": {"RISK-001": {"id": "RISK-001", "impact": "high", "likelihood": "medium", "title": "Test Risk", "status": "identified"}},
        "technicalDebts": {},
        "components": {}
    }
    mock_get.return_value = mock_response
    
    # Mock columns to return correct number
    col_mock = MagicMock()
    col_mock.__enter__ = lambda self: self
    col_mock.__exit__ = lambda self, *args: None
    
    mock_columns.side_effect = [
        [col_mock, col_mock, col_mock, col_mock, col_mock],  # metrics columns
        [col_mock, col_mock],  # recent items columns
        [col_mock, col_mock],  # visualization columns
    ]
    
    # Call render function
    render_dashboard()
    
    # Check that charts were rendered
    assert mock_plotly_chart.called
