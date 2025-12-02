import pandas as pd
import numpy as np
import random
from typing import List, Dict
import uuid

def generate_advisors(num_advisors: int = 50) -> pd.DataFrame:
    """
    Generates a DataFrame of mock advisors matching RepProfile schema.
    """
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Jessica', 'William', 'Ashley']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    # Mock Firms
    firms = [
        {'FIRM_ID': 'F001', 'FIRM_NAME': 'Merrill Lynch'},
        {'FIRM_ID': 'F002', 'FIRM_NAME': 'Morgan Stanley'},
        {'FIRM_ID': 'F003', 'FIRM_NAME': 'UBS'},
        {'FIRM_ID': 'F004', 'FIRM_NAME': 'Wells Fargo'}
    ]
    
from datetime import date, timedelta

def generate_contacts(num_contacts: int = 100) -> pd.DataFrame:
    """
    Generates mock Contact data.
    """
    contacts = []
    for i in range(1, num_contacts + 1):
        contacts.append({
            'CONTACT_ID': str(i),
            'FIRST_NAME': f"FirstName{i}",
            'LAST_NAME': f"LastName{i}",
            'EMAIL_ADDRESS': f"advisor{i}@example.com"
        })
    return pd.DataFrame(contacts)

def generate_reps(contacts_df: pd.DataFrame, firms_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates mock RepProfile data linked to Contacts.
    """
    reps = []
    firm_ids = firms_df['FIRM_ID'].tolist()
    channels = ['Wirehouse', 'Independent', 'RIA', 'Bank']
    
    for _, contact in contacts_df.iterrows():
        reps.append({
            'CONTACT_ID': contact['CONTACT_ID'],
            'FIRM_ID': np.random.choice(firm_ids),
            'OFFICE_ID': f"OFF{np.random.randint(100, 999)}",
            'CHANNEL': np.random.choice(channels),
            'SUB_CHANNEL': 'General',
            'CRD_NUMBER': str(np.random.randint(1000000, 9999999)),
            'ZIP_CODE': f"{np.random.randint(10000, 99999)}",
            'TERR1': np.random.choice(['Northeast', 'Southeast', 'Midwest', 'West']),
            'TERR2': np.random.choice(['A', 'B', 'C']),
            # Add other territories as None or random
        })
    return pd.DataFrame(reps)

def generate_firms(num_firms: int = 10) -> pd.DataFrame:
    """
    Generates mock Firm data.
    """
    firms = []
    types = ['National', 'Regional', 'Boutique']
    for i in range(1, num_firms + 1):
        firms.append({
            'FIRM_ID': f"F{i:03d}",
            'FIRM_NAME': f"Firm {i}",
            'FIRM_TYPE': np.random.choice(types),
            'CRD_NUMBER': str(np.random.randint(100000, 999999))
        })
    return pd.DataFrame(firms)

def generate_sales_data(reps_df: pd.DataFrame, num_transactions: int = 1000) -> pd.DataFrame:
    """
    Generates mock sales transactions.
    """
    transactions = []
    contact_ids = reps_df['CONTACT_ID'].tolist()
    products = ['Fund A', 'Fund B', 'Fund C', 'ETF X', 'ETF Y']
    
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    days_range = (end_date - start_date).days
    
    for i in range(1, num_transactions + 1):
        random_days = np.random.randint(0, days_range)
        txn_date = start_date + timedelta(days=random_days)
        
        transactions.append({
            'TRANSACTION_ID': f"T{i}",
            'TRANSACTION_DATE': txn_date,
            'CONTACT_ID': np.random.choice(contact_ids),
            'FIRM_ID': None, # Can be joined from RepProfile
            'PRODUCT_CODE': np.random.choice(products),
            'CUSIP': f"CUSIP{np.random.randint(1000, 9999)}",
            'GROSS_AMOUNT': round(np.random.uniform(-5000, 50000), 2),
            'TRANSACTION_TYPE': 'Purchase' if np.random.random() > 0.2 else 'Redemption'
        })
    return pd.DataFrame(transactions)

def generate_activities(reps_df: pd.DataFrame, num_activities: int = 500) -> pd.DataFrame:
    """
    Generates mock CRM activities.
    """
    activities = []
    contact_ids = reps_df['CONTACT_ID'].tolist()
    types = ['Call', 'Meeting', 'Email', 'Webinar']
    
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    days_range = (end_date - start_date).days
    
    for _ in range(num_activities):
        random_days = np.random.randint(0, days_range)
        act_date = start_date + timedelta(days=random_days)
        
        activities.append({
            'CONTACT_ID': np.random.choice(contact_ids), # Renamed from REP_ID
            'ActivityType': np.random.choice(types),
            'Date': act_date,
            'Subject': 'Follow up',
            'Notes': 'Discussed new fund launch'
        })
    return pd.DataFrame(activities)

def generate_territory_mapping(num_zips: int = 50) -> pd.DataFrame:
    """
    Generates mock Zip Code to Territory mapping.
    """
    mapping = []
    territories = ['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest']
    wholesalers = ['Mike Ross', 'Harvey Specter', 'Samantha Wheeler', 'Louis Litt', 'Donna Paulsen']
    
    for _ in range(num_zips):
        mapping.append({
            'ZipCode': f"{np.random.randint(10000, 99999)}",
            'Territory': np.random.choice(territories),
            'Wholesaler': np.random.choice(wholesalers)
        })
    return pd.DataFrame(mapping)
