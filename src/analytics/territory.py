import pandas as pd
from ..core.logger import logger

class TerritoryManager:
    """
    Manages territory mappings and assignments.
    """
    def __init__(self, mapping_df: pd.DataFrame = None):
        """
        Initialize with a DataFrame containing Zip Code to Territory/Wholesaler mapping.
        Expected columns: 'ZipCode', 'Territory', 'Wholesaler'
        """
        self.mapping_df = mapping_df

    def load_mapping_from_csv(self, filepath: str):
        """
        Loads territory mapping from a CSV file.
        """
        try:
            self.mapping_df = pd.read_csv(filepath, dtype={'ZipCode': str})
            logger.info(f"Loaded territory mapping from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load mapping from CSV: {e}")
            raise

    def assign_territory(self, data_df: pd.DataFrame, zip_col: str) -> pd.DataFrame:
        """
        Assigns Territory and Wholesaler to the data DataFrame based on Zip Code.
        """
        if self.mapping_df is None:
            logger.error("Territory mapping not loaded.")
            raise ValueError("Territory mapping not loaded.")
        
        if zip_col not in data_df.columns:
            logger.error(f"Zip code column '{zip_col}' not found in data.")
            raise ValueError(f"Zip code column '{zip_col}' not found in data.")

        # Ensure zip codes are strings for merging
        data_df[zip_col] = data_df[zip_col].astype(str)
        
        logger.info("Merging data with territory mapping...")
        merged_df = pd.merge(
            data_df,
            self.mapping_df,
            left_on=zip_col,
            right_on='ZipCode',
            how='left'
        )
        
        return merged_df
