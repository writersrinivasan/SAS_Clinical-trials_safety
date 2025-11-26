import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    """Generate sample clinical trial datasets"""
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate Demographics data
    n_subjects = 150
    
    demographics_data = {
        'SUBJID': [f'SUB{str(i).zfill(3)}' for i in range(1, n_subjects + 1)],
        'TRT': np.random.choice(['Placebo', 'Drug A 10mg', 'Drug A 20mg'], n_subjects, p=[0.33, 0.33, 0.34]),
        'AGE': np.random.normal(45, 15, n_subjects).astype(int),
        'SEX': np.random.choice(['M', 'F'], n_subjects, p=[0.48, 0.52]),
        'RACE': np.random.choice(['White', 'Black', 'Asian', 'Hispanic', 'Other'], n_subjects, p=[0.6, 0.15, 0.15, 0.08, 0.02]),
        'WEIGHT': np.random.normal(70, 15, n_subjects).round(1),
        'HEIGHT': np.random.normal(170, 12, n_subjects).round(1),
        'COUNTRY': np.random.choice(['USA', 'Canada', 'Germany', 'UK'], n_subjects, p=[0.4, 0.2, 0.2, 0.2])
    }
    
    # Calculate BMI
    demographics_data['BMI'] = (demographics_data['WEIGHT'] / ((demographics_data['HEIGHT']/100) ** 2)).round(1)
    
    demographics_df = pd.DataFrame(demographics_data)
    demographics_df.to_csv('data/demographics.csv', index=False)
    
    # Generate Adverse Events data
    ae_terms = [
        'Headache', 'Nausea', 'Dizziness', 'Fatigue', 'Diarrhea', 
        'Constipation', 'Insomnia', 'Back pain', 'Upper respiratory tract infection',
        'Hypertension', 'Anxiety', 'Depression', 'Muscle spasms', 'Cough',
        'Dry mouth', 'Abdominal pain', 'Vomiting', 'Rash', 'Fever'
    ]
    
    ae_data = []
    for subjid in demographics_data['SUBJID']:
        trt = demographics_df[demographics_df['SUBJID'] == subjid]['TRT'].iloc[0]
        
        # Different AE rates by treatment
        if trt == 'Placebo':
            n_aes = np.random.poisson(0.8)
        elif trt == 'Drug A 10mg':
            n_aes = np.random.poisson(1.2)
        else:  # Drug A 20mg
            n_aes = np.random.poisson(1.8)
            
        for ae_num in range(n_aes):
            ae_data.append({
                'SUBJID': subjid,
                'TRT': trt,
                'AETERM': np.random.choice(ae_terms),
                'AESEV': np.random.choice(['Mild', 'Moderate', 'Severe'], p=[0.6, 0.3, 0.1]),
                'AEREL': np.random.choice(['Not Related', 'Possibly Related', 'Probably Related', 'Definitely Related'], 
                                       p=[0.4, 0.3, 0.2, 0.1]),
                'AESTDT': (datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                'AEENDT': (datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
                'AEOUT': np.random.choice(['Recovered', 'Recovering', 'Not Recovered', 'Unknown'], p=[0.6, 0.2, 0.15, 0.05])
            })
    
    ae_df = pd.DataFrame(ae_data)
    ae_df.to_csv('data/adverse_events.csv', index=False)
    
    # Generate Vital Signs data
    vs_data = []
    for subjid in demographics_data['SUBJID']:
        trt = demographics_df[demographics_df['SUBJID'] == subjid]['TRT'].iloc[0]
        for visit in ['Baseline', 'Week 4', 'Week 8', 'Week 12']:
            vs_data.append({
                'SUBJID': subjid,
                'TRT': trt,
                'VISIT': visit,
                'SBP': np.random.normal(125, 15),  # Systolic BP
                'DBP': np.random.normal(80, 10),   # Diastolic BP
                'PULSE': np.random.normal(72, 8),   # Heart rate
                'TEMP': np.random.normal(36.5, 0.5), # Temperature
                'WEIGHT': demographics_df[demographics_df['SUBJID'] == subjid]['WEIGHT'].iloc[0] + np.random.normal(0, 2)
            })
    
    vs_df = pd.DataFrame(vs_data)
    vs_df.to_csv('data/vital_signs.csv', index=False)
    
    # Generate Laboratory data
    lab_data = []
    lab_tests = ['ALT', 'AST', 'Creatinine', 'Hemoglobin', 'Glucose', 'Cholesterol']
    
    for subjid in demographics_data['SUBJID']:
        trt = demographics_df[demographics_df['SUBJID'] == subjid]['TRT'].iloc[0]
        for visit in ['Baseline', 'Week 4', 'Week 8', 'Week 12']:
            for test in lab_tests:
                # Different normal ranges for different tests
                if test == 'ALT':
                    value = np.random.normal(25, 8)
                elif test == 'AST':
                    value = np.random.normal(28, 10)
                elif test == 'Creatinine':
                    value = np.random.normal(1.0, 0.2)
                elif test == 'Hemoglobin':
                    value = np.random.normal(13.5, 1.5)
                elif test == 'Glucose':
                    value = np.random.normal(95, 15)
                else:  # Cholesterol
                    value = np.random.normal(180, 30)
                
                lab_data.append({
                    'SUBJID': subjid,
                    'TRT': trt,
                    'VISIT': visit,
                    'LBTEST': test,
                    'LBVAL': round(value, 2),
                    'LBUNIT': 'mg/dL' if test in ['Glucose', 'Cholesterol'] else 'U/L' if test in ['ALT', 'AST'] else 'g/dL' if test == 'Hemoglobin' else 'mg/dL'
                })
    
    lab_df = pd.DataFrame(lab_data)
    lab_df.to_csv('data/laboratory.csv', index=False)
    
    # Generate Concomitant Medications data
    conmed_data = []
    common_meds = [
        'Aspirin', 'Ibuprofen', 'Acetaminophen', 'Lisinopril', 'Metformin',
        'Atorvastatin', 'Omeprazole', 'Levothyroxine', 'Metoprolol', 'Vitamin D'
    ]
    
    for subjid in demographics_data['SUBJID']:
        trt = demographics_df[demographics_df['SUBJID'] == subjid]['TRT'].iloc[0]
        n_meds = np.random.poisson(2)  # Average 2 conmeds per subject
        
        for med_num in range(n_meds):
            conmed_data.append({
                'SUBJID': subjid,
                'TRT': trt,
                'CMTRT': np.random.choice(common_meds),
                'CMDOSE': f"{np.random.choice([5, 10, 20, 25, 50, 100, 200])} mg",
                'CMFREQ': np.random.choice(['Once daily', 'Twice daily', 'Three times daily', 'As needed']),
                'CMSTDT': (datetime(2022, 6, 1) + timedelta(days=np.random.randint(0, 180))).strftime('%Y-%m-%d')
            })
    
    conmed_df = pd.DataFrame(conmed_data)
    conmed_df.to_csv('data/concomitant_medications.csv', index=False)
    
    # Generate Disposition data
    disp_data = []
    for subjid in demographics_data['SUBJID']:
        trt = demographics_df[demographics_df['SUBJID'] == subjid]['TRT'].iloc[0]
        
        # Different completion rates by treatment
        if trt == 'Placebo':
            completion_prob = 0.85
        else:
            completion_prob = 0.80  # Slightly lower due to AEs
            
        completed = np.random.random() < completion_prob
        
        if completed:
            disposition = 'Completed'
            reason = 'Study Completion'
        else:
            disposition = 'Discontinued'
            reason = np.random.choice(['Adverse Event', 'Withdrawal of Consent', 'Lost to Follow-up', 'Protocol Violation'], 
                                    p=[0.4, 0.3, 0.2, 0.1])
        
        disp_data.append({
            'SUBJID': subjid,
            'TRT': trt,
            'DSDECOD': disposition,
            'DSTERM': reason
        })
    
    disp_df = pd.DataFrame(disp_data)
    disp_df.to_csv('data/disposition.csv', index=False)
    
    print("Sample clinical trial datasets generated successfully!")
    print(f"Generated data for {n_subjects} subjects across 6 datasets")

if __name__ == "__main__":
    generate_sample_data()
