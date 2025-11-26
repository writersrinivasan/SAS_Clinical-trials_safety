# Contributing to Clinical Trials Safety Tables Generator

Thank you for your interest in contributing to this project! This application helps SAS programmers transition to modern web-based clinical trial table generation.

## 🎯 Project Goals

- Provide familiar clinical trial table generation for SAS programmers
- Follow CDISC and ICH GCP standards
- Create production-ready, regulatory-compliant tables
- Maintain clean, well-documented code

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Flask and Pandas

### Setup Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/SAS_Clinical-trials_safety.git
   cd SAS_Clinical-trials_safety
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate Sample Data**
   ```bash
   python data_generator.py
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

## 📝 How to Contribute

### Reporting Bugs
- Use GitHub Issues
- Include Python version, OS, and error messages
- Provide steps to reproduce

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the clinical trial use case
- Explain how it helps SAS programmers

### Code Contributions

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow PEP 8 style guidelines
   - Add docstrings to functions
   - Use clinical trial terminology (CDISC standards)

3. **Test Your Changes**
   ```bash
   python demo.py  # Test table generation
   python app.py   # Test web interface
   ```

4. **Commit with Clear Messages**
   ```bash
   git commit -m "feat: Add new vital signs table"
   git commit -m "fix: Correct adverse event percentage calculation"
   git commit -m "docs: Update README with new examples"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🎨 Code Style

- **Python**: Follow PEP 8
- **Variable Names**: Use CDISC standards (SUBJID, AETERM, TRT, etc.)
- **Comments**: Explain clinical trial concepts for non-SAS programmers
- **Docstrings**: Include for all functions and classes

### Example
```python
def generate_adverse_events_table(self, filters=None):
    """
    Generate adverse events summary table.
    
    Similar to SAS PROC FREQ for AE data.
    
    Args:
        filters (dict): Optional filters for treatment, demographics
        
    Returns:
        dict: Table HTML, data, and summary statistics
    """
```

## 🧪 Testing

Before submitting a pull request:

```bash
# Test core functionality
python demo.py

# Test table generation
python -c "from table_generator import TableGenerator; t = TableGenerator(); print('✅ Tests pass')"

# Check imports
python -c "import flask, pandas, numpy; print('✅ Dependencies OK')"
```

## 📚 Areas for Contribution

### High Priority
- [ ] Additional statistical tests (t-tests, chi-square)
- [ ] Data validation and CDISC compliance checks
- [ ] Database connectivity for real data
- [ ] User authentication
- [ ] Excel export functionality

### Documentation
- [ ] Video tutorials for SAS programmers
- [ ] Comparison guide: SAS vs Python/Flask
- [ ] API documentation
- [ ] More example use cases

### Features
- [ ] New table types (ECG, tumor response, etc.)
- [ ] Advanced filtering options
- [ ] Batch table generation
- [ ] Custom template support
- [ ] Interactive charts with Plotly

## 🏥 Clinical Research Standards

When contributing, please ensure:
- Tables follow FDA submission guidelines
- Variable naming follows CDISC SDTM/ADaM standards
- Statistical summaries are accurate (N, mean±SD, percentages)
- Missing data is handled appropriately
- Dates use ISO format (YYYY-MM-DD)

## 💬 Questions?

- Open a GitHub Issue
- Check existing documentation
- Review the code examples in `demo.py`

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be acknowledged in the README and release notes.

---

**Thank you for helping bridge SAS programming to modern web development!** 🧬📊
