import pandas as pd
from datetime import date, timedelta
from typing import Tuple

def get_fiscal_year_and_quarter(date_obj: date, fiscal_year_start_month: int = 1) -> Tuple[int, int]:
    """
    Returns the fiscal year and quarter for a given date.
    """
    month = date_obj.month
    year = date_obj.year
    
    # Adjust month to be 0-indexed relative to fiscal start
    # e.g. if start is 4 (April), then April (4) -> 0, March (3) -> 11
    adj_month = (month - fiscal_year_start_month) % 12
    
    quarter = (adj_month // 3) + 1
    
    # If the month is before the start month, it's part of the previous calendar year's fiscal year
    # Wait, usually if FY starts in April 2024, then April 2024 is FY2025 (or FY2024 depending on convention).
    # Let's assume "FY Ending" convention (common in US gov) or "FY Starting"
    # Let's stick to: FY is the year the fiscal year ENDS.
    # If start is Jan, FY == Calendar Year.
    # If start is April, April 2024 starts FY 2025 (ends March 2025).
    
    # Actually, let's use a simpler logic:
    # If month >= start_month, then it's in the current calendar year's fiscal cycle.
    # If we assume FY2024 starts in 2023... this gets complicated.
    
    # Let's use standard corporate: FY2024 starts Jan 1 2024 (if standard).
    # If non-standard, usually denoted by end year.
    
    if fiscal_year_start_month == 1:
        fiscal_year = year
    else:
        if month >= fiscal_year_start_month:
            fiscal_year = year + 1
        else:
            fiscal_year = year
            
    return fiscal_year, quarter

def get_business_days(start_date: date, end_date: date) -> int:
    """
    Calculates number of business days between two dates.
    """
    return pd.bdate_range(start=start_date, end=end_date).size

def get_previous_business_day(date_obj: date) -> date:
    """
    Returns the previous business day.
    """
    return (pd.Timestamp(date_obj) - pd.tseries.offsets.BusinessDay(1)).date()

def get_fiscal_year(date_obj: date, fiscal_year_start_month: int = 1) -> int:
    return get_fiscal_year_and_quarter(date_obj, fiscal_year_start_month)[0]

def get_fiscal_quarter(date_obj: date, fiscal_year_start_month: int = 1) -> int:
    return get_fiscal_year_and_quarter(date_obj, fiscal_year_start_month)[1]

def add_business_days(date_obj: date, days: int) -> date:
    return (pd.Timestamp(date_obj) + pd.tseries.offsets.BusinessDay(days)).date()
