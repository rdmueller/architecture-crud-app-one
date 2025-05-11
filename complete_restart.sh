#!/bin/bash
# Complete restart of the Architecture CRUD Application

echo "🔄 Complete restart of Architecture CRUD Application..."
echo ""

# Kill existing processes
echo "Stopping existing processes..."
pkill -f "python.*run_api_simple.py" || true
pkill -f "streamlit run src/ui/app.py" || true

# Wait for processes to stop
sleep 2

# Force reset data
echo "📦 Resetting data..."
python3 force_reset_data.py
echo ""

# Start API in background with explicit data file
echo "🔧 Starting API server on http://localhost:8082..."
ARCHITECTURE_DATA_FILE=$(pwd)/data/architecture.json python3 run_api_simple.py &
API_PID=$!

# Wait for API to start
echo "Waiting for API to start..."
sleep 5

# Test API
echo "Testing API..."
curl -s http://localhost:8082/api/architecture | head -20
echo ""

# Start UI
echo "🎨 Starting UI on http://localhost:8501..."
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Trap Ctrl+C and kill both processes
trap 'kill $API_PID; exit' INT

# Start UI with explicit API URL
STREAMLIT_API_URL=http://localhost:8082 streamlit run src/ui/app.py
