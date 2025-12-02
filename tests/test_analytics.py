import pytest
import pandas as pd
from src.analytics.geospatial import haversine_distance, find_nearest_wholesaler
from src.analytics.segmentation import segment_advisors_by_decile, segment_advisors_by_tier
from src.analytics.goals import calculate_percent_to_goal, calculate_gap_to_goal
from src.analytics.product import analyze_product_mix
from src.analytics.crm_activity import summarize_activity_by_type, correlate_activity_sales
from src.analytics.sales import calculate_net_flows, summarize_sales_by_territory
from src.analytics.territory import TerritoryManager

# Geospatial Tests
def test_calculate_haversine_distance():
    # NY to LA approx 3935 km, which is approx 2445 miles
    ny_lat, ny_lon = 40.7128, -74.0060
    la_lat, la_lon = 34.0522, -118.2437
    dist = haversine_distance(ny_lat, ny_lon, la_lat, la_lon)
    # Allow some margin of error
    assert 2400 < dist < 2500

def test_find_nearest_wholesaler():
    wholesalers = pd.DataFrame([
        {'Name': 'NY Rep', 'Latitude': 40.7128, 'Longitude': -74.0060},
        {'Name': 'LA Rep', 'Latitude': 34.0522, 'Longitude': -118.2437}
    ])
    # Chicago is closer to NY than LA
    chi_lat, chi_lon = 41.8781, -87.6298
    nearest = find_nearest_wholesaler(chi_lat, chi_lon, wholesalers)
    assert nearest['Name'] == 'NY Rep'

# Segmentation Tests
def test_segment_advisors_decile(sample_sales):
    # Aggregate sales first
    advisor_sales = sample_sales.groupby('CONTACT_ID')['GROSS_AMOUNT'].sum().reset_index()
    segmented = segment_advisors_by_decile(advisor_sales, 'GROSS_AMOUNT')
    assert 'Decile' in segmented.columns

def test_segment_advisors_tier(sample_sales):
    advisor_sales = sample_sales.groupby('CONTACT_ID')['GROSS_AMOUNT'].sum().reset_index()
    segmented = segment_advisors_by_tier(advisor_sales, 'GROSS_AMOUNT', thresholds={'Gold': 14000, 'Silver': 5000})
    assert 'Tier' in segmented.columns
    # Check specific IDs (as strings now)
    assert segmented.loc[segmented['CONTACT_ID'] == '2', 'Tier'].iloc[0] == 'Gold' 
    assert segmented.loc[segmented['CONTACT_ID'] == '1', 'Tier'].iloc[0] == 'Gold' 
    assert segmented.loc[segmented['CONTACT_ID'] == '3', 'Tier'].iloc[0] == 'Gold' 

# Goal Tests
def test_calculate_percent_to_goal():
    assert calculate_percent_to_goal(50, 100) == 50.0
    assert calculate_percent_to_goal(0, 100) == 0.0
    assert calculate_percent_to_goal(100, 0) == 0.0 # Avoid div by zero

def test_calculate_gap_to_goal():
    assert calculate_gap_to_goal(50, 100) == 50
    # If actual > goal, gap is negative (surpassed goal)
    assert calculate_gap_to_goal(110, 100) == -10

# Product Tests
def test_analyze_product_mix(sample_sales):
    mix = analyze_product_mix(sample_sales, 'PRODUCT_CODE', 'GROSS_AMOUNT')
    assert 'Fund A' in mix['PRODUCT_CODE'].values
    # Fund A: 10000 + 5000 = 15000
    assert mix.loc[mix['PRODUCT_CODE'] == 'Fund A', 'GROSS_AMOUNT'].iloc[0] == 15000

# CRM Activity Tests
def test_summarize_activity_by_type(sample_activities):
    summary = summarize_activity_by_type(sample_activities, 'ActivityType')
    assert len(summary) == 3
    assert summary.loc[summary['ActivityType'] == 'Call', 'Count'].iloc[0] == 1

def test_correlate_activity_sales(sample_activities, sample_sales):
    # Aggregate activities by CONTACT_ID
    activity_counts = sample_activities.groupby('CONTACT_ID').size().reset_index(name='ActivityCount')
    # Aggregate sales by CONTACT_ID
    sales_sums = sample_sales.groupby('CONTACT_ID')['GROSS_AMOUNT'].sum().reset_index()
    
    corr = correlate_activity_sales(activity_counts, sales_sums, 'CONTACT_ID', 'ActivityCount', 'GROSS_AMOUNT')
    assert isinstance(corr, float)

# Sales Tests
def test_calculate_net_flows():
    df = pd.DataFrame({
        'Sales': [100, 50, 25],
        'Redemptions': [10, 5, 0]
    })
    net = calculate_net_flows(df, 'Sales', 'Redemptions')
    assert net.iloc[0] == 90
    assert net.iloc[1] == 45

def test_summarize_sales_by_territory(sample_sales, sample_reps, sample_territory_mapping):
    # 1. Merge reps with territory map
    reps_with_terr = pd.merge(sample_reps, sample_territory_mapping, left_on='ZIP_CODE', right_on='ZipCode')
    
    # 2. Merge sales with reps
    sales_with_terr = pd.merge(sample_sales, reps_with_terr, on='CONTACT_ID')
    
    summary = summarize_sales_by_territory(sales_with_terr, 'Territory', 'GROSS_AMOUNT')
    assert 'Territory' in summary.columns
    assert 'GROSS_AMOUNT' in summary.columns

# Territory Tests
def test_map_territories(sample_sales):
    # Create a mock mapping dataframe
    mapping_data = {
        'ZipCode': ['10001', '20001', '90001', '60601', '33101'],
        'Territory': ['Northeast', 'Mid-Atlantic', 'West', 'Midwest', 'Southeast'],
        'Wholesaler': ['Mike Ross', 'Harvey Specter', 'Samantha Wheeler', 'Louis Litt', 'Donna Paulsen']
    }
    mapping_df = pd.DataFrame(mapping_data)
    
    manager = TerritoryManager(mapping_df)
    
    # Add ZipCode to sample_sales if not present (it is in our fixture)
    # Ensure ZipCode is string
    sample_sales['ZIP_CODE'] = ['10001', '20001', '10001', '90001', '20001']
    sample_sales['ZIP_CODE'] = sample_sales['ZIP_CODE'].astype(str)
    
    mapped_sales = manager.assign_territory(sample_sales, 'ZIP_CODE')
    
    # Check a specific mapping
    ny_sale = mapped_sales[mapped_sales['ZIP_CODE'] == '10001']
    if not ny_sale.empty:
        assert ny_sale.iloc[0]['Territory'] == 'Northeast'
