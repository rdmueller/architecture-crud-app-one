# UI Testing Guide

This document explains the UI testing strategy for the Architecture CRUD application.

## Testing Framework

We use a comprehensive testing approach for the Streamlit UI:

- **pytest**: Test framework
- **unittest.mock**: For mocking Streamlit components
- **Custom StreamlitTestHelper**: Utilities for testing Streamlit apps
- **Coverage.py**: For code coverage reporting

## Test Structure

```
tests/ui/
├── streamlit_test_utils.py    # Testing utilities
├── test_app.py               # Main app tests
└── pages/                    # Page-specific tests
    ├── test_dashboard_comprehensive.py
    ├── test_adrs_comprehensive.py
    ├── test_qualities.py
    ├── test_risks.py
    ├── test_technical_debts.py
    ├── test_components.py
    ├── test_relationships.py
    └── test_export.py
```

## Running Tests

### Run all UI tests:
```bash
python run_ui_tests.py
```

### Run specific test file:
```bash
pytest tests/ui/pages/test_dashboard_comprehensive.py -v
```

### Run with coverage:
```bash
pytest tests/ui --cov=src/ui --cov-report=html
```

## Test Patterns

### 1. Basic Page Test
```python
def test_page_renders_correctly():
    with mock_streamlit() as st_mock:
        from ui.pages.example import render_page
        
        render_page()
        
        # Assert header was called
        st_mock.mocks['header'].assert_called_with("Expected Header")
        
        # Check that specific components were rendered
        assert st_mock.mocks['button'].called
```

### 2. Form Submission Test
```python
def test_form_submission():
    with mock_streamlit() as st_mock:
        from ui.pages.example import render_page
        
        # Mock form input values
        st_mock.mock_widget('text_input', 'name', 'Test Name')
        st_mock.mock_widget('submit_button', 'submit', True)
        
        with patch('requests.post') as mock_post:
            mock_post.return_value = mock_successful_api_response({"id": "1"})
            
            render_page()
            
            # Assert API was called
            mock_post.assert_called_once()
            
            # Check success message
            assert len(st_mock.success_calls) > 0
```

### 3. API Error Handling Test
```python
def test_api_error_handling():
    with mock_streamlit() as st_mock:
        from ui.pages.example import render_page
        
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Connection error")
            
            render_page()
            
            # Check error was displayed
            assert len(st_mock.error_calls) > 0
            assert any("Error" in call for call in st_mock.error_calls)
```

## Coverage Goals

- Minimum coverage: 80%
- Critical paths: 100%
- Error handling: 100%
- User interactions: 90%

## CI/CD Integration

The UI tests are automatically run on:
- Every push to main branch
- Every pull request
- Scheduled nightly builds

Coverage reports are:
- Generated as HTML
- Uploaded as artifacts
- Sent to Codecov (if configured)

## Best Practices

1. **Mock External Dependencies**: Always mock API calls and external services
2. **Test User Flows**: Test complete user workflows, not just individual functions
3. **Test Error States**: Ensure all error conditions are handled gracefully
4. **Keep Tests Fast**: Use mocks to avoid slow operations
5. **Test Edge Cases**: Empty data, malformed input, API failures
6. **Maintain Test Data**: Use consistent test data across tests

## Common Issues

### 1. StreamlitAPIException
- **Cause**: Trying to access Streamlit components outside of app context
- **Solution**: Use `mock_streamlit()` context manager

### 2. Session State Issues
- **Cause**: Tests not properly mocking session state
- **Solution**: Use `st_mock.mock_session_state()` method

### 3. Widget Key Conflicts
- **Cause**: Duplicate widget keys in tests
- **Solution**: Use unique keys for each widget

## Adding New Tests

When adding new UI features:

1. Create test file following naming convention: `test_[feature]_comprehensive.py`
2. Use `StreamlitTestHelper` for consistent mocking
3. Test all user interactions
4. Test error conditions
5. Add to CI pipeline if needed

## Debugging Tests

To debug failing tests:

1. Run with verbose output: `pytest -v`
2. Use `--pdb` flag to drop into debugger
3. Check mock call history: `st_mock.mocks['widget_name'].call_args_list`
4. Print captured calls: `print(st_mock.markdown_calls)`

## Future Improvements

- [ ] Add visual regression testing
- [ ] Implement end-to-end tests with Selenium
- [ ] Add performance testing
- [ ] Create test data factories
- [ ] Add accessibility testing
