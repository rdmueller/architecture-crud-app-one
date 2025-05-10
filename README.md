# Architecture CRUD Application

Eine Web-basierte Anwendung zur Verwaltung von Architekturbeziehungen im JSON-Format.

## Features

- Verwaltung von Architecture Decision Records (ADRs)
- Verwaltung von Qualitätsanforderungen, Risiken, technischen Schulden und Komponenten
- Visualisierung von Beziehungen zwischen Architektur-Elementen
- JSON-Schema-basierte Validierung
- Export als AsciiDoc im arc42-Format

## Projektstruktur

```
architecture-crud-app/
├── docs/
│   ├── arc42/              # Arc42 Architekturdokumentation
│   │   ├── architecture.json   # Architektur im JSON-Format
│   │   └── ...            # AsciiDoc-Kapitel
│   └── specification/      # Anwendungsspezifikation
├── src/
│   └── json/
│       └── architecture-schema.json  # JSON-Schema Definition
└── README.md
```

## Architektur

Die Anwendung basiert auf folgenden Technologien:

- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Persistenz**: JSON-Dateien
- **Validierung**: JSON Schema + Pydantic
- **Export**: Jinja2 Templates für AsciiDoc-Generierung

## Dokumentation

- [Architekturdokumentation](docs/arc42/architecture-documentation.adoc)
- [Anwendungsspezifikation](docs/specification/crud-app-specification.md)

## Nächste Schritte

1. Implementierung der Basis-API mit FastAPI
2. Erstellung der Streamlit-UI
3. Implementierung der Beziehungsverwaltung
4. AsciiDoc-Export-Funktionalität
5. Testing und Dokumentation

## Lizenz

MIT License
