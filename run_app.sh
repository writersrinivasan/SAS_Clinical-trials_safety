#!/bin/bash

# Clinical Trials Safety Tables - Direct Start Script

clear
echo "🧬 Clinical Trials Safety Tables Generator"
echo "=========================================="
echo ""

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    exit 1
fi

echo "✅ Virtual environment found"

# Check data directory
if [ ! -d "data" ]; then
    echo "📊 Generating sample data..."
    .venv/bin/python data_generator.py
fi

echo "✅ Sample data ready"

# Start application
echo ""
echo "🚀 Starting application on port 8080..."
echo "📍 Access at: http://localhost:8080"
echo "🔬 Test page: http://localhost:8080"
echo "🚀 Full app: http://localhost:8080/app"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"
echo ""

# Run the application
.venv/bin/python -c "
import sys
sys.path.append('.')
from app import app

print('🧬 Flask application starting...')
print('📍 URL: http://localhost:8080')
print('🛑 Press Ctrl+C to stop')
print()

try:
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
except KeyboardInterrupt:
    print('\\n🛑 Application stopped by user')
except Exception as e:
    print(f'❌ Error: {e}')
    print('💡 Try: .venv/bin/python test_app.py')
"
