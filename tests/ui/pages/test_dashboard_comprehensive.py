"""Comprehensive tests for the dashboard page."""
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Add test utilities to path
test_path = Path(__file__).parent.parent
sys.path.insert(0, str(test_path))

from streamlit_test_utils import mock_streamlit, mock_successful_api_response, mock_error_api_response


class TestDashboard:
    """Test suite for the dashboard page."""
    
    def setup_sample_architecture_data(self):
        """Create sample architecture data for testing."""
        return {
            "adrs": {
                "ADR-001": {
                    "id": "ADR-001",
                    "title": "Use FastAPI for Backend",
                    "status": "accepted",
                    "date": "2025-05-10",
                    "authors": ["John Doe"],
                    "context": "We need to choose a web framework",
                    "decision": "We will use FastAPI",
                    "relationships": {
                        "qualities": [],
                        "risks": ["RISK-001"],
                        "technicalDebts": [],
                        "components": ["COMP-001"]
                    }
                },
                "ADR-002": {
                    "id": "ADR-002",
                    "title": "Use Streamlit for Frontend",
                    "status": "accepted",
                    "date": "2025-05-11",
                    "authors": ["Jane Doe"]
                }
            },
            "qualities": {
                "Q-001": {
                    "id": "Q-001",
                    "title": "Performance",
                    "description": "System should be fast",
                    "priority": "high"
                }
            },
            "risks": {
                "RISK-001": {
                    "id": "RISK-001",
                    "title": "Scalability Risk",
                    "impact": "high",
                    "likelihood": "medium",
                    "status": "identified"
                }
            },
            "technicalDebts": {
                "TD-001": {
                    "id": "TD-001",
                    "title": "Refactor validation logic",
                    "impact": "medium",
                    "effort": "medium",
                    "status": "open"
                }
            },
            "components": {
                "COMP-001": {
                    "id": "COMP-001",
                    "title": "API Gateway",
                    "responsibility": "Routes API requests"
                }
            }
        }
    
    def test_dashboard_renders_all_sections(self):
        """Test that dashboard renders all expected sections."""
        with mock_streamlit() as st_mock:
            from ui.pages.dashboard import render_dashboard
            
            # Mock API response
            sample_data = self.setup_sample_architecture_data()
            
            with patch('requests.get') as mock_get:
                mock_get.return_value = mock_successful_api_response(sample_data)
                
                render_dashboard()
                
                # Check that header was called
                st_mock.mocks['header'].assert_called_with("Architecture Overview")
                
                # Check that metrics were displayed
                assert st_mock.mocks['metric'].call_count >= 5
                metric_calls = [call[0] for call in st_mock.mocks['metric'].call_args_list]
                assert "ADRs" in metric_calls[0]
                assert "Qualities" in metric_calls[1]
                assert "Risks" in metric_calls[2]
                assert "Technical Debts" in metric_calls[3]
                assert "Components" in metric_calls[4]
                
                # Check that markdown sections were created
                assert any("Key Metrics" in call for call in st_mock.markdown_calls)
                assert any("Recent Activity" in call for call in st_mock.markdown_calls)
                assert any("Visualizations" in call for call in st_mock.markdown_calls)
                
                # Check that subheaders were created
                subheader_calls = [call[0][0] for call in st_mock.mocks['subheader'].call_args_list]
                assert "Recent ADRs" in subheader_calls
                assert "Open Risks" in subheader_calls
    
    def test_dashboard_displays_recent_adrs(self):
        """Test that dashboard correctly displays recent ADRs."""
        with mock_streamlit() as st_mock:
            from ui.pages.dashboard import render_dashboard
            
            sample_data = self.setup_sample_architecture_data()
            
            with patch('requests.get') as mock_get:
                mock_get.return_value = mock_successful_api_response(sample_data)
                
                render_dashboard()
                
                # Check that dataframe was called with ADR data
                assert len(st_mock.dataframe_calls) > 0
                df = st_mock.dataframe_calls[0]
                assert isinstance(df, pd.DataFrame)
                assert "ADR-002" in df["ID"].values  # Most recent ADR
                assert df.iloc[0]["Title"] == "Use Streamlit for Frontend"
    
    def test_dashboard_displays_open_risks(self):
        """Test that dashboard correctly displays open risks."""
        with mock_streamlit() as st_mock:
            from ui.pages.dashboard import render_dashboard
            
            sample_data = self.setup_sample_architecture_data()
            
            with patch('requests.get') as mock_get:
                mock_get.return_value = mock_successful_api_response(sample_data)
                
                render_dashboard()
                
                # Check that risk dataframe was created
                assert len(st_mock.dataframe_calls) > 1
                risk_df = None
                for df in st_mock.dataframe_calls:
                    if isinstance(df, pd.DataFrame) and "Impact" in df.columns:
                        risk_df = df
                        break
                
                assert risk_df is not None
                assert "RISK-001" in risk_df["ID"].values
                assert risk_df.iloc[0]["Impact"] == "high"
    
    def test_dashboard_creates_visualizations(self):
        """Test that dashboard creates visualization charts."""
        with mock_streamlit() as st_mock:
            from ui.pages.dashboard import render_dashboard
            
            sample_data = self.setup_sample_architecture_data()
            
            with patch('requests.get') as mock_get:
                mock_get.return_value = mock_successful_api_response(sample_data)
                
                render_dashboard()
                
                # Check that plotly charts were created
                assert st_mock.mocks['plotly_chart'].call_count >= 2
                
                # Check that visualization subheaders were created
                subheader_calls = [call[0][0] for call in st_mock.mocks['subheader'].call_args_list]
                assert "ADR Status Distribution" in subheader_calls
                assert "Risk Heat Map" in subheader_calls
    
    def test_dashboard_handles_empty_data(self):
        """Test that dashboard handles empty data gracefully."""
        with mock_streamlit() as st_mock:
            from ui.pages.dashboard import render_dashboard
            
            empty_data = {
                "adrs": {},
                "qualities": {},
                "risks": {},
                "technicalDebts": {},
                "components": {}
            }
            
            with patch('requests.get') as mock_get:
                mock_get.return_value = mock_successful_api_response(empty_data)
                
                render_dashboard()
                
                # Check that info messages were displayed
                assert len(st_mock.info_calls) > 0
                assert any("No ADRs" in call for call in st_mock.info_calls)
    
    def test_dashboard_handles_api_errors(self):
        """Test that dashboard handles API errors gracefully."""
        with mock_streamlit() as st_mock:
            from ui.pages.dashboard import render_dashboard
            
            with patch('requests.get') as mock_get:
                mock_get.side_effect = Exception("Connection error")
                
                render_dashboard()
                
                # Check that error was displayed
                assert len(st_mock.error_calls) > 0
                assert any("API" in call for call in st_mock.error_calls)
    
    def test_dashboard_technical_debt_section(self):
        """Test the technical debt section of the dashboard."""
        with mock_streamlit() as st_mock:
            from ui.pages.dashboard import render_dashboard
            
            sample_data = self.setup_sample_architecture_data()
            
            with patch('requests.get') as mock_get:
                mock_get.return_value = mock_successful_api_response(sample_data)
                
                render_dashboard()
                
                # Check that technical debt section was rendered
                assert any("Technical Debt Overview" in call for call in st_mock.markdown_calls)
                
                # Check that technical debt data was displayed
                debt_df = None
                for df in st_mock.dataframe_calls:
                    if isinstance(df, pd.DataFrame) and "Effort" in df.columns:
                        debt_df = df
                        break
                
                assert debt_df is not None
                assert "TD-001" in debt_df["ID"].values
    
    def test_dashboard_api_fallback_mechanism(self):
        """Test that dashboard falls back to individual endpoints when architecture endpoint fails."""
        with mock_streamlit() as st_mock:
            from ui.pages.dashboard import render_dashboard
            
            # Mock individual endpoint responses
            adrs_data = ["ADR-001", "ADR-002"]
            qualities_data = ["Q-001"]
            
            def side_effect(url):
                if "architecture" in url:
                    return mock_error_api_response(500, "Internal Server Error")
                elif "adrs" in url:
                    return mock_successful_api_response(adrs_data)
                elif "qualities" in url:
                    return mock_successful_api_response(qualities_data)
                else:
                    return mock_successful_api_response({})
            
            with patch('requests.get') as mock_get:
                mock_get.side_effect = side_effect
                
                render_dashboard()
                
                # Check that multiple API calls were made
                assert mock_get.call_count > 1
                
                # Check that data was still displayed
                assert st_mock.mocks['metric'].call_count >= 5
