"""Utilities for testing Streamlit applications."""
import streamlit as st
from unittest.mock import MagicMock, patch, Mock
from contextlib import contextmanager
import pandas as pd
from typing import Any, Dict, List, Optional
import pytest


class StreamlitTestHelper:
    """Helper class for testing Streamlit components."""
    
    def __init__(self):
        self.widgets = {}
        self.markdown_calls = []
        self.write_calls = []
        self.error_calls = []
        self.success_calls = []
        self.info_calls = []
        self.warning_calls = []
        self.dataframe_calls = []
        self.session_state = {}
        
    def mock_widget(self, widget_type: str, key: str, value: Any):
        """Mock a widget with a specific return value."""
        self.widgets[key] = value
        return value
    
    def get_widget_value(self, key: str):
        """Get the value of a mocked widget."""
        return self.widgets.get(key)
    
    def mock_session_state(self, key: str, value: Any):
        """Mock session state value."""
        self.session_state[key] = value
    
    def get_session_state(self, key: str):
        """Get session state value."""
        return self.session_state.get(key)


@contextmanager
def mock_streamlit():
    """Context manager that mocks Streamlit components."""
    helper = StreamlitTestHelper()
    
    # Create all mocks
    mocks = {
        'columns': MagicMock(),
        'tabs': MagicMock(),
        'text_input': MagicMock(),
        'text_area': MagicMock(),
        'selectbox': MagicMock(),
        'multiselect': MagicMock(),
        'number_input': MagicMock(),
        'date_input': MagicMock(),
        'checkbox': MagicMock(),
        'button': MagicMock(),
        'form_submit_button': MagicMock(),
        'form': MagicMock(),
        'markdown': MagicMock(),
        'write': MagicMock(),
        'error': MagicMock(),
        'success': MagicMock(),
        'info': MagicMock(),
        'warning': MagicMock(),
        'dataframe': MagicMock(),
        'plotly_chart': MagicMock(),
        'download_button': MagicMock(),
        'metric': MagicMock(),
        'header': MagicMock(),
        'subheader': MagicMock(),
        'json': MagicMock(),
        'expander': MagicMock(),
        'spinner': MagicMock(),
        'rerun': MagicMock()
    }
    
    # Setup context manager helper
    def create_context_manager(obj):
        obj.__enter__ = lambda self: self
        obj.__exit__ = lambda self, *args: None
        return obj
    
    # Mock columns to return context managers
    def mock_columns_func(num_cols, **kwargs):
        cols = [create_context_manager(MagicMock()) for _ in range(num_cols)]
        return cols
    
    mocks['columns'].side_effect = mock_columns_func
    
    # Mock tabs to return context managers
    def mock_tabs_func(tab_names):
        tabs = [create_context_manager(MagicMock()) for _ in tab_names]
        return tabs
    
    mocks['tabs'].side_effect = mock_tabs_func
    
    # Mock form to return context manager
    mocks['form'].return_value = create_context_manager(MagicMock())
    
    # Mock expander to return context manager
    mocks['expander'].return_value = create_context_manager(MagicMock())
    
    # Mock spinner to return context manager
    mocks['spinner'].return_value = create_context_manager(MagicMock())
    
    # Setup widget mocks
    mocks['text_input'].side_effect = lambda label, **kwargs: helper.mock_widget('text_input', kwargs.get('key', label), kwargs.get('value', ''))
    mocks['text_area'].side_effect = lambda label, **kwargs: helper.mock_widget('text_area', kwargs.get('key', label), kwargs.get('value', ''))
    mocks['selectbox'].side_effect = lambda label, options, **kwargs: helper.mock_widget('selectbox', kwargs.get('key', label), options[0] if options else None)
    mocks['multiselect'].side_effect = lambda label, options, **kwargs: helper.mock_widget('multiselect', kwargs.get('key', label), kwargs.get('default', []))
    mocks['number_input'].side_effect = lambda label, **kwargs: helper.mock_widget('number_input', kwargs.get('key', label), kwargs.get('value', 0))
    mocks['date_input'].side_effect = lambda label, **kwargs: helper.mock_widget('date_input', kwargs.get('key', label), kwargs.get('value', None))
    mocks['checkbox'].side_effect = lambda label, **kwargs: helper.mock_widget('checkbox', kwargs.get('key', label), kwargs.get('value', False))
    mocks['button'].side_effect = lambda label, **kwargs: helper.mock_widget('button', kwargs.get('key', label), False)
    mocks['form_submit_button'].side_effect = lambda label, **kwargs: helper.mock_widget('submit_button', kwargs.get('key', label), False)
    
    # Track calls to display functions
    mocks['markdown'].side_effect = lambda text, **kwargs: helper.markdown_calls.append(text)
    mocks['write'].side_effect = lambda *args, **kwargs: helper.write_calls.extend(args)
    mocks['error'].side_effect = lambda text: helper.error_calls.append(text)
    mocks['success'].side_effect = lambda text: helper.success_calls.append(text)
    mocks['info'].side_effect = lambda text: helper.info_calls.append(text)
    mocks['warning'].side_effect = lambda text: helper.warning_calls.append(text)
    mocks['dataframe'].side_effect = lambda df, **kwargs: helper.dataframe_calls.append(df)
    
    # Mock session state
    mock_session_state = MagicMock()
    mock_session_state.__getitem__ = lambda self, key: helper.get_session_state(key)
    mock_session_state.__setitem__ = lambda self, key, value: helper.mock_session_state(key, value)
    mock_session_state.__contains__ = lambda self, key: key in helper.session_state
    mocks['session_state'] = mock_session_state
    
    # Add all mocks to the helper for easy access
    helper.mocks = mocks
    
    # Create patches
    patches = []
    for name, mock_obj in mocks.items():
        if name != 'session_state':  # session_state is handled differently
            p = patch(f'streamlit.{name}', mock_obj)
            patches.append(p)
    
    # Start all patches
    for p in patches:
        p.start()
    
    try:
        yield helper
    finally:
        # Stop all patches
        for p in patches:
            p.stop()


def mock_successful_api_response(data: Dict[str, Any]):
    """Create a mock successful API response."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = data
    return response


def mock_error_api_response(status_code: int, error_message: str):
    """Create a mock error API response."""
    response = MagicMock()
    response.status_code = status_code
    response.json.return_value = {"detail": error_message}
    response.text = error_message
    return response
