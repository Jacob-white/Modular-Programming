import pytest
import pandas as pd
import os
from src.reporting.excel_generator import generate_excel_report
from src.visualization.charts import generate_bar_chart

def test_generate_excel_report(tmp_path):
    # Create sample data
    df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    df2 = pd.DataFrame({'X': ['x', 'y', 'z'], 'Y': [7, 8, 9]})
    
    # Create sample chart
    chart = generate_bar_chart(df1, 'A', 'B')
    
    # Output file
    output_file = tmp_path / "test_report.xlsx"
    
    # Generate report
    generate_excel_report(
        dataframes={'Sheet1': df1, 'Sheet2': df2},
        file_path=str(output_file),
        charts={'Sheet1': chart}
    )
    
    # Verify file exists
    assert os.path.exists(output_file)
    
    # Verify content (basic check)
    xls = pd.ExcelFile(output_file)
    assert 'Sheet1' in xls.sheet_names
    assert 'Sheet2' in xls.sheet_names
    
    read_df1 = pd.read_excel(output_file, sheet_name='Sheet1')
    assert len(read_df1) == 3
