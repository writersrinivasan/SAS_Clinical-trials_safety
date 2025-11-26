#!/usr/bin/env python3
"""
Simple direct launcher for the Clinical Trials app
"""

import os
import sys

# Ensure we're in the right directory
os.chdir('/Users/srinivasanramanujam/Documents/AgenticAI/ClinicalTrials-sas')
sys.path.insert(0, os.getcwd())

print("🧬 Clinical Trials Safety Tables Generator")
print("=" * 60)
print()

# Check data directory
if not os.path.exists('data'):
    print("📊 Generating sample data first...")
    from data_generator import generate_sample_data
    generate_sample_data()
    print()

# Import and run Flask app
try:
    from flask import Flask, render_template, request, jsonify
    from table_generator import TableGenerator
    
    print("✅ Imports successful")
    print("✅ Starting Flask application...")
    print()
    print("📍 Access the application at:")
    print("   → http://localhost:8080")
    print("   → http://127.0.0.1:8080")
    print()
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Create Flask app
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/tables')
    def get_available_tables():
        tables = {
            'adverse_events': 'Adverse Events Summary',
            'demographics': 'Demographics Table', 
            'vital_signs': 'Vital Signs Summary',
            'laboratory': 'Laboratory Values Summary',
            'concomitant_meds': 'Concomitant Medications',
            'disposition': 'Subject Disposition'
        }
        return jsonify(tables)
    
    @app.route('/api/datasets')
    def get_datasets():
        datasets = {
            'demographics': 'Subject demographics and baseline characteristics',
            'adverse_events': 'Adverse events data',
            'vital_signs': 'Vital signs measurements',
            'laboratory': 'Laboratory test results',
            'concomitant_medications': 'Concomitant medications',
            'disposition': 'Subject disposition and study completion'
        }
        return jsonify(datasets)
    
    @app.route('/api/generate_table', methods=['POST'])
    def generate_table():
        try:
            data = request.get_json()
            table_type = data.get('table_type')
            filters = data.get('filters', {})
            
            generator = TableGenerator()
            
            if table_type == 'adverse_events':
                result = generator.generate_adverse_events_table(filters)
            elif table_type == 'demographics':
                result = generator.generate_demographics_table(filters)
            elif table_type == 'vital_signs':
                result = generator.generate_vital_signs_table(filters)
            elif table_type == 'laboratory':
                result = generator.generate_laboratory_table(filters)
            elif table_type == 'concomitant_meds':
                result = generator.generate_conmed_table(filters)
            elif table_type == 'disposition':
                result = generator.generate_disposition_table(filters)
            else:
                return jsonify({'error': 'Invalid table type'}), 400
                
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Start the server
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
    
except KeyboardInterrupt:
    print("\n\n🛑 Application stopped by user")
    print("👋 Goodbye!")
    
except Exception as e:
    print(f"\n❌ Error starting application: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 Troubleshooting tips:")
    print("   1. Check if port 8080 is already in use")
    print("   2. Try: lsof -i :8080")
    print("   3. Run the demo instead: .venv/bin/python demo.py")
    sys.exit(1)
