# Architecture CRUD Application - Installation Guide

Diese Anleitung beschreibt die Installation und Konfiguration der Architecture CRUD Application.

## Inhaltsverzeichnis

1. [Voraussetzungen](#voraussetzungen)
2. [Installation](#installation)
3. [Konfiguration](#konfiguration)
4. [Starten der Anwendung](#starten-der-anwendung)
5. [Dateninitialisierung](#dateninitialisierung)
6. [Fehlerbehebung](#fehlerbehebung)
7. [Docker-Installation](#docker-installation)

## Voraussetzungen

- Python 3.10 oder höher
- pip (Python Package Manager)
- git (für das Klonen des Repositories)
- Internetverbindung für das Herunterladen der Abhängigkeiten

## Installation

### 1. Repository klonen

```bash
git clone <repository-url>
cd architecture-crud-app
```

### 2. Virtuelle Umgebung erstellen und aktivieren

**Linux/macOS**:
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Testabhängigkeiten installieren (optional)

```bash
pip install -r requirements-test.txt
```

## Konfiguration

Die Anwendung kann über Umgebungsvariablen konfiguriert werden:

### Umgebungsvariablen

| Variable | Beschreibung | Standardwert |
|----------|--------------|--------------|
| `ARCHITECTURE_DATA_FILE` | Pfad zur Datendatei | `data/architecture.json` |
| `API_PORT` | Port für den API-Server | `8082` |
| `STREAMLIT_SERVER_PORT` | Port für den Streamlit-Server | `8501` |

### Beispiel für die Konfiguration

**Linux/macOS**:
```bash
export ARCHITECTURE_DATA_FILE=$(pwd)/data/architecture.json
export API_PORT=8082
export STREAMLIT_SERVER_PORT=8501
```

**Windows**:
```bash
set ARCHITECTURE_DATA_FILE=%cd%\data\architecture.json
set API_PORT=8082
set STREAMLIT_SERVER_PORT=8501
```

## Starten der Anwendung

### Schnellstart

Verwenden Sie das mitgelieferte Start-Skript:

```bash
./final_restart.sh  # Linux/macOS
```

oder

```bash
start.bat  # Windows
```

### Manueller Start

#### 1. API-Server starten

```bash
python run_api_simple.py
```

Der API-Server ist dann unter `http://localhost:8082` verfügbar.

#### 2. UI-Server starten

In einem separaten Terminal:

```bash
streamlit run src/ui/app.py
```

Die UI ist dann unter `http://localhost:8501` verfügbar.

## Dateninitialisierung

### Beispieldaten initialisieren

```bash
python initialize_data.py
```

### Daten zurücksetzen

```bash
python use_fixed_data.py
```

### Daten erzwungen zurücksetzen

```bash
python force_reset_data.py
```

## Fehlerbehebung

Wenn Probleme auftreten, können Sie die folgenden Schritte ausführen:

### 1. Diagnose-Tools verwenden

```bash
python fix_api_debug.py  # API-Diagnose
python fix_data_loading.py  # Daten-Diagnose
python fix_environment.py  # Umgebungs-Diagnose
```

### 2. Anwendung mit Debug-Ausgaben starten

```bash
./debug_restart.sh
```

### 3. Modelle und Daten korrigieren

```bash
python fix_models.py  # Modelle anpassen
python fix_relationship_models.py  # Beziehungsmodelle anpassen
python fix_example_data.py  # Beispieldaten korrigieren
python use_fixed_data.py  # Korrigierte Daten verwenden
```

Weitere Informationen finden Sie in der [Fehlerbehebungsanleitung](TROUBLESHOOTING.md).

## Docker-Installation

### Voraussetzungen

- Docker
- Docker Compose

### 1. Docker-Images erstellen

```bash
docker-compose build
```

### 2. Container starten

```bash
docker-compose up -d
```

### 3. Container-Status überprüfen

```bash
docker-compose ps
```

### 4. Logs anzeigen

```bash
docker-compose logs -f
```

### 5. Container stoppen

```bash
docker-compose down
```

## Testen der Installation

### API-Tests ausführen

```bash
pytest tests/api tests/data
```

### UI-Tests ausführen

```bash
python run_ui_tests_simple.py
```

### Integrationstests ausführen

```bash
python run_integration_tests.py --simple
```

## Nächste Schritte

Nach erfolgreicher Installation können Sie:

1. Die [Benutzerdokumentation](README.md) lesen
2. Die [API-Dokumentation](http://localhost:8082/docs) aufrufen
3. Die [Fehlerbehebungsanleitung](TROUBLESHOOTING.md) für Probleme konsultieren
4. Die [Entwicklerdokumentation](arc42/architecture-documentation.adoc) für technische Details lesen
