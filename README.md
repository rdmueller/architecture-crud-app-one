# Architecture CRUD Application

A web application for managing architectural relationships between Architecture Decision Records (ADRs), Quality Requirements, Risks, Technical Debts, and Components.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete all entity types
- **Relationship Management**: Define and manage relationships between entities
- **JSON-based Storage**: Simple file-based persistence
- **REST API**: Full REST API with automatic OpenAPI documentation
- **Streamlit UI**: Modern, responsive user interface
- **Type Safety**: Built with FastAPI and Pydantic for full type safety
- **Validation**: Comprehensive validation including business rules
- **Dashboard**: Visualizations and metrics overview
- **Export**: Export to JSON and AsciiDoc formats

## Project Structure

```
architecture-crud-app/
├── src/
│   ├── api/                 # FastAPI application
│   │   ├── models/          # Pydantic models
│   │   ├── routes/          # API endpoints
│   │   └── dependencies.py  # Dependency injection
│   ├── data/                # Data layer
│   │   ├── repository.py    # Data persistence
│   │   └── validator.py     # Schema validation
│   ├── ui/                  # Streamlit UI
│   │   ├── pages/           # UI pages
│   │   └── utils/           # UI utilities
│   └── json/                # JSON schemas
├── tests/                   # Test suite
├── data/                    # JSON data storage
└── docs/                    # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd architecture-crud-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Quick Start (with example data)

To start the application with example data already loaded:

```bash
# Start the API with data initialization
python run_api_with_data.py

# In another terminal, start the UI
python run_ui_with_data.py
```

### Manual Start

If you want to start without automatic data initialization:

#### Start the API Server

```bash
python run_api.py
```

The API will be available at `http://localhost:8082`

#### Start the Streamlit UI

In a separate terminal:

```bash
streamlit run src/ui/app.py
```

The UI will be available at `http://localhost:8501`

### Initialize Example Data

If you need to manually initialize example data:

```bash
python initialize_data.py
```

This will copy the example data from `data/example_architecture.json` to `data/architecture.json`.

## API Documentation

Once the API server is running, you can access:
- OpenAPI documentation: `http://localhost:8082/docs`
- ReDoc documentation: `http://localhost:8082/redoc`

## API Endpoints

### Architecture
- `GET /api/architecture` - Get complete architecture data
- `PUT /api/architecture` - Update complete architecture

### ADRs
- `GET /api/adrs` - List all ADRs
- `GET /api/adrs/{id}` - Get specific ADR
- `POST /api/adrs` - Create new ADR
- `PUT /api/adrs/{id}` - Update ADR
- `DELETE /api/adrs/{id}` - Delete ADR

### Quality Requirements
- `GET /api/qualities` - List all quality requirements
- `GET /api/qualities/{id}` - Get specific quality requirement
- `POST /api/qualities` - Create new quality requirement
- `PUT /api/qualities/{id}` - Update quality requirement
- `DELETE /api/qualities/{id}` - Delete quality requirement

### Risks
- `GET /api/risks` - List all risks
- `GET /api/risks/{id}` - Get specific risk
- `POST /api/risks` - Create new risk
- `PUT /api/risks/{id}` - Update risk
- `DELETE /api/risks/{id}` - Delete risk

### Technical Debts
- `GET /api/technical-debts` - List all technical debts
- `GET /api/technical-debts/{id}` - Get specific technical debt
- `POST /api/technical-debts` - Create new technical debt
- `PUT /api/technical-debts/{id}` - Update technical debt
- `DELETE /api/technical-debts/{id}` - Delete technical debt

### Components
- `GET /api/components` - List all components
- `GET /api/components/{id}` - Get specific component
- `POST /api/components` - Create new component
- `PUT /api/components/{id}` - Update component
- `DELETE /api/components/{id}` - Delete component

### Export
- `GET /api/export/asciidoc` - Export to AsciiDoc format

## Testing

### Run Backend Tests
```bash
pytest tests/api tests/data -v
```

### Run Frontend Tests
```bash
python run_ui_tests_simple.py
```

### Run All Tests with Coverage
```bash
pytest --cov=src --cov-report=html
```

## Development

### Code Style

The project follows PEP 8 style guidelines. Format code with:
```bash
black src tests
```

### Type Checking

Run type checking with:
```bash
mypy src
```

## Data Storage

Data is stored in JSON format in the `data/` directory. The default file is `data/architecture.json`. You can specify a different file using the `ARCHITECTURE_DATA_FILE` environment variable:

```bash
export ARCHITECTURE_DATA_FILE=data/my-architecture.json
python run_api.py
```

## Example Data

The application comes with example data in `data/example_architecture.json`. This includes:
- Sample ADRs with alternatives and relationships
- Quality requirements with metrics
- Risks with mitigation strategies
- Technical debts with remediation plans
- Components with interfaces and attributes

## Troubleshooting

### No Data Showing in UI

If the UI shows no data:
1. Make sure the API is running (`http://localhost:8082/health` should respond)
2. Initialize the example data: `python initialize_data.py`
3. Restart both the API and UI

### Port Already in Use

If you get a port already in use error:
- API: Change the port in `run_api.py` (default: 8082)
- UI: Change the port with `streamlit run src/ui/app.py --server.port 8502`

## License

This project is licensed under the MIT License.
