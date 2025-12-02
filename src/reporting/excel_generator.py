import pandas as pd
import io
from typing import Dict, Optional
from src.core.logger import logger

def generate_excel_report(
    dataframes: Dict[str, pd.DataFrame], 
    file_path: str,
    charts: Optional[Dict[str, io.BytesIO]] = None
):
    """
    Generates an Excel report with multiple sheets and optional charts.
    
    Args:
        dataframes: Dictionary mapping sheet names to DataFrames.
        file_path: Output file path.
        charts: Dictionary mapping sheet names to BytesIO objects containing chart images.
                The chart will be inserted into the specified sheet.
    """
    try:
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        workbook = writer.book
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            
            # Format columns
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Adjust column width
            for i, col in enumerate(df.columns):
                column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_len)
                
            # Insert chart if available for this sheet
            if charts and sheet_name in charts:
                image_data = charts[sheet_name]
                worksheet.insert_image('E2', 'chart.png', {'image_data': image_data})
                
        writer.close()
        logger.info(f"Excel report generated at {file_path}")
        
    except Exception as e:
        logger.error(f"Failed to generate Excel report: {e}")
        raise
