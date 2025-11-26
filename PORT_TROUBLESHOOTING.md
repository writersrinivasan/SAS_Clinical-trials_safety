# 🔧 Port Issue Resolution Guide

## Problem Diagnosis

The Flask application is not starting properly on the expected ports. Here are multiple solutions to get your Clinical Trials Safety Tables application running.

## ✅ Solution 1: Manual Start (Recommended)

Open a new terminal and run:

```bash
cd /Users/srinivasanramanujam/Documents/AgenticAI/ClinicalTrials-sas

# Activate virtual environment and start app
source .venv/bin/activate
python app.py
```

The application will start on **http://localhost:8080**

## ✅ Solution 2: Test Application

Use the simplified test version:

```bash
# Start the test app
.venv/bin/python test_app.py

# Then open browser to:
# http://localhost:8080
```

## ✅ Solution 3: Different Port

If port 8080 is still blocked, try a different port:

```bash
# Edit app.py to change port to 9000
sed -i '' 's/port=8080/port=9000/g' app.py

# Start application
.venv/bin/python app.py

# Access at: http://localhost:9000
```

## ✅ Solution 4: Use Python HTTP Server (Emergency)

If Flask has issues, use built-in Python server for static testing:

```bash
# Generate a static HTML table for testing
.venv/bin/python -c "
from table_generator import TableGenerator
generator = TableGenerator()
result = generator.generate_adverse_events_table()
with open('test_table.html', 'w') as f:
    f.write('<html><body>' + result['table_html'] + '</body></html>')
print('Static test file created: test_table.html')
"

# Start simple HTTP server
.venv/bin/python -m http.server 9090

# Open: http://localhost:9090/test_table.html
```

## 🔍 Troubleshooting Steps

### Step 1: Check What's Using Ports

```bash
# Check port usage
lsof -i :5000 -i :8080 -i :9000

# Kill processes if needed
pkill -f python
```

### Step 2: Verify Installation

```bash
# Test basic functionality
.venv/bin/python demo.py

# Check setup
.venv/bin/python test_setup.py
```

### Step 3: Check Flask Installation

```bash
# Verify Flask works
.venv/bin/python -c "
import flask
print('Flask version:', flask.__version__)
from app import app
print('App created successfully')
"
```

## 🚀 Quick Start Commands

Choose any of these methods:

### Method A: Background Process
```bash
nohup .venv/bin/python app.py > flask.log 2>&1 &
echo "Check http://localhost:8080"
tail -f flask.log
```

### Method B: Direct Run
```bash
.venv/bin/python app.py
```

### Method C: Flask CLI
```bash
export FLASK_APP=app.py
.venv/bin/flask run --host=0.0.0.0 --port=8080
```

### Method D: Test Version
```bash
.venv/bin/python test_app.py
```

## 📱 Access URLs

Once running, try these URLs:

- **Main Test Page**: http://localhost:8080
- **Full Application**: http://localhost:8080/app  
- **API Test**: http://localhost:8080/api/tables
- **Alternative Ports**: http://localhost:9000 or http://localhost:5000

## 🔧 Port Configuration

The application is configured to run on:
- **Primary**: Port 8080 
- **Backup**: Port 9000
- **Original**: Port 5000 (if available)

## ⚡ Instant Test

Run this one-liner to test everything:

```bash
.venv/bin/python -c "
import subprocess, time, webbrowser
print('🧬 Starting Clinical Trials App...')
proc = subprocess.Popen(['.venv/bin/python', 'test_app.py'])
time.sleep(3)
print('✅ Opening browser...')
webbrowser.open('http://localhost:8080')
print('📊 Application should be running!')
"
```

## 🆘 If Nothing Works

1. **Restart VS Code** and try again
2. **Check firewall settings** - allow Python to access network
3. **Use different terminal** - try Terminal.app instead of VS Code terminal
4. **Check system ports** - something might be blocking Flask

## ✅ Success Indicators

You'll know it's working when you see:

```
🧬 Starting Clinical Trials Safety Tables Generator...
🌐 Access at: http://localhost:8080
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:8080
* Running on http://[::]:8080
```

## 📞 Emergency Backup

If all else fails, the table generation still works via command line:

```bash
# Generate tables without web interface
.venv/bin/python demo.py

# This proves your core functionality works!
```

---

**Choose the method that works best for your setup. The application is ready to go! 🎉**
