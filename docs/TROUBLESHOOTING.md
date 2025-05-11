# Architecture CRUD Application - Troubleshooting Guide

Diese Anleitung hilft bei der Behebung häufiger Probleme mit der Architecture CRUD Application.

## Inhaltsverzeichnis

1. [Startprobleme](#startprobleme)
2. [Datenprobleme](#datenprobleme)
3. [API-Probleme](#api-probleme)
4. [UI-Probleme](#ui-probleme)
5. [Diagnose-Tools](#diagnose-tools)
6. [Häufige Fehlermeldungen](#häufige-fehlermeldungen)

## Startprobleme

### Die Anwendung startet nicht

**Symptom**: Beim Ausführen von `./start.sh` erscheint eine Fehlermeldung.

**Mögliche Lösungen**:

1. **Multiprocessing-Fehler**:
   ```
   RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase.
   ```
   
   Lösung: Verwenden Sie das stabilere Start-Skript:
   ```bash
   ./final_restart.sh
   ```

2. **Port bereits in Verwendung**:
   ```
   OSError: [Errno 98] Address already in use
   ```
   
   Lösung: Beenden Sie alle laufenden Prozesse und starten Sie neu:
   ```bash
   pkill -f "python.*run_api" || true
   pkill -f "streamlit run src/ui/app.py" || true
   ./final_restart.sh
   ```

3. **Python-Module fehlen**:
   ```
   ModuleNotFoundError: No module named 'uvicorn'
   ```
   
   Lösung: Aktivieren Sie die virtuelle Umgebung und installieren Sie die Abhängigkeiten:
   ```bash
   source .venv/bin/activate  # oder venv/bin/activate
   pip install -r requirements.txt
   ```

## Datenprobleme

### Keine Daten im Dashboard

**Symptom**: Das Dashboard zeigt keine Daten an, obwohl die Anwendung startet.

**Mögliche Lösungen**:

1. **Daten zurücksetzen**:
   ```bash
   python3 use_fixed_data.py
   ./final_restart.sh
   ```

2. **Datenformat überprüfen**:
   ```bash
   python3 fix_api_debug.py
   ```
   
   Dieses Skript zeigt an, welche Daten die API tatsächlich zurückgibt.

3. **Validierungsfehler beheben**:
   ```bash
   python3 fix_remaining_errors.py
   ./final_restart.sh
   ```

### Validierungsfehler

**Symptom**: In den Logs erscheinen Validierungsfehler wie:
```
Error loading architecture: X validation errors for Architecture
```

**Mögliche Lösungen**:

1. **Modelle anpassen**:
   ```bash
   python3 fix_models.py
   python3 fix_relationship_models.py
   ./final_restart.sh
   ```

2. **Daten korrigieren**:
   ```bash
   python3 fix_example_data.py
   python3 use_fixed_data.py
   ./final_restart.sh
   ```

## API-Probleme

### API gibt leere Daten zurück

**Symptom**: Die API-Endpunkte geben leere Listen oder Objekte zurück.

**Mögliche Lösungen**:

1. **API-Routen debuggen**:
   ```bash
   python3 fix_api_debug.py
   ```

2. **API-Routen korrigieren**:
   ```bash
   python3 fix_api_routes.py
   ./final_restart.sh
   ```

3. **Umgebungsvariablen überprüfen**:
   ```bash
   python3 fix_environment.py
   ```

### API-Endpunkte nicht erreichbar

**Symptom**: Die API-Endpunkte sind nicht erreichbar oder geben 404 zurück.

**Mögliche Lösungen**:

1. **API-Server-Status überprüfen**:
   ```bash
   curl -s http://localhost:8082/health
   ```

2. **API mit explizitem Datei-Pfad starten**:
   ```bash
   ARCHITECTURE_DATA_FILE=$(pwd)/data/architecture.json python3 run_api_simple.py
   ```

## UI-Probleme

### UI zeigt keine Daten an

**Symptom**: Die UI startet, zeigt aber keine Daten an.

**Mögliche Lösungen**:

1. **API-Client korrigieren**:
   ```bash
   python3 fix_api_client.py
   ```

2. **Dashboard korrigieren**:
   ```bash
   python3 fix_dashboard.py
   ```

3. **Mit Debug-Ausgaben neu starten**:
   ```bash
   ./debug_restart.sh
   ```

### UI-Komponenten funktionieren nicht

**Symptom**: Formulare oder andere UI-Komponenten funktionieren nicht wie erwartet.

**Mögliche Lösungen**:

1. **Cache leeren**:
   ```bash
   rm -rf ~/.streamlit/
   ```

2. **Streamlit neu starten**:
   ```bash
   pkill -f "streamlit run src/ui/app.py" || true
   streamlit run src/ui/app.py
   ```

## Diagnose-Tools

Die Anwendung enthält mehrere Diagnose-Tools, die bei der Fehlerbehebung helfen können:

### API-Diagnose

```bash
python3 fix_api_debug.py
```

Dieses Skript überprüft die API-Endpunkte und zeigt an, welche Daten zurückgegeben werden.

### Daten-Diagnose

```bash
python3 fix_data_loading.py
```

Dieses Skript überprüft die Datendatei und zeigt an, welche Entitäten sie enthält.

### Umgebungs-Diagnose

```bash
python3 fix_environment.py
```

Dieses Skript überprüft die Umgebungsvariablen und zeigt an, welche Werte sie haben.

## Häufige Fehlermeldungen

### Multiprocessing-Fehler

```
RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase.
```

Dieser Fehler tritt auf, wenn Uvicorn's Reload-Funktion mit Python's Multiprocessing-Modul kollidiert. Verwenden Sie `run_api_simple.py` ohne Reload-Funktion.

### Validierungsfehler

```
Error loading architecture: X validation errors for Architecture
```

Dieser Fehler tritt auf, wenn die Daten nicht dem erwarteten Schema entsprechen. Verwenden Sie die Skripte `fix_models.py` und `fix_relationship_models.py`, um die Modelle anzupassen, oder `fix_example_data.py` und `use_fixed_data.py`, um die Daten zu korrigieren.

### Datei-Pfad-Fehler

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/architecture.json'
```

Dieser Fehler tritt auf, wenn die Datendatei nicht gefunden wird. Verwenden Sie absolute Pfade und die Umgebungsvariable `ARCHITECTURE_DATA_FILE`.

## Komplette Neuinstallation

Wenn alle anderen Lösungen fehlschlagen, können Sie die Anwendung komplett neu installieren:

```bash
# Virtuelle Umgebung neu erstellen
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Daten zurücksetzen
python3 force_reset_data.py

# Anwendung starten
./final_restart.sh
```

## Support

Wenn Sie weitere Hilfe benötigen, erstellen Sie bitte ein Issue im GitHub-Repository oder wenden Sie sich an das Entwicklungsteam.
