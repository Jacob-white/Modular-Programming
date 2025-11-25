import pandas as pd
import numpy as np
import random
from typing import List, Dict

def generate_advisors(num_advisors: int = 50) -> pd.DataFrame:
    """
    Generates a DataFrame of mock advisors.
    """
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Jessica', 'William', 'Ashley']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    firms = ['Merrill Lynch', 'Morgan Stanley', 'UBS', 'Wells Fargo', 'LPL Financial', 'Edward Jones']
    
    advisors = []
    for i in range(num_advisors):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        
        # Generate semi-realistic zip codes
        zip_prefix = random.choice(['100', '200', '300', '400', '500', '600', '700', '800', '900'])
        zip_suffix = f"{random.randint(10, 99):02d}"
        zip_code = f"{zip_prefix}{zip_suffix}"
        
        advisors.append({
            'AdvisorID': i + 1,
            'AdvisorName': name,
            'Firm': random.choice(firms),
            'ZipCode': zip_code,
            'Email': f"{first.lower()}.{last.lower()}@example.com",
            'Latitude': round(random.uniform(25.0, 48.0), 4), # US Latitudes
            'Longitude': round(random.uniform(-125.0, -67.0), 4) # US Longitudes
        })
        
    return pd.DataFrame(advisors)

def generate_sales_data(advisor_df: pd.DataFrame, num_records: int = 200) -> pd.DataFrame:
    """
    Generates mock sales transactions linked to advisors.
    """
    products = ['Growth Fund', 'Income Fund', 'Balanced Fund', 'Global Equity', 'Bond Fund']
    
    sales = []
    advisor_ids = advisor_df['AdvisorID'].tolist()
    
    for _ in range(num_records):
        advisor_id = random.choice(advisor_ids)
        amount = round(random.uniform(5000, 500000), 2)
        is_redemption = random.random() < 0.2 # 20% chance of redemption
        
        sales.append({
            'AdvisorID': advisor_id,
            'Product': random.choice(products),
            'TransactionDate': pd.Timestamp('2024-01-01') + pd.Timedelta(days=random.randint(0, 364)),
            'Amount': -amount if is_redemption else amount,
            'TransactionType': 'Redemption' if is_redemption else 'Purchase'
        })
        
    return pd.DataFrame(sales)

def generate_activities(advisor_df: pd.DataFrame, num_activities: int = 100) -> pd.DataFrame:
    """
    Generates mock CRM activities.
    """
    activity_types = ['Call', 'Meeting', 'Email', 'Webinar']
    
    activities = []
    advisor_ids = advisor_df['AdvisorID'].tolist()
    
    for _ in range(num_activities):
        activities.append({
            'AdvisorID': random.choice(advisor_ids),
            'ActivityType': random.choice(activity_types),
            'ActivityDate': pd.Timestamp('2024-01-01') + pd.Timedelta(days=random.randint(0, 364)),
            'Notes': 'Discussed market outlook.'
        })
        
    return pd.DataFrame(activities)

def generate_territory_mapping() -> pd.DataFrame:
    """
    Generates a simple zip-to-territory mapping.
    """
    mapping = []
    # Map 100xx to Northeast, 200xx to Mid-Atlantic, etc.
    # Simplified for demo
    regions = {
        '1': 'Northeast', '2': 'Mid-Atlantic', '3': 'Southeast', 
        '4': 'Midwest', '5': 'Midwest', '6': 'Central', 
        '7': 'South', '8': 'Mountain', '9': 'West'
    }
    wholesalers = {
        'Northeast': 'Mike Ross', 'Mid-Atlantic': 'Harvey Specter', 'Southeast': 'Louis Litt',
        'Midwest': 'Donna Paulsen', 'Central': 'Rachel Zane', 'South': 'Jessica Pearson',
        'Mountain': 'Alex Williams', 'West': 'Samantha Wheeler'
    }
    
    # Generate a range of zips
    for prefix, region in regions.items():
        for i in range(100): # 00-99
            zip_code = f"{prefix}00{i:02d}"
            mapping.append({
                'ZipCode': zip_code,
                'Territory': region,
                'Wholesaler': wholesalers.get(region, 'Unknown')
            })
            
    return pd.DataFrame(mapping)
