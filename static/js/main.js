// Clinical Trials Safety Tables - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

async function initializeApp() {
    // Load available table types
    await loadTableTypes();
    
    // Set up event listeners
    setupEventListeners();
    
    // Generate sample data on first load
    console.log('Clinical Trials Safety Tables app initialized');
}

async function loadTableTypes() {
    try {
        const response = await fetch('/api/tables');
        const tables = await response.json();
        
        const tableTypeSelect = document.getElementById('tableType');
        tableTypeSelect.innerHTML = '<option value="">Select a table type...</option>';
        
        for (const [key, value] of Object.entries(tables)) {
            const option = document.createElement('option');
            option.value = key;
            option.textContent = value;
            tableTypeSelect.appendChild(option);
        }
    } catch (error) {
        console.error('Error loading table types:', error);
        showError('Failed to load available table types');
    }
}

function setupEventListeners() {
    // Generate table button
    document.getElementById('generateTable').addEventListener('click', generateTable);
    
    // Clear filters button
    document.getElementById('clearFilters').addEventListener('click', clearFilters);
    
    // Export buttons
    document.getElementById('exportHTML').addEventListener('click', exportHTML);
    document.getElementById('exportCSV').addEventListener('click', exportCSV);
    document.getElementById('printTable').addEventListener('click', printTable);
    
    // Table type change
    document.getElementById('tableType').addEventListener('change', function() {
        const generateBtn = document.getElementById('generateTable');
        if (this.value) {
            generateBtn.disabled = false;
            generateBtn.style.opacity = '1';
        } else {
            generateBtn.disabled = true;
            generateBtn.style.opacity = '0.6';
        }
    });
}

async function generateTable() {
    const tableType = document.getElementById('tableType').value;
    
    if (!tableType) {
        showError('Please select a table type');
        return;
    }
    
    // Collect filters
    const filters = collectFilters();
    
    // Show loading spinner
    showLoading();
    
    try {
        const response = await fetch('/api/generate_table', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                table_type: tableType,
                filters: filters
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.error) {
            throw new Error(result.error);
        }
        
        // Display the generated table
        displayTable(result);
        
        // Show export options
        document.getElementById('exportOptions').style.display = 'flex';
        
    } catch (error) {
        console.error('Error generating table:', error);
        showError(`Failed to generate table: ${error.message}`);
    } finally {
        hideLoading();
    }
}

function collectFilters() {
    const filters = {};
    
    // Treatment filter
    const treatmentFilter = document.getElementById('treatmentFilter');
    const selectedTreatments = Array.from(treatmentFilter.selectedOptions).map(option => option.value);
    if (selectedTreatments.length > 0) {
        filters.treatment = selectedTreatments;
    }
    
    // Gender filter
    const genderFilter = document.getElementById('genderFilter');
    const selectedGenders = Array.from(genderFilter.selectedOptions).map(option => option.value);
    if (selectedGenders.length > 0) {
        filters.sex = selectedGenders;
    }
    
    // Age range filter
    const ageMin = document.getElementById('ageMinFilter').value;
    const ageMax = document.getElementById('ageMaxFilter').value;
    
    if (ageMin) {
        filters.age_min = parseInt(ageMin);
    }
    
    if (ageMax) {
        filters.age_max = parseInt(ageMax);
    }
    
    return filters;
}

function clearFilters() {
    document.getElementById('treatmentFilter').selectedIndex = -1;
    document.getElementById('genderFilter').selectedIndex = -1;
    document.getElementById('ageMinFilter').value = '';
    document.getElementById('ageMaxFilter').value = '';
    
    // Reset multi-select highlighting
    const multiSelects = document.querySelectorAll('select[multiple]');
    multiSelects.forEach(select => {
        Array.from(select.options).forEach(option => {
            option.selected = false;
        });
    });
    
    showMessage('Filters cleared', 'info');
}

function displayTable(result) {
    const tableContainer = document.getElementById('tableContainer');
    
    let html = '';
    
    // Add summary information
    if (result.summary) {
        html += `
            <div class="table-summary">
                <div class="summary-info">
                    <i class="fas fa-info-circle"></i>
                    <span>${result.summary}</span>
                </div>
            </div>
        `;
    }
    
    // Add the table HTML
    if (result.table_html) {
        html += result.table_html;
    }
    
    // Add additional metadata if available
    if (result.total_subjects) {
        html += `
            <div class="metadata">
                <h4>Study Population:</h4>
                <ul>
        `;
        
        for (const [treatment, count] of Object.entries(result.total_subjects)) {
            html += `<li><strong>${treatment}:</strong> ${count} subjects</li>`;
        }
        
        html += `
                </ul>
            </div>
        `;
    }
    
    tableContainer.innerHTML = html;
    
    // Store data for export
    window.currentTableData = result;
}

function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'flex';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('tableContainer').innerHTML = '';
    document.getElementById('exportOptions').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

function showError(message) {
    document.getElementById('errorText').textContent = message;
    document.getElementById('errorMessage').style.display = 'block';
    document.getElementById('tableContainer').innerHTML = '';
    document.getElementById('exportOptions').style.display = 'none';
}

function showMessage(message, type = 'success') {
    // Create and show a temporary message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#48bb78' : '#4299e1'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 300);
    }, 3000);
}

function exportHTML() {
    if (!window.currentTableData || !window.currentTableData.table_html) {
        showError('No table data available to export');
        return;
    }
    
    const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Trial Table Export</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 20px; 
            color: #333; 
        }
        .clinical-table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 20px; 
        }
        .clinical-table th { 
            background: #4a5568; 
            color: white; 
            padding: 12px; 
            text-align: left; 
        }
        .clinical-table td { 
            padding: 10px; 
            border-bottom: 1px solid #e2e8f0; 
        }
        .clinical-table tr:nth-child(even) { 
            background: #f7fafc; 
        }
        .table-title { 
            color: #4a5568; 
            font-size: 1.5em; 
            margin-bottom: 8px; 
        }
        .table-subtitle { 
            color: #718096; 
            margin-bottom: 20px; 
            font-style: italic; 
        }
        .export-info { 
            margin-bottom: 20px; 
            padding: 15px; 
            background: #f0f9ff; 
            border-left: 4px solid #0ea5e9; 
        }
    </style>
</head>
<body>
    <div class="export-info">
        <strong>Export Information:</strong><br>
        Generated on: ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString()}<br>
        Table Type: ${document.getElementById('tableType').selectedOptions[0].text}<br>
        Source: Clinical Trials Safety Tables Generator
    </div>
    
    ${window.currentTableData.table_html}
</body>
</html>
    `;
    
    downloadFile(html, 'clinical_table_export.html', 'text/html');
    showMessage('HTML table exported successfully');
}

function exportCSV() {
    if (!window.currentTableData || !window.currentTableData.data) {
        showError('No table data available to export');
        return;
    }
    
    const data = window.currentTableData.data;
    
    if (data.length === 0) {
        showError('No data to export');
        return;
    }
    
    // Get headers
    const headers = Object.keys(data[0]);
    
    // Create CSV content
    let csv = headers.join(',') + '\n';
    
    data.forEach(row => {
        const values = headers.map(header => {
            const value = row[header];
            // Escape quotes and wrap in quotes if needed
            if (typeof value === 'string' && (value.includes(',') || value.includes('"') || value.includes('\n'))) {
                return '"' + value.replace(/"/g, '""') + '"';
            }
            return value;
        });
        csv += values.join(',') + '\n';
    });
    
    downloadFile(csv, 'clinical_table_export.csv', 'text/csv');
    showMessage('CSV data exported successfully');
}

function printTable() {
    window.print();
}

function downloadFile(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// CSS animations for messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .table-summary {
        background: #e6fffa;
        border: 1px solid #38b2ac;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .summary-info {
        color: #2c7a7b;
        font-weight: 500;
    }
    
    .summary-info i {
        margin-right: 8px;
        color: #38b2ac;
    }
    
    .metadata {
        margin-top: 25px;
        padding: 20px;
        background: #f7fafc;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    .metadata h4 {
        color: #4a5568;
        margin-bottom: 15px;
        font-size: 1.1em;
    }
    
    .metadata ul {
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    .metadata li {
        padding: 5px 0;
        color: #718096;
    }
    
    .metadata li strong {
        color: #4a5568;
    }
`;
document.head.appendChild(style);
