#!/usr/bin/env python3

"""
Simple test server for Clinical Trials Safety Tables
"""

from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Main page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clinical Trials Safety Tables - Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .button { background: #007cba; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
            .button:hover { background: #005a87; }
            #result { background: #f8f8f8; padding: 15px; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧬 Clinical Trials Safety Tables Generator</h1>
            
            <div class="status">
                ✅ <strong>Application Status:</strong> Running successfully on port 8080<br>
                📊 <strong>Sample Data:</strong> 150 subjects across 3 treatment groups<br>
                🎯 <strong>Available Tables:</strong> 6 table types ready to generate
            </div>
            
            <h2>Quick Test</h2>
            <button class="button" onclick="testAPI()">🔬 Test Table Generation</button>
            <button class="button" onclick="testData()">📊 Check Sample Data</button>
            <button class="button" onclick="openFullApp()">🚀 Open Full Application</button>
            
            <div id="result"></div>
            
            <h2>Next Steps</h2>
            <p><strong>1. Full Application:</strong> Click "Open Full Application" above to access the complete interface</p>
            <p><strong>2. Table Types Available:</strong></p>
            <ul>
                <li>Adverse Events Summary</li>
                <li>Demographics Table</li>
                <li>Vital Signs Summary</li>
                <li>Laboratory Values</li>
                <li>Concomitant Medications</li>
                <li>Subject Disposition</li>
            </ul>
        </div>
        
        <script>
            function testAPI() {
                document.getElementById('result').innerHTML = '<p>🔄 Testing API...</p>';
                fetch('/api/tables')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('result').innerHTML = 
                            '<h3>✅ API Test Successful!</h3>' +
                            '<p><strong>Available Tables:</strong></p>' +
                            '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    })
                    .catch(error => {
                        document.getElementById('result').innerHTML = 
                            '<h3>❌ API Test Failed</h3><p>' + error + '</p>';
                    });
            }
            
            function testData() {
                document.getElementById('result').innerHTML = '<p>🔄 Checking data files...</p>';
                fetch('/api/datasets')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('result').innerHTML = 
                            '<h3>✅ Data Files Found!</h3>' +
                            '<p><strong>Available Datasets:</strong></p>' +
                            '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    })
                    .catch(error => {
                        document.getElementById('result').innerHTML = 
                            '<h3>❌ Data Check Failed</h3><p>' + error + '</p>';
                    });
            }
            
            function openFullApp() {
                window.location.href = '/app';
            }
        </script>
    </body>
    </html>
    '''

@app.route('/app')
def full_app():
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

@app.route('/api/datasets')
def get_datasets():
    """Get information about available datasets"""
    # Check if data files exist
    data_files = {
        'demographics': 'data/demographics.csv',
        'adverse_events': 'data/adverse_events.csv',
        'vital_signs': 'data/vital_signs.csv',
        'laboratory': 'data/laboratory.csv',
        'concomitant_medications': 'data/concomitant_medications.csv',
        'disposition': 'data/disposition.csv'
    }
    
    status = {}
    for name, file_path in data_files.items():
        status[name] = {
            'file': file_path,
            'exists': os.path.exists(file_path),
            'description': f'{name.replace("_", " ").title()} dataset'
        }
    
    return jsonify(status)

@app.route('/api/generate_table', methods=['POST'])
def generate_table():
    """Generate the requested table"""
    try:
        from table_generator import TableGenerator
        
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

if __name__ == '__main__':
    print("🧬 Starting Clinical Trials Safety Tables Generator...")
    print(f"🌐 Access at: http://localhost:8080")
    print(f"🔬 Test page: http://localhost:8080")
    print(f"🚀 Full app: http://localhost:8080/app")
    print("🛑 Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
