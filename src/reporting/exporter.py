import pandas as pd
from ..core.logger import logger

def export_to_excel(df: pd.DataFrame, filepath: str, sheet_name: str = 'Sheet1'):
    """
    Exports DataFrame to Excel.
    """
    try:
        logger.info(f"Exporting data to Excel: {filepath}")
        df.to_excel(filepath, index=False, sheet_name=sheet_name)
        logger.info("Export successful.")
    except Exception as e:
        logger.error(f"Failed to export to Excel: {e}")
        raise

def export_to_csv(df: pd.DataFrame, filepath: str):
    """
    Exports DataFrame to CSV.
    """
    try:
        logger.info(f"Exporting data to CSV: {filepath}")
        df.to_csv(filepath, index=False)
        logger.info("Export successful.")
    except Exception as e:
        logger.error(f"Failed to export to CSV: {e}")
        raise
