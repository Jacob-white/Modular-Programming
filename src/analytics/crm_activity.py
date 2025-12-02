import pandas as pd

def summarize_activity_by_type(df: pd.DataFrame, type_col: str) -> pd.DataFrame:
    """
    Counts activities by type (Call, Meeting, Email).
    """
    return df[type_col].value_counts().reset_index(name='Count')

def correlate_activity_sales(activity_df: pd.DataFrame, sales_df: pd.DataFrame, join_col: str, activity_count_col: str, sales_col: str) -> float:
    """
    Calculates correlation between activity count and sales.
    Expects activity_df to be aggregated by advisor/territory.
    """
    merged = pd.merge(activity_df, sales_df, on=join_col, how='inner')
    return merged[activity_count_col].corr(merged[sales_col])
