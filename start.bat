@echo off
REM Start the Architecture CRUD Application with data

echo Starting Architecture CRUD Application...
echo.

REM Initialize data
echo Initializing example data...
python initialize_data.py
echo.

REM Start API in new window
echo Starting API server on http://localhost:8082...
start "API Server" cmd /k python run_api_with_data.py

REM Wait a bit for API to start
timeout /t 3 /nobreak > nul

REM Start UI in new window
echo Starting UI on http://localhost:8501...
echo.
start "Streamlit UI" cmd /k streamlit run src/ui/app.py

echo.
echo Both servers started in separate windows.
echo Close the windows to stop the servers.
pause
