# CLAUDE.md
Diese Datei enthält Anleitungen für Claude Code (claude.ai/code) bei der Arbeit mit Code in diesem Repository.

## Build/Test/Lint Commands
```bash
# Setup
python -m venv venv && source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Run tests
pytest                                # All tests
pytest tests/test_api.py::test_func  # Single test
pytest -v -s                         # Verbose with stdout

# Lint/Format
black src/ tests/                    # Format code
isort src/ tests/                    # Sort imports
mypy src/                           # Type checking
flake8 src/ tests/                  # Style check
```

## Code Style Guidelines
- **Python 3.10+** with type hints everywhere
- **Imports**: Use absolute imports, group by stdlib/third-party/local
- **Format**: Black + isort, line length 88 chars
- **Naming**: snake_case for functions, PascalCase for classes, UPPER_CASE for constants
- **Types**: Pydantic models for API, full type annotations, avoid Any
- **Errors**: Custom exceptions, early returns, explicit error messages
- **Docstrings**: Google style, describe purpose and params
- **Architecture**: Repository pattern, separate concerns (API/UI/Data/Generator)
- **JSON**: Always validate against schema before saving
- **Tests**: Test data validation, API endpoints, and JSON transformations
