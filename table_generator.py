import pandas as pd
import numpy as np
from datetime import datetime
import os

class TableGenerator:
    """Generate clinical trial safety and efficacy tables"""
    
    def __init__(self):
        self.data_path = 'data'
        self.load_datasets()
    
    def load_datasets(self):
        """Load all available datasets"""
        try:
            self.demographics = pd.read_csv(f'{self.data_path}/demographics.csv')
            self.adverse_events = pd.read_csv(f'{self.data_path}/adverse_events.csv')
            self.vital_signs = pd.read_csv(f'{self.data_path}/vital_signs.csv')
            self.laboratory = pd.read_csv(f'{self.data_path}/laboratory.csv')
            self.conmed = pd.read_csv(f'{self.data_path}/concomitant_medications.csv')
            self.disposition = pd.read_csv(f'{self.data_path}/disposition.csv')
        except FileNotFoundError as e:
            print(f"Dataset file not found: {e}")
    
    def apply_filters(self, df, filters):
        """Apply filters to dataframe"""
        filtered_df = df.copy()
        
        if 'treatment' in filters and filters['treatment']:
            filtered_df = filtered_df[filtered_df['TRT'].isin(filters['treatment'])]
        
        if 'sex' in filters and filters['sex']:
            if 'SEX' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['SEX'].isin(filters['sex'])]
        
        if 'age_min' in filters and filters['age_min']:
            if 'AGE' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['AGE'] >= filters['age_min']]
        
        if 'age_max' in filters and filters['age_max']:
            if 'AGE' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['AGE'] <= filters['age_max']]
                
        return filtered_df
    
    def generate_adverse_events_table(self, filters=None):
        """Generate adverse events summary table"""
        if filters is None:
            filters = {}
        
        # Merge with demographics for filtering
        ae_with_demo = self.adverse_events.merge(
            self.demographics[['SUBJID', 'SEX', 'AGE']], 
            on='SUBJID', 
            how='left'
        )
        
        filtered_df = self.apply_filters(ae_with_demo, filters)
        
        # Count total subjects per treatment
        total_subjects = self.demographics.groupby('TRT').size().to_dict()
        if filters:
            demo_filtered = self.apply_filters(self.demographics, filters)
            total_subjects = demo_filtered.groupby('TRT').size().to_dict()
        
        # Generate summary by AE term and treatment
        ae_summary = []
        
        for ae_term in filtered_df['AETERM'].unique():
            ae_data = filtered_df[filtered_df['AETERM'] == ae_term]
            
            row = {'AE_Term': ae_term}
            
            for trt in sorted(filtered_df['TRT'].unique()):
                trt_data = ae_data[ae_data['TRT'] == trt]
                n_subjects_with_ae = len(trt_data['SUBJID'].unique())
                total_n = total_subjects.get(trt, 0)
                
                if total_n > 0:
                    percentage = (n_subjects_with_ae / total_n) * 100
                    row[f'{trt}_n'] = n_subjects_with_ae
                    row[f'{trt}_total'] = total_n
                    row[f'{trt}_percent'] = f"{n_subjects_with_ae} ({percentage:.1f}%)"
                else:
                    row[f'{trt}_percent'] = "0 (0.0%)"
        
            ae_summary.append(row)
        
        # Sort by most common AE
        ae_summary_df = pd.DataFrame(ae_summary)
        
        # Calculate total subjects with AEs for sorting
        total_ae_counts = []
        for _, row in ae_summary_df.iterrows():
            total_count = sum([int(row[col].split(' ')[0]) for col in row.index if col.endswith('_percent')])
            total_ae_counts.append(total_count)
        
        ae_summary_df['total_count'] = total_ae_counts
        ae_summary_df = ae_summary_df.sort_values('total_count', ascending=False)
        ae_summary_df = ae_summary_df.drop('total_count', axis=1)
        
        # Convert to HTML table
        html_table = self._dataframe_to_html_table(
            ae_summary_df, 
            title="Adverse Events Summary Table",
            subtitle=f"Number of Subjects (%) with Adverse Events"
        )
        
        return {
            'table_html': html_table,
            'data': ae_summary_df.to_dict('records'),
            'total_subjects': total_subjects,
            'summary': f"Generated adverse events table with {len(ae_summary_df)} unique AE terms"
        }
    
    def generate_demographics_table(self, filters=None):
        """Generate demographics summary table"""
        if filters is None:
            filters = {}
            
        filtered_df = self.apply_filters(self.demographics, filters)
        
        demo_summary = []
        
        # Age statistics
        age_stats = filtered_df.groupby('TRT')['AGE'].agg(['count', 'mean', 'std', 'min', 'max']).round(1)
        
        for trt in age_stats.index:
            stats = age_stats.loc[trt]
            demo_summary.append({
                'Characteristic': f'Age - {trt}',
                'Statistic': f"N={int(stats['count'])}, Mean±SD={stats['mean']}±{stats['std']}, Range={int(stats['min'])}-{int(stats['max'])}"
            })
        
        # Sex distribution
        sex_crosstab = pd.crosstab(filtered_df['TRT'], filtered_df['SEX'], margins=True)
        
        for trt in filtered_df['TRT'].unique():
            trt_data = filtered_df[filtered_df['TRT'] == trt]
            total = len(trt_data)
            male_count = len(trt_data[trt_data['SEX'] == 'M'])
            female_count = len(trt_data[trt_data['SEX'] == 'F'])
            
            demo_summary.append({
                'Characteristic': f'Sex - {trt}',
                'Statistic': f"Male: {male_count} ({male_count/total*100:.1f}%), Female: {female_count} ({female_count/total*100:.1f}%)"
            })
        
        # BMI statistics
        bmi_stats = filtered_df.groupby('TRT')['BMI'].agg(['mean', 'std']).round(1)
        
        for trt in bmi_stats.index:
            stats = bmi_stats.loc[trt]
            demo_summary.append({
                'Characteristic': f'BMI - {trt}',
                'Statistic': f"Mean±SD={stats['mean']}±{stats['std']}"
            })
        
        demo_df = pd.DataFrame(demo_summary)
        
        html_table = self._dataframe_to_html_table(
            demo_df,
            title="Demographics Summary Table",
            subtitle="Baseline Characteristics by Treatment Group"
        )
        
        return {
            'table_html': html_table,
            'data': demo_df.to_dict('records'),
            'summary': f"Generated demographics table for {len(filtered_df)} subjects"
        }
    
    def generate_vital_signs_table(self, filters=None):
        """Generate vital signs summary table"""
        if filters is None:
            filters = {}
            
        vs_with_demo = self.vital_signs.merge(
            self.demographics[['SUBJID', 'SEX', 'AGE']],
            on='SUBJID',
            how='left'
        )
        
        filtered_df = self.apply_filters(vs_with_demo, filters)
        
        vs_summary = []
        
        for visit in filtered_df['VISIT'].unique():
            visit_data = filtered_df[filtered_df['VISIT'] == visit]
            
            for vital in ['SBP', 'DBP', 'PULSE', 'TEMP']:
                for trt in sorted(visit_data['TRT'].unique()):
                    trt_data = visit_data[visit_data['TRT'] == trt][vital].dropna()
                    
                    if len(trt_data) > 0:
                        vs_summary.append({
                            'Visit': visit,
                            'Vital_Sign': vital,
                            'Treatment': trt,
                            'N': len(trt_data),
                            'Mean': round(trt_data.mean(), 1),
                            'SD': round(trt_data.std(), 1),
                            'Min': round(trt_data.min(), 1),
                            'Max': round(trt_data.max(), 1),
                            'Summary': f"N={len(trt_data)}, {trt_data.mean():.1f}±{trt_data.std():.1f}"
                        })
        
        vs_df = pd.DataFrame(vs_summary)
        
        html_table = self._dataframe_to_html_table(
            vs_df[['Visit', 'Vital_Sign', 'Treatment', 'Summary']],
            title="Vital Signs Summary Table",
            subtitle="Descriptive Statistics by Visit and Treatment"
        )
        
        return {
            'table_html': html_table,
            'data': vs_df.to_dict('records'),
            'summary': f"Generated vital signs table with {len(vs_df)} measurements"
        }
    
    def generate_laboratory_table(self, filters=None):
        """Generate laboratory values summary table"""
        if filters is None:
            filters = {}
            
        lab_with_demo = self.laboratory.merge(
            self.demographics[['SUBJID', 'SEX', 'AGE']],
            on='SUBJID',
            how='left'
        )
        
        filtered_df = self.apply_filters(lab_with_demo, filters)
        
        lab_summary = []
        
        for visit in filtered_df['VISIT'].unique():
            visit_data = filtered_df[filtered_df['VISIT'] == visit]
            
            for test in visit_data['LBTEST'].unique():
                test_data = visit_data[visit_data['LBTEST'] == test]
                
                for trt in sorted(test_data['TRT'].unique()):
                    trt_data = test_data[test_data['TRT'] == trt]['LBVAL'].dropna()
                    
                    if len(trt_data) > 0:
                        lab_summary.append({
                            'Visit': visit,
                            'Lab_Test': test,
                            'Treatment': trt,
                            'N': len(trt_data),
                            'Mean': round(trt_data.mean(), 2),
                            'SD': round(trt_data.std(), 2),
                            'Summary': f"N={len(trt_data)}, {trt_data.mean():.2f}±{trt_data.std():.2f}"
                        })
        
        lab_df = pd.DataFrame(lab_summary)
        
        html_table = self._dataframe_to_html_table(
            lab_df[['Visit', 'Lab_Test', 'Treatment', 'Summary']],
            title="Laboratory Values Summary Table",
            subtitle="Descriptive Statistics by Visit and Treatment"
        )
        
        return {
            'table_html': html_table,
            'data': lab_df.to_dict('records'),
            'summary': f"Generated laboratory table with {len(lab_df)} test results"
        }
    
    def generate_conmed_table(self, filters=None):
        """Generate concomitant medications table"""
        if filters is None:
            filters = {}
            
        conmed_with_demo = self.conmed.merge(
            self.demographics[['SUBJID', 'SEX', 'AGE']],
            on='SUBJID',
            how='left'
        )
        
        filtered_df = self.apply_filters(conmed_with_demo, filters)
        
        # Count total subjects per treatment
        total_subjects = self.demographics.groupby('TRT').size().to_dict()
        if filters:
            demo_filtered = self.apply_filters(self.demographics, filters)
            total_subjects = demo_filtered.groupby('TRT').size().to_dict()
        
        conmed_summary = []
        
        for medication in filtered_df['CMTRT'].unique():
            med_data = filtered_df[filtered_df['CMTRT'] == medication]
            
            row = {'Medication': medication}
            
            for trt in sorted(filtered_df['TRT'].unique()):
                trt_data = med_data[med_data['TRT'] == trt]
                n_subjects_with_med = len(trt_data['SUBJID'].unique())
                total_n = total_subjects.get(trt, 0)
                
                if total_n > 0:
                    percentage = (n_subjects_with_med / total_n) * 100
                    row[f'{trt}'] = f"{n_subjects_with_med} ({percentage:.1f}%)"
                else:
                    row[f'{trt}'] = "0 (0.0%)"
            
            conmed_summary.append(row)
        
        conmed_df = pd.DataFrame(conmed_summary)
        
        html_table = self._dataframe_to_html_table(
            conmed_df,
            title="Concomitant Medications Table",
            subtitle="Number of Subjects (%) Taking Concomitant Medications"
        )
        
        return {
            'table_html': html_table,
            'data': conmed_df.to_dict('records'),
            'total_subjects': total_subjects,
            'summary': f"Generated concomitant medications table with {len(conmed_df)} medications"
        }
    
    def generate_disposition_table(self, filters=None):
        """Generate subject disposition table"""
        if filters is None:
            filters = {}
            
        disp_with_demo = self.disposition.merge(
            self.demographics[['SUBJID', 'SEX', 'AGE']],
            on='SUBJID',
            how='left'
        )
        
        filtered_df = self.apply_filters(disp_with_demo, filters)
        
        # Count total subjects per treatment
        total_subjects = self.demographics.groupby('TRT').size().to_dict()
        if filters:
            demo_filtered = self.apply_filters(self.demographics, filters)
            total_subjects = demo_filtered.groupby('TRT').size().to_dict()
        
        disp_summary = []
        
        for disposition in filtered_df['DSDECOD'].unique():
            disp_data = filtered_df[filtered_df['DSDECOD'] == disposition]
            
            row = {'Disposition': disposition}
            
            for trt in sorted(filtered_df['TRT'].unique()):
                trt_data = disp_data[disp_data['TRT'] == trt]
                n_subjects = len(trt_data)
                total_n = total_subjects.get(trt, 0)
                
                if total_n > 0:
                    percentage = (n_subjects / total_n) * 100
                    row[f'{trt}'] = f"{n_subjects} ({percentage:.1f}%)"
                else:
                    row[f'{trt}'] = "0 (0.0%)"
            
            disp_summary.append(row)
        
        # Add reasons for discontinuation
        discontinued_data = filtered_df[filtered_df['DSDECOD'] == 'Discontinued']
        if not discontinued_data.empty:
            for reason in discontinued_data['DSTERM'].unique():
                if reason != 'Study Completion':
                    reason_data = discontinued_data[discontinued_data['DSTERM'] == reason]
                    
                    row = {'Disposition': f'  {reason}'}
                    
                    for trt in sorted(filtered_df['TRT'].unique()):
                        trt_data = reason_data[reason_data['TRT'] == trt]
                        n_subjects = len(trt_data)
                        total_n = total_subjects.get(trt, 0)
                        
                        if total_n > 0:
                            percentage = (n_subjects / total_n) * 100
                            row[f'{trt}'] = f"{n_subjects} ({percentage:.1f}%)"
                        else:
                            row[f'{trt}'] = "0 (0.0%)"
                    
                    disp_summary.append(row)
        
        disp_df = pd.DataFrame(disp_summary)
        
        html_table = self._dataframe_to_html_table(
            disp_df,
            title="Subject Disposition Table",
            subtitle="Number of Subjects (%) by Disposition Status"
        )
        
        return {
            'table_html': html_table,
            'data': disp_df.to_dict('records'),
            'total_subjects': total_subjects,
            'summary': f"Generated disposition table for {sum(total_subjects.values())} subjects"
        }
    
    def _dataframe_to_html_table(self, df, title="", subtitle=""):
        """Convert pandas DataFrame to formatted HTML table"""
        
        html = f"""
        <div class="table-container">
            <h3 class="table-title">{title}</h3>
            <p class="table-subtitle">{subtitle}</p>
            <table class="clinical-table">
                <thead>
                    <tr>
        """
        
        # Add headers
        for col in df.columns:
            html += f"<th>{col.replace('_', ' ').title()}</th>"
        
        html += """
                    </tr>
                </thead>
                <tbody>
        """
        
        # Add data rows
        for _, row in df.iterrows():
            html += "<tr>"
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    value = ""
                html += f"<td>{value}</td>"
            html += "</tr>"
        
        html += """
                </tbody>
            </table>
        </div>
        """
        
        return html
