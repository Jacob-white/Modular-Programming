import pandas as pd

def segment_advisors_by_decile(df: pd.DataFrame, metric_col: str, num_deciles: int = 10) -> pd.DataFrame:
    """
    Segments advisors into deciles based on a metric (e.g., Gross Sales).
    Decile 1 is the top performing group.
    """
    df_seg = df.copy()
    df_seg['Decile'] = pd.qcut(df_seg[metric_col], num_deciles, labels=False, duplicates='drop')
    # qcut gives 0 for lowest values, we want 1 for highest.
    # So if we want 1 to be top, we need to reverse.
    # Actually qcut 0 is lowest quantile.
    # Let's just reverse the labels or subtract from num_deciles.
    df_seg['Decile'] = num_deciles - df_seg['Decile']
    return df_seg

def assign_tier(value: float, thresholds: dict) -> str:
    """
    Assigns a tier (Gold, Silver, Bronze) based on value and thresholds.
    thresholds = {'Gold': 1000000, 'Silver': 500000, 'Bronze': 0}
    """
    for tier, threshold in thresholds.items():
        if value >= threshold:
            return tier
    return 'None'

def segment_advisors_by_tier(df: pd.DataFrame, metric_col: str, thresholds: dict) -> pd.DataFrame:
    """
    Segments advisors into named tiers.
    """
    df_seg = df.copy()
    # Sort thresholds by value desc to ensure correct assignment
    sorted_thresholds = dict(sorted(thresholds.items(), key=lambda item: item[1], reverse=True))
    
    df_seg['Tier'] = df_seg[metric_col].apply(lambda x: assign_tier(x, sorted_thresholds))
    return df_seg
