import pandas as pd
import re
from ..core.logger import logger

def clean_zip_code(zip_code: str) -> str:
    """
    Standardizes zip codes to 5 digits.
    Handles 9-digit zips by taking the first 5.
    Returns None for invalid zips.
    """
    if pd.isna(zip_code):
        return None
    
    zip_str = str(zip_code).strip()
    
    # Remove non-numeric characters
    zip_str = re.sub(r'[^0-9]', '', zip_str)
    
    if len(zip_str) == 5:
        return zip_str
    elif len(zip_str) > 5:
        return zip_str[:5]
    elif len(zip_str) < 5 and len(zip_str) > 0:
        return zip_str.zfill(5)
    else:
        return None

def standardize_advisor_name(name: str) -> str:
    """
    Standardizes advisor names to Title Case.
    Removes extra whitespace.
    """
    if pd.isna(name):
        return None
    
    return " ".join(name.split()).title()

def validate_email(email: str) -> bool:
    """
    Validates email format using regex.
    """
    if pd.isna(email):
        return False
    
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_regex, str(email)))

def clean_dataframe(df: pd.DataFrame, zip_col: str = None, name_col: str = None, email_col: str = None) -> pd.DataFrame:
    """
    Applies cleaning functions to a DataFrame.
    """
    df_clean = df.copy()
    
    if zip_col and zip_col in df_clean.columns:
        logger.info(f"Cleaning zip code column: {zip_col}")
        df_clean[zip_col] = df_clean[zip_col].apply(clean_zip_code)
        
    if name_col and name_col in df_clean.columns:
        logger.info(f"Standardizing name column: {name_col}")
        df_clean[name_col] = df_clean[name_col].apply(standardize_advisor_name)
        
    if email_col and email_col in df_clean.columns:
        logger.info(f"Validating email column: {email_col}")
        # Create a new boolean column for validity? Or just filter?
        # For now, let's just log invalid count
        invalid_count = (~df_clean[email_col].apply(validate_email)).sum()
        logger.warning(f"Found {invalid_count} invalid emails in {email_col}")
        
    return df_clean
