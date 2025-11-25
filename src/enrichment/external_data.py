import pandas as pd
from typing import List
from ..core.logger import logger

class ExternalDataEnricher:
    """
    Mock interface for enriching advisor data with external sources (e.g. Discovery, RIA DB).
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def enrich_advisors(self, advisor_df: pd.DataFrame, match_col: str) -> pd.DataFrame:
        """
        Enriches advisor DataFrame with mock external data (AUM, Team Size).
        """
        logger.info("Enriching advisor data from external source...")
        
        # Mock enrichment data
        enrichment_data = {
            'External_AUM': [10000000, 50000000, 25000000, 100000000],
            'TeamSize': [1, 3, 2, 5],
            'YearsExperience': [5, 15, 10, 20]
        }
        
        # Create a DataFrame with the same length as input or merge logic
        # For simplicity, let's just add random data if we can't match real IDs
        enriched_df = advisor_df.copy()
        
        # Add mock columns
        import numpy as np
        n = len(enriched_df)
        enriched_df['External_AUM'] = np.random.randint(1000000, 100000000, n)
        enriched_df['TeamSize'] = np.random.randint(1, 10, n)
        
        return enriched_df
