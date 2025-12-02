import pandas as pd
from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel, ValidationError
from src.core.logger import logger

class DataValidator:
    """
    Validates pandas DataFrames against Pydantic models.
    """
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, model: Type[BaseModel]) -> bool:
        """
        Validates a DataFrame against a Pydantic model.
        Returns True if valid, raises ValidationError if invalid.
        """
        errors = []
        
        # Convert DataFrame to list of dicts for validation
        records = df.to_dict(orient='records')
        
        for i, record in enumerate(records):
            try:
                model(**record)
            except ValidationError as e:
                errors.append(f"Row {i}: {e}")
        
        if errors:
            error_msg = f"Validation failed with {len(errors)} errors:\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                error_msg += f"\n... and {len(errors) - 10} more errors."
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        return True

    @staticmethod
    def check_required_columns(df: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Checks if the DataFrame has all required columns.
        """
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            msg = f"Missing required columns: {missing}"
            logger.error(msg)
            raise ValueError(msg)
        return True
