#!/bin/bash

# Clinical Trials Safety Tables - Startup Script

echo "🧬 Clinical Trials Safety Tables Generator"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "📊 Generating sample clinical trial datasets..."
    .venv/bin/python data_generator.py
    echo "✅ Sample data generated successfully!"
    echo ""
fi

# Start the Flask application
echo "🚀 Starting Clinical Trials Safety Tables web application..."
echo "📍 Access the application at: http://localhost:8080"
echo "🔬 Test page: http://localhost:8080"
echo "🚀 Full app: http://localhost:8080/app"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

.venv/bin/python app.py
