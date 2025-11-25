import pandas as pd

def analyze_product_mix(df: pd.DataFrame, product_col: str, sales_col: str) -> pd.DataFrame:
    """
    Calculates the percentage of total sales for each product.
    """
    total_sales = df[sales_col].sum()
    mix = df.groupby(product_col)[sales_col].sum().reset_index()
    mix['MixPercent'] = (mix[sales_col] / total_sales) * 100
    return mix.sort_values(by='MixPercent', ascending=False)

def group_by_asset_class(df: pd.DataFrame, asset_class_col: str, sales_col: str) -> pd.DataFrame:
    """
    Aggregates sales by asset class.
    """
    return df.groupby(asset_class_col)[sales_col].sum().reset_index().sort_values(by=sales_col, ascending=False)
