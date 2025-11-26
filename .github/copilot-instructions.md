<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Clinical Trials Safety Tables Generator - Copilot Instructions

This is a Flask web application for generating clinical trial safety and efficacy tables, designed for SAS programmers transitioning to web-based solutions.

## Project Context
- **Purpose**: Generate professional clinical trial tables (adverse events, demographics, vital signs, etc.)
- **Target Users**: SAS programmers and clinical research professionals
- **Tech Stack**: Python Flask backend, HTML/CSS/JavaScript frontend, Pandas for data processing

## Code Style Guidelines
- Follow PEP 8 for Python code
- Use descriptive variable names following clinical research conventions (e.g., SUBJID, AETERM, TRT)
- Include comprehensive docstrings for all functions
- Use type hints where appropriate

## Clinical Domain Knowledge
- Follow ICH GCP and CDISC standards for variable naming
- Use standard clinical trial terminology (AE = Adverse Event, SAE = Serious Adverse Event, etc.)
- Generate tables following industry standards (counts, percentages, statistical summaries)
- Include appropriate safety and efficacy endpoints

## File Organization
- `app.py`: Main Flask application with API routes
- `table_generator.py`: Core table generation logic
- `data_generator.py`: Sample clinical trial data creation
- `templates/`: HTML templates with responsive design
- `static/`: CSS and JavaScript assets
- `data/`: Generated CSV datasets

## Key Features to Maintain
- Professional medical research table formatting
- Real-time filtering capabilities (treatment, demographics)
- Export functionality (HTML, CSV, print)
- Responsive design for various devices
- Error handling and data validation

## When Adding New Features
- Ensure clinical data integrity and validation
- Follow existing table generation patterns in `TableGenerator` class
- Add corresponding API endpoints in Flask app
- Update frontend JavaScript for new functionality
- Include appropriate statistical summaries and formatting

## Data Standards
- Use standard units (mg/dL, U/L, etc.)
- Follow consistent date formatting (YYYY-MM-DD)
- Include proper statistical measures (N, mean±SD, counts/percentages)
- Handle missing data appropriately

## Security Considerations
- Validate all input data
- Sanitize user inputs for filters
- Use parameterized queries if adding database functionality
- Implement proper error handling without exposing sensitive information
