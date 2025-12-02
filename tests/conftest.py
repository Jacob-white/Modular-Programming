import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_contacts():
    return pd.DataFrame([
        {'CONTACT_ID': '1', 'FIRST_NAME': 'John', 'LAST_NAME': 'Doe', 'EMAIL_ADDRESS': 'john@example.com'},
        {'CONTACT_ID': '2', 'FIRST_NAME': 'Jane', 'LAST_NAME': 'Smith', 'EMAIL_ADDRESS': 'jane@example.com'},
        {'CONTACT_ID': '3', 'FIRST_NAME': 'Bob', 'LAST_NAME': 'Jones', 'EMAIL_ADDRESS': 'bob@example.com'}
    ])

@pytest.fixture
def sample_reps():
    return pd.DataFrame([
        {'CONTACT_ID': '1', 'FIRM_ID': 'F001', 'ZIP_CODE': '10001', 'CHANNEL': 'Wirehouse', 'TERR1': 'Northeast'},
        {'CONTACT_ID': '2', 'FIRM_ID': 'F001', 'ZIP_CODE': '20001', 'CHANNEL': 'Independent', 'TERR1': 'Mid-Atlantic'},
        {'CONTACT_ID': '3', 'FIRM_ID': 'F002', 'ZIP_CODE': '90001', 'CHANNEL': 'RIA', 'TERR1': 'West'}
    ])

@pytest.fixture
def sample_sales():
    return pd.DataFrame([
        {'TRANSACTION_ID': 'T1', 'CONTACT_ID': '1', 'PRODUCT_CODE': 'Fund A', 'GROSS_AMOUNT': 10000, 'TRANSACTION_TYPE': 'Purchase'},
        {'TRANSACTION_ID': 'T2', 'CONTACT_ID': '2', 'PRODUCT_CODE': 'Fund B', 'GROSS_AMOUNT': 20000, 'TRANSACTION_TYPE': 'Purchase'},
        {'TRANSACTION_ID': 'T3', 'CONTACT_ID': '1', 'PRODUCT_CODE': 'Fund A', 'GROSS_AMOUNT': 5000, 'TRANSACTION_TYPE': 'Purchase'},
        {'TRANSACTION_ID': 'T4', 'CONTACT_ID': '3', 'PRODUCT_CODE': 'Fund C', 'GROSS_AMOUNT': 15000, 'TRANSACTION_TYPE': 'Purchase'},
        {'TRANSACTION_ID': 'T5', 'CONTACT_ID': '2', 'PRODUCT_CODE': 'Fund B', 'GROSS_AMOUNT': -5000, 'TRANSACTION_TYPE': 'Redemption'}
    ])

@pytest.fixture
def sample_activities():
    return pd.DataFrame([
        {'CONTACT_ID': '1', 'ActivityType': 'Call', 'Date': '2024-01-01'},
        {'CONTACT_ID': '2', 'ActivityType': 'Meeting', 'Date': '2024-01-02'},
        {'CONTACT_ID': '1', 'ActivityType': 'Email', 'Date': '2024-01-03'}
    ])

@pytest.fixture
def sample_territory_mapping():
    return pd.DataFrame([
        {'ZipCode': '10001', 'Territory': 'Northeast', 'Wholesaler': 'Mike Ross'},
        {'ZipCode': '20001', 'Territory': 'Mid-Atlantic', 'Wholesaler': 'Harvey Specter'},
        {'ZipCode': '90001', 'Territory': 'West', 'Wholesaler': 'Samantha Wheeler'}
    ])
