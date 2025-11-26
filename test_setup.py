#!/usr/bin/env python3

"""
Quick test to verify the application setup
"""

import os
import sys
import subprocess

def test_setup():
    print("🧬 Clinical Trials Safety Tables - Setup Test")
    print("=" * 60)
    
    # Check virtual environment
    venv_python = ".venv/bin/python"
    if os.path.exists(venv_python):
        print("✅ Virtual environment found")
    else:
        print("❌ Virtual environment not found")
        return False
    
    # Check required packages
    try:
        result = subprocess.run([venv_python, "-c", "import pandas, flask, numpy"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Required packages installed")
        else:
            print("❌ Missing packages:", result.stderr)
            return False
    except Exception as e:
        print("❌ Error checking packages:", e)
        return False
    
    # Check data files
    data_dir = "data"
    required_files = [
        "demographics.csv",
        "adverse_events.csv", 
        "vital_signs.csv",
        "laboratory.csv",
        "concomitant_medications.csv",
        "disposition.csv"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(data_dir, file)):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing data files: {missing_files}")
        print("   Run: .venv/bin/python data_generator.py")
        return False
    else:
        print("✅ All data files present")
    
    # Test table generation
    try:
        result = subprocess.run([venv_python, "demo.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Table generation works")
        else:
            print("❌ Table generation failed:", result.stderr)
            return False
    except Exception as e:
        print("❌ Error testing table generation:", e)
        return False
    
    print("\n🎉 All tests passed!")
    print("\n🚀 To start the application:")
    print("   Option 1: ./start_app.sh")
    print("   Option 2: .venv/bin/python app.py")
    print("   Option 3: .venv/bin/python test_app.py")
    print("\n📍 Application will be available at:")
    print("   http://localhost:8080")
    
    return True

if __name__ == "__main__":
    test_setup()
