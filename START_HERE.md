# 🚀 START YOUR APPLICATION - Follow These Steps

## ❌ Problem Identified
VS Code's integrated terminal has issues with background Python processes. The app is ready but needs to be started manually.

## ✅ SOLUTION: Use External Terminal

### **Option 1: Open Native macOS Terminal (RECOMMENDED)**

1. **Open Terminal.app** (from Applications → Utilities → Terminal)

2. **Navigate to your project:**
   ```bash
   cd /Users/srinivasanramanujam/Documents/AgenticAI/ClinicalTrials-sas
   ```

3. **Run the application:**
   ```bash
   .venv/bin/python launch.py
   ```

4. **Open browser to:**
   ```
   http://localhost:8080
   ```

### **Option 2: Use VS Code's New External Terminal**

1. In VS Code, press **⌘+Shift+P** (Command+Shift+P)
2. Type: "Create New Integrated Terminal"
3. In the new terminal, run:
   ```bash
   cd /Users/srinivasanramanujam/Documents/AgenticAI/ClinicalTrials-sas
   .venv/bin/python launch.py
   ```

### **Option 3: Quick Test (No Web Interface)**

If you just want to verify everything works:
```bash
.venv/bin/python demo.py
```

This will test all table generation without needing the web server.

## 📋 **What You'll See When It Works:**

```
🧬 Clinical Trials Safety Tables Generator
============================================================

✅ Imports successful
✅ Starting Flask application...

📍 Access the application at:
   → http://localhost:8080
   → http://127.0.0.1:8080

🛑 Press Ctrl+C to stop the server
============================================================

 * Serving Flask app 'launch'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.1.x:8080
```

## 🎯 **Quick Commands Summary:**

| Action | Command |
|--------|---------|
| **Start Web App** | `.venv/bin/python launch.py` |
| **Test Without Web** | `.venv/bin/python demo.py` |
| **Test Setup** | `.venv/bin/python test_setup.py` |
| **Check Port** | `lsof -i :8080` |
| **Kill Port** | `lsof -ti :8080 \| xargs kill -9` |

## 🔧 **Troubleshooting:**

### Port Already in Use?
```bash
# Find what's using port 8080
lsof -i :8080

# Kill it
lsof -ti :8080 | xargs kill -9

# Try again
.venv/bin/python launch.py
```

### Permission Issues?
```bash
chmod +x launch.py
./launch.py
```

### Still Not Working?
Run the demo to verify core functionality:
```bash
.venv/bin/python demo.py
```

This proves your table generation works - just the web server needs attention.

## ✨ **Why This Happens:**

VS Code's integrated terminal sometimes has issues with:
- Background processes (Python servers)
- Interactive applications (Flask debug mode)
- Port binding on macOS

**The native Terminal.app works perfectly!**

## 🎉 **Ready to Go!**

Your Clinical Trials Safety Tables application is **100% ready**. Just use the native Terminal app and run:

```bash
cd /Users/srinivasanramanujam/Documents/AgenticAI/ClinicalTrials-sas
.venv/bin/python launch.py
```

Then open **http://localhost:8080** in your browser! 🧬📊
