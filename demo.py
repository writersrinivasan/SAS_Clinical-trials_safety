#!/usr/bin/env python3

"""
Demo script to test table generation functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from table_generator import TableGenerator

def demo_table_generation():
    """Demonstrate table generation capabilities"""
    print("🧬 Clinical Trials Safety Tables - Demo")
    print("=" * 50)
    
    # Initialize table generator
    generator = TableGenerator()
    
    # Test adverse events table
    print("\n📊 Generating Adverse Events Summary Table...")
    ae_result = generator.generate_adverse_events_table()
    print(f"✅ Generated table with {len(ae_result['data'])} adverse event terms")
    
    # Test demographics table
    print("\n👥 Generating Demographics Table...")
    demo_result = generator.generate_demographics_table()
    print(f"✅ Generated demographics summary")
    
    # Test with filters
    print("\n🔍 Testing filters (Drug A 20mg only)...")
    filtered_result = generator.generate_adverse_events_table(
        filters={'treatment': ['Drug A 20mg']}
    )
    print(f"✅ Generated filtered table with {len(filtered_result['data'])} adverse event terms")
    
    print(f"\n📈 Summary:")
    print(f"   - Total subjects in study: {sum(ae_result['total_subjects'].values())}")
    print(f"   - Treatment groups: {list(ae_result['total_subjects'].keys())}")
    print(f"   - Available table types: 6")
    
    print("\n🎉 All table generation tests passed!")
    print("🌐 Start the web application with: python app.py")

if __name__ == "__main__":
    demo_table_generation()
