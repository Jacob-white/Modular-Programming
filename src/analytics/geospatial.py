import numpy as np
import pandas as pd
from typing import Tuple

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    Returns distance in miles.
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    r = 3956 # Radius of earth in miles
    return c * r

def find_nearest_wholesaler(
    advisor_lat: float, 
    advisor_lon: float, 
    wholesaler_df: pd.DataFrame, 
    lat_col: str = 'Latitude', 
    lon_col: str = 'Longitude'
) -> pd.Series:
    """
    Finds the nearest wholesaler from a DataFrame of wholesalers.
    """
    distances = wholesaler_df.apply(
        lambda row: haversine_distance(advisor_lat, advisor_lon, row[lat_col], row[lon_col]), 
        axis=1
    )
    nearest_idx = distances.idxmin()
    return wholesaler_df.loc[nearest_idx]
