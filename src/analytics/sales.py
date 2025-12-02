import pandas as pd
from ..core.logger import logger

def calculate_net_flows(df: pd.DataFrame, sales_col: str, redemptions_col: str) -> pd.Series:
    """
    Calculates Net Flows = Gross Sales - Redemptions.
    """
    return df[sales_col] - df[redemptions_col]

def calculate_market_share(df: pd.DataFrame, firm_assets_col: str, total_market_assets_col: str) -> pd.Series:
    """
    Calculates Market Share = Firm Assets / Total Market Assets.
    """
    return (df[firm_assets_col] / df[total_market_assets_col]) * 100

def summarize_sales_by_territory(df: pd.DataFrame, territory_col: str, sales_col: str) -> pd.DataFrame:
    """
    Aggregates sales by territory.
    """
    logger.info(f"Summarizing sales by {territory_col}")
    return df.groupby(territory_col)[sales_col].sum().reset_index().sort_values(by=sales_col, ascending=False)

def identify_top_advisors(df: pd.DataFrame, advisor_id_col: str, sales_col: str, top_n: int = 10) -> pd.DataFrame:
    """
    Identifies top N advisors by sales.
    """
    logger.info(f"Identifying top {top_n} advisors")
    return df.groupby(advisor_id_col)[sales_col].sum().reset_index().sort_values(by=sales_col, ascending=False).head(top_n)

def summarize_sales_by_channel(df: pd.DataFrame, channel_col: str, sales_col: str) -> pd.DataFrame:
    """
    Aggregates sales by channel.
    """
    logger.info(f"Summarizing sales by {channel_col}")
    return df.groupby(channel_col)[sales_col].sum().reset_index().sort_values(by=sales_col, ascending=False)

def summarize_sales_by_firm_type(df: pd.DataFrame, firm_type_col: str, sales_col: str) -> pd.DataFrame:
    """
    Aggregates sales by firm type.
    """
    logger.info(f"Summarizing sales by {firm_type_col}")
    return df.groupby(firm_type_col)[sales_col].sum().reset_index().sort_values(by=sales_col, ascending=False)
