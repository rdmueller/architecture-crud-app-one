#!/bin/bash
# Restart the Architecture CRUD Application with fixed data

echo "🔄 Restarting Architecture CRUD Application..."
echo ""

# Kill existing processes
echo "Stopping existing processes..."
pkill -f "python.*run_api_simple.py" || true
pkill -f "streamlit run src/ui/app.py" || true

# Wait for processes to stop
sleep 2

# Initialize data
echo "📦 Initializing example data..."
python3 force_reset_data.py
echo ""

# Start API in background
echo "🔧 Starting API server on http://localhost:8082..."
python3 run_api_simple.py &
API_PID=$!

# Wait a bit for API to start
sleep 3

# Start UI
echo "🎨 Starting UI on http://localhost:8501..."
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Trap Ctrl+C and kill both processes
trap 'kill $API_PID; exit' INT

# Start UI (this will block until Ctrl+C)
streamlit run src/ui/app.py
