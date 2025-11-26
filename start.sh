#!/bin/bash

# Clinical Trials Safety Tables - Ultimate Launcher
# This script handles all edge cases and starts the application

clear

echo "🧬 Clinical Trials Safety Tables Generator"
echo "==========================================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Verify virtual environment
if [ ! -f ".venv/bin/python" ]; then
    echo "❌ Virtual environment not found at .venv/"
    echo "💡 Please run: python3 -m venv .venv"
    exit 1
fi

echo "✅ Virtual environment found"

# Check and install dependencies
echo "🔍 Checking dependencies..."
.venv/bin/python -c "import flask, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required packages..."
    .venv/bin/pip install flask pandas numpy python-dateutil -q
fi

echo "✅ Dependencies ready"

# Generate data if needed
if [ ! -d "data" ]; then
    echo "📊 Generating sample clinical trial data..."
    .venv/bin/python data_generator.py
    echo "✅ Sample data created"
fi

# Kill any existing processes on port 8080
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8080 is in use. Attempting to free it..."
    lsof -ti :8080 | xargs kill -9 2>/dev/null
    sleep 1
fi

echo "✅ Port 8080 is available"
echo ""
echo "🚀 Starting Flask application..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Access your application at:"
echo "   🌐 http://localhost:8080"
echo "   🌐 http://127.0.0.1:8080"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start the application
.venv/bin/python launch.py

# Cleanup on exit
echo ""
echo "🛑 Application stopped"
echo "👋 Goodbye!"
