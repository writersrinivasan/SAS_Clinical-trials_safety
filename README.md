# Clinical Trials Safety Tables Generator

A modern web application for generating professional clinical trial safety and efficacy tables, designed for SAS programmers transitioning to web-based solutions.

## Features

### 🎯 **Table Generation**
- **Adverse Events Summary**: Safety overview by treatment group with counts and percentages
- **Demographics Table**: Baseline characteristics and population statistics
- **Vital Signs Summary**: Vital signs measurements by visit and treatment
- **Laboratory Values**: Lab test results summary with descriptive statistics
- **Concomitant Medications**: Concurrent medication usage analysis
- **Subject Disposition**: Study completion status and discontinuation reasons

### 🔧 **Advanced Filtering**
- Filter by treatment groups (Placebo, Drug A 10mg, Drug A 20mg)
- Gender-based filtering (Male/Female)
- Age range filtering (customizable min/max)
- Real-time filter application

### 📊 **Data Export**
- Export tables as HTML files
- Export raw data as CSV
- Print-friendly table formatting
- Professional styling for presentations

### 💻 **Modern Interface**
- Responsive design for all devices
- Professional clinical research styling
- Intuitive controls familiar to SAS programmers
- Real-time table generation

## Technology Stack

- **Backend**: Python Flask
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with gradient themes
- **Icons**: Font Awesome

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd /path/to/your/project/folder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data**
   ```bash
   python data_generator.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Sample Data

The application includes realistic clinical trial datasets:

- **150 subjects** across 3 treatment groups
- **Demographics**: Age, sex, race, weight, height, BMI, country
- **Adverse Events**: 19 different AE terms with severity and relationship
- **Vital Signs**: SBP, DBP, pulse, temperature, weight over 4 visits
- **Laboratory**: 6 lab tests (ALT, AST, Creatinine, Hemoglobin, Glucose, Cholesterol)
- **Concomitant Medications**: 10 common medications with dosing
- **Disposition**: Study completion and discontinuation data

## Usage Guide

### Generating Your First Table

1. **Select Table Type**: Choose from the dropdown (e.g., "Adverse Events Summary")
2. **Apply Filters** (Optional):
   - Select specific treatment groups
   - Filter by gender
   - Set age range limits
3. **Click "Generate Table"**: The table will be created instantly
4. **Export Results**: Use HTML, CSV, or Print options

### Understanding Table Outputs

#### Adverse Events Summary
- Shows count and percentage of subjects experiencing each AE
- Grouped by treatment arm
- Sorted by frequency (most common first)

#### Demographics Table
- Age statistics (N, mean±SD, range)
- Sex distribution with percentages
- BMI summary statistics

#### Vital Signs Summary
- Descriptive statistics by visit and treatment
- Shows N, mean±SD for each measurement

### Tips for SAS Programmers

This tool provides similar functionality to common SAS procedures:
- **PROC FREQ** → Adverse Events Summary, Demographics
- **PROC MEANS** → Vital Signs, Laboratory summaries
- **PROC TABULATE** → Cross-tabulation features
- **ODS** → HTML export functionality

## File Structure

```
ClinicalTrials-sas/
├── app.py                 # Main Flask application
├── data_generator.py      # Sample data generation
├── table_generator.py     # Table generation logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Generated datasets (CSV files)
├── templates/
│   └── index.html        # Main web interface
└── static/
    ├── css/
    │   └── styles.css    # Application styling
    └── js/
        └── main.js       # Frontend JavaScript
```

## Customization

### Adding New Table Types

1. **Update `table_generator.py`**:
   ```python
   def generate_new_table_type(self, filters=None):
       # Your table generation logic here
       return result_dict
   ```

2. **Add route in `app.py`**:
   ```python
   elif table_type == 'new_table':
       result = generator.generate_new_table_type(filters)
   ```

3. **Update the frontend**: Add new option to `/api/tables` endpoint

### Modifying Sample Data

Edit `data_generator.py` to:
- Change number of subjects
- Add new variables
- Modify treatment groups
- Adjust adverse event rates

### Styling Customization

The application uses CSS custom properties for easy theming:
- Primary colors: `#667eea` to `#764ba2`
- Background gradients and card styling
- Responsive breakpoints for mobile devices

## Deployment

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment
For production deployment, consider:
- Using a WSGI server (Gunicorn)
- Adding authentication if needed
- Setting up SSL/HTTPS
- Configuring a reverse proxy (nginx)

## Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## Contributing

This is a demonstration project for SAS programmers learning web development. Feel free to:
- Add new table types
- Improve the UI/UX
- Add statistical tests
- Implement data validation

## License

This project is created for educational purposes and clinical trial table generation.

## Support

For questions about clinical trial programming or transitioning from SAS to Python/web development, this application serves as a practical example of modern data presentation techniques.

---

**Built for Clinical Research Professionals** 🧬📊
