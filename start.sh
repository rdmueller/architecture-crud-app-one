#!/bin/bash
# Start the Architecture CRUD Application with data

echo "🚀 Starting Architecture CRUD Application..."
echo ""

# Initialize data
echo "📦 Initializing example data..."
python initialize_data.py
echo ""

# Start API in background
echo "🔧 Starting API server on http://localhost:8082..."
python run_api_with_data.py &
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
