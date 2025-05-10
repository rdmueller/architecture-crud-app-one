"""Tests for the Export page."""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
import json

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


@patch('streamlit.header')
def test_export_page_renders_header(mock_header):
    """Test that Export page renders header."""
    from ui.pages.export import render_export
    
    # Mock empty fetch
    with patch('ui.pages.export.fetch_architecture_data') as mock_fetch:
        mock_fetch.return_value = {}
        render_export()
    
    # Check header was called
    mock_header.assert_called_with("Export Architecture Documentation")


@patch('streamlit.info')
@patch('requests.get')
def test_export_handles_empty_data(mock_get, mock_info):
    """Test that Export page handles empty data."""
    from ui.pages.export import render_export
    
    # Mock empty API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response
    
    render_export()
    
    # Check that info message was shown
    mock_info.assert_called_with("No architecture data available to export.")


@patch('streamlit.download_button')
@patch('requests.get')
@patch('streamlit.columns')
def test_export_renders_download_buttons(mock_columns, mock_get, mock_download_button):
    """Test that Export page renders download buttons."""
    from ui.pages.export import render_export
    
    # Mock API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "adrs": {
            "ADR-001": {
                "id": "ADR-001",
                "title": "Test ADR",
                "status": "accepted",
                "date": "2025-05-10",
                "authors": ["John Doe"],
                "context": "Test context",
                "decision": "Test decision"
            }
        }
    }
    mock_get.return_value = mock_response
    
    # Mock columns - return different number of columns for different calls
    def mock_columns_side_effect(num_cols):
        col_mock = MagicMock()
        col_mock.__enter__ = lambda self: self
        col_mock.__exit__ = lambda self, *args: None
        return [col_mock for _ in range(num_cols)]
    
    mock_columns.side_effect = mock_columns_side_effect
    
    render_export()
    
    # Check that download buttons were created
    assert mock_download_button.call_count >= 3  # JSON, AsciiDoc, ZIP


def test_export_asciidoc_generates_content():
    """Test that export_asciidoc generates proper content."""
    from ui.pages.export import export_asciidoc
    
    test_data = {
        "adrs": {
            "ADR-001": {
                "id": "ADR-001",
                "title": "Test ADR",
                "status": "accepted",
                "date": "2025-05-10",
                "authors": ["John Doe"],
                "context": "Test context",
                "decision": "Test decision"
            }
        },
        "qualities": {
            "Q-001": {
                "id": "Q-001",
                "title": "Performance",
                "description": "High performance requirements",
                "priority": "must",
                "metrics": [
                    {
                        "metricName": "Response Time",
                        "targetValue": "< 200ms",
                        "unit": "milliseconds"
                    }
                ]
            }
        }
    }
    
    result = export_asciidoc(test_data)
    
    # Check that AsciiDoc contains expected sections
    assert "= Architecture Documentation" in result
    assert "== Architecture Decision Records" in result
    assert "=== ADR-001: Test ADR" in result
    assert "*Status:* accepted" in result
    assert "==== Context" in result
    assert "Test context" in result
    assert "== Quality Requirements" in result
    assert "=== Q-001: Performance" in result
    assert "*Priority:* must" in result
    assert "Response Time: < 200ms milliseconds" in result


def test_create_zip_export():
    """Test that create_zip_export creates proper ZIP file."""
    from ui.pages.export import create_zip_export
    import zipfile
    import io
    
    test_data = {
        "adrs": {
            "ADR-001": {
                "id": "ADR-001",
                "title": "Test ADR",
                "status": "accepted"
            }
        }
    }
    
    zip_bytes = create_zip_export(test_data)
    
    # Check that ZIP file is created
    assert len(zip_bytes) > 0
    
    # Check ZIP contents
    with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zip_file:
        file_names = zip_file.namelist()
        
        assert 'architecture.json' in file_names
        assert 'architecture.adoc' in file_names
        assert 'README.txt' in file_names
        
        # Check JSON content
        with zip_file.open('architecture.json') as json_file:
            json_data = json.loads(json_file.read())
            assert json_data == test_data


@patch('streamlit.metric')
@patch('requests.get')
@patch('streamlit.columns')
def test_export_displays_statistics(mock_columns, mock_get, mock_metric):
    """Test that Export page displays statistics."""
    from ui.pages.export import render_export
    
    # Mock API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "adrs": {"ADR-001": {}, "ADR-002": {}},
        "qualities": {"Q-001": {}},
        "risks": {"R-001": {}, "R-002": {}, "R-003": {}},
        "technicalDebts": {},
        "components": {"C-001": {}}
    }
    mock_get.return_value = mock_response
    
    # Mock columns - return different number of columns for different calls
    def mock_columns_side_effect(num_cols):
        col_mock = MagicMock()
        col_mock.__enter__ = lambda self: self
        col_mock.__exit__ = lambda self, *args: None
        return [col_mock for _ in range(num_cols)]
    
    mock_columns.side_effect = mock_columns_side_effect
    
    render_export()
    
    # Check that metrics were called with correct values
    metric_calls = [call[0] for call in mock_metric.call_args_list]
    
    # Find the metric calls and their values
    metric_dict = {}
    for call in mock_metric.call_args_list:
        metric_dict[call[0][0]] = call[0][1]
    
    assert metric_dict.get("Total ADRs") == 2
    assert metric_dict.get("Total Qualities") == 1
    assert metric_dict.get("Total Risks") == 3
    assert metric_dict.get("Total Components") == 1
