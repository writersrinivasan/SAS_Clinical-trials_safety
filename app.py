from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json
from data_generator import generate_sample_data
from table_generator import TableGenerator

app = Flask(__name__)

# Initialize sample data
generate_sample_data()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/tables')
def get_available_tables():
    """Get list of available table types"""
    tables = {
        'adverse_events': 'Adverse Events Summary',
        'demographics': 'Demographics Table', 
        'vital_signs': 'Vital Signs Summary',
        'laboratory': 'Laboratory Values Summary',
        'concomitant_meds': 'Concomitant Medications',
        'disposition': 'Subject Disposition'
    }
    return jsonify(tables)

@app.route('/api/generate_table', methods=['POST'])
def generate_table():
    """Generate the requested table"""
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

@app.route('/api/datasets')
def get_datasets():
    """Get information about available datasets"""
    datasets = {
        'demographics': 'Subject demographics and baseline characteristics',
        'adverse_events': 'Adverse events data',
        'vital_signs': 'Vital signs measurements',
        'laboratory': 'Laboratory test results',
        'concomitant_medications': 'Concomitant medications',
        'disposition': 'Subject disposition and study completion'
    }
    return jsonify(datasets)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
