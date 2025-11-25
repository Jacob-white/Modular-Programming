import pandas as pd
import os
from src.core.logger import logger
from src.processing.cleaner import clean_dataframe
from src.analytics.territory import TerritoryManager
from src.analytics.sales import calculate_net_flows, summarize_sales_by_territory
from src.reporting.exporter import export_to_csv

def main():
    logger.info("Starting Asset Management Analytics Tool...")

    # 1. Mock Data Creation (In a real scenario, this would come from DB/CRM)
    logger.info("Generating mock data...")
    sales_data = pd.DataFrame({
        'AdvisorName': ['john doe', 'JANE SMITH', 'bob jones', '  alice wonderland  '],
        'ZipCode': ['12345', '67890-1234', '12345', '99999'],
        'GrossSales': [100000, 250000, 50000, 75000],
        'Redemptions': [10000, 50000, 5000, 0],
        'Email': ['john@example.com', 'jane.smith@firm.com', 'invalid-email', 'alice@wonderland.net']
    })

    territory_map = pd.DataFrame({
        'ZipCode': ['12345', '67890', '99999'],
        'Territory': ['Northeast', 'Midwest', 'West'],
        'Wholesaler': ['Mike Ross', 'Harvey Specter', 'Louis Litt']
    })
    
    # Save mock territory map to CSV to demonstrate loading
    territory_map.to_csv('territory_map.csv', index=False)

    # 2. Data Cleaning
    logger.info("Cleaning data...")
    cleaned_df = clean_dataframe(
        sales_data, 
        zip_col='ZipCode', 
        name_col='AdvisorName', 
        email_col='Email'
    )
    
    # 3. Territory Assignment
    logger.info("Assigning territories...")
    tm = TerritoryManager()
    tm.load_mapping_from_csv('territory_map.csv')
    enriched_df = tm.assign_territory(cleaned_df, zip_col='ZipCode')
    
    # 4. Analytics
    logger.info("Running analytics...")
    enriched_df['NetFlows'] = calculate_net_flows(enriched_df, 'GrossSales', 'Redemptions')
    
    territory_summary = summarize_sales_by_territory(enriched_df, 'Territory', 'NetFlows')
    print("\nSales Summary by Territory:")
    print(territory_summary)

    # 5. Reporting
    logger.info("Exporting reports...")
    export_to_csv(enriched_df, 'enriched_sales_report.csv')
    
    logger.info("Process completed successfully.")

    # Cleanup
    if os.path.exists('territory_map.csv'):
        os.remove('territory_map.csv')
    if os.path.exists('enriched_sales_report.csv'):
        os.remove('enriched_sales_report.csv')

if __name__ == "__main__":
    main()
