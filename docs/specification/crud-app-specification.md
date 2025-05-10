# Architecture CRUD Application - Spezifikation

## 1. Überblick

Die Architecture CRUD Application ist ein Werkzeug zur Verwaltung von Architekturbeziehungen basierend auf einem definierten JSON-Schema. Die Anwendung ermöglicht es, Architecture Decision Records (ADRs), Qualitätsanforderungen, Risiken, technische Schulden und Komponenten zu verwalten und deren Beziehungen zu visualisieren.

## 2. Funktionale Anforderungen

### 2.1 Datenverwaltung

#### 2.1.1 CRUD-Operationen
- **Create**: Neue Einträge für alle Entitätstypen erstellen
- **Read**: Einzelne Einträge und Listen anzeigen
- **Update**: Bestehende Einträge bearbeiten
- **Delete**: Einträge löschen (mit Bestätigung)

#### 2.1.2 Unterstützte Entitäten
1. **Architecture Decision Records (ADRs)**
   - ID, Titel, Status, Datum, Autoren
   - Kontext und Problemstellung
   - Betrachtete Alternativen mit Vor-/Nachteilen
   - Getroffene Entscheidung
   - Beziehungen zu anderen Entitäten

2. **Qualitätsanforderungen**
   - ID, Titel, Beschreibung
   - Metriken mit Zielwerten
   - Priorität

3. **Risiken**
   - ID, Titel, Beschreibung
   - Auswirkung und Eintrittswahrscheinlichkeit
   - Mitigationsstrategie
   - Status

4. **Technische Schulden**
   - ID, Titel, Beschreibung
   - Auswirkung und Behebungsaufwand
   - Behebungsplan
   - Status

5. **Komponenten**
   - ID, Titel, Verantwortlichkeit
   - Schnittstellen
   - Attribute

### 2.2 Beziehungsverwaltung

- Beziehungen zwischen ADRs und anderen Entitäten definieren
- Typ und Stärke von Beziehungen festlegen
- Bidirektionale Beziehungen automatisch pflegen
- Konsistenz von Beziehungen sicherstellen

### 2.3 Visualisierung

- Übersichtslisten für alle Entitätstypen
- Detailansichten mit allen Beziehungen
- Beziehungsmatrix (Tabellen-Darstellung)
- Interaktiver Beziehungsgraph (optional)

### 2.4 Export

- Export als AsciiDoc im arc42-Format
- Generierung von Kapiteln basierend auf JSON-Daten
- Download als ZIP-Archiv

### 2.5 Validierung

- Echtzeit-Validierung gegen JSON-Schema
- Klare Fehlermeldungen bei Validierungsfehlern
- Verhinderung ungültiger Datenzustände

## 3. Technische Architektur

### 3.1 Technologie-Stack

#### Backend
- **Framework**: FastAPI
- **Validierung**: Pydantic + jsonschema
- **Persistenz**: JSON-Dateien
- **Templates**: Jinja2

#### Frontend
- **Framework**: Streamlit
- **Visualisierung**: Streamlit-native Komponenten
- **HTTP-Client**: requests

#### Deployment
- **Container**: Docker (optional)
- **Server**: Uvicorn (FastAPI) + Streamlit Server

### 3.2 Projektstruktur

```
architecture-crud-app/
├── src/
│   ├── api/                 # FastAPI Anwendung
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI App
│   │   ├── routes/         # API Endpoints
│   │   ├── models/         # Pydantic Models
│   │   ├── services/       # Business Logic
│   │   └── utils/          # Hilfsfunktionen
│   ├── ui/                 # Streamlit UI
│   │   ├── __init__.py
│   │   ├── app.py          # Streamlit App
│   │   ├── pages/          # UI Seiten
│   │   └── components/     # UI Komponenten
│   ├── data/               # Datenschicht
│   │   ├── __init__.py
│   │   ├── repository.py   # Datenzugriff
│   │   └── validator.py    # Schema-Validierung
│   ├── generator/          # AsciiDoc Generator
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── templates/      # Jinja2 Templates
│   └── json/
│       └── architecture-schema.json
├── data/                   # JSON Datenspeicher
│   └── architecture.json
├── templates/              # AsciiDoc Templates
├── tests/                  # Unit Tests
├── docs/                   # Dokumentation
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 3.3 API-Endpunkte

#### ADR-Endpunkte
- `GET /api/adrs` - Liste aller ADRs
- `GET /api/adrs/{id}` - Einzelnes ADR
- `POST /api/adrs` - Neues ADR erstellen
- `PUT /api/adrs/{id}` - ADR aktualisieren
- `DELETE /api/adrs/{id}` - ADR löschen

#### Weitere Endpunkte (analog für andere Entitäten)
- `/api/qualities`
- `/api/risks`
- `/api/technical-debts`
- `/api/components`

#### Spezielle Endpunkte
- `GET /api/relationships` - Alle Beziehungen
- `POST /api/export/asciidoc` - AsciiDoc Export

### 3.4 Datenmodelle

```python
# Beispiel: ADR Model
class ADR(BaseModel):
    id: str = Field(regex="^ADR-[0-9]{3}$")
    title: str = Field(min_length=5, max_length=100)
    status: Literal["proposed", "accepted", "rejected", "deprecated", "superseded"]
    date: date
    authors: List[str]
    context: str
    decision: str
    relationships: Relationships
    
class Relationships(BaseModel):
    qualities: List[QualityRelationship]
    risks: List[RiskRelationship]
    technicalDebts: List[TechnicalDebtRelationship]
    components: List[ComponentRelationship]
    relatedAdrs: List[ADRRelationship]
```

## 4. UI-Spezifikation

### 4.1 Seitenstruktur

1. **Home/Dashboard**
   - Übersicht über alle Entitäten
   - Schnellzugriff auf häufige Aktionen
   - Statusübersicht

2. **ADR-Verwaltung**
   - Liste aller ADRs mit Filter/Suche
   - Formular für neue ADRs
   - Detailansicht mit Bearbeitungsmöglichkeit

3. **Qualitätsanforderungen**
   - Analog zu ADR-Verwaltung

4. **Risiken**
   - Analog zu ADR-Verwaltung
   - Risikomatrix-Visualisierung

5. **Technische Schulden**
   - Analog zu ADR-Verwaltung
   - Priorisierungsansicht

6. **Komponenten**
   - Analog zu ADR-Verwaltung
   - Schnittstellenübersicht

7. **Beziehungen**
   - Beziehungsmatrix
   - Beziehungsgraph (optional)

8. **Export**
   - Export-Konfiguration
   - Download-Bereich

### 4.2 UI-Komponenten

#### Formulare
- Dynamische Formulare basierend auf JSON-Schema
- Inline-Validierung
- Autovervollständigung für Referenzen

#### Listen
- Sortierbar und filterbar
- Pagination bei großen Datenmengen
- Inline-Aktionen (Edit, Delete)

#### Visualisierungen
- Streamlit-Tabellen für Matrizen
- Streamlit-Charts für Statistiken
- Optional: NetworkX für Graphen

## 5. Implementierungsplan

### Phase 1: Grundstruktur (2 Tage)
- Projekt-Setup
- Basis-API mit FastAPI
- Datenmodelle und Repository
- JSON-Schema-Validierung

### Phase 2: CRUD-Funktionalität (2 Tage)
- API-Endpunkte für alle Entitäten
- Streamlit-UI Grundstruktur
- Formulare und Listen

### Phase 3: Beziehungsverwaltung (1 Tag)
- Beziehungs-Endpunkte
- UI für Beziehungsverwaltung
- Konsistenzprüfungen

### Phase 4: Export-Funktionalität (1 Tag)
- AsciiDoc-Generator
- Jinja2-Templates
- Export-API und UI

### Phase 5: Finalisierung (1 Tag)
- Tests
- Dokumentation
- Docker-Setup
- README

## 6. Qualitätssicherung

### 6.1 Testing
- Unit Tests für alle Services
- Integration Tests für API
- UI Tests (manuell)
- Schema-Validierungstests

### 6.2 Code-Qualität
- Type Hints überall
- Docstrings für alle Funktionen
- PEP 8 Compliance
- Code Reviews

### 6.3 Dokumentation
- API-Dokumentation (automatisch via FastAPI)
- Benutzerhandbuch
- Entwicklerdokumentation
- Inline-Code-Kommentare

## 7. Deployment

### 7.1 Lokale Installation
```bash
# Virtuelle Umgebung
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# FastAPI starten
uvicorn src.api.main:app --reload

# Streamlit starten
streamlit run src/ui/app.py
```

### 7.2 Docker Deployment
```bash
# Build und Start
docker-compose up --build

# Zugriff
# API: http://localhost:8000
# UI: http://localhost:8501
```

## 8. Erweiterungsmöglichkeiten

1. **Datenbank-Integration**
   - Migration zu SQLite/PostgreSQL
   - ORM-Integration (SQLAlchemy)

2. **Erweiterte Visualisierungen**
   - D3.js Integration
   - Interaktive Graphen
   - Timeline-Ansichten

3. **Kollaboration**
   - Benutzerauthentifizierung
   - Versionierung
   - Kommentare

4. **Import/Export**
   - Excel-Import/Export
   - Confluence-Integration
   - Git-Integration

5. **Erweiterte Validierung**
   - Benutzerdefinierte Validierungsregeln
   - Architektur-Compliance-Checks
   - Automatische Vorschläge
