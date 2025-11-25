import pandas as pd
import os
from src.core.logger import logger
from src.processing.cleaner import clean_dataframe
from src.analytics.territory import TerritoryManager
from src.analytics.sales import calculate_net_flows, summarize_sales_by_territory
from src.reporting.exporter import export_to_csv
from src.utils.date_utils import get_fiscal_year_and_quarter
from src.analytics.segmentation import segment_advisors_by_decile
from src.analytics.goals import track_goals
from src.enrichment.external_data import ExternalDataEnricher
from src.reporting.html_generator import generate_html_report

def main():
    logger.info("Starting Asset Management Analytics Tool...")

    # 1. Mock Data Creation
    logger.info("Generating mock data...")
    sales_data = pd.DataFrame({
        'AdvisorName': ['john doe', 'JANE SMITH', 'bob jones', 'alice wonderland', 'tom cruise'],
        'ZipCode': ['12345', '67890-1234', '12345', '99999', '12345'],
        'GrossSales': [100000, 250000, 50000, 75000, 500000],
        'Redemptions': [10000, 50000, 5000, 0, 20000],
        'SalesGoal': [150000, 300000, 100000, 100000, 600000],
        'Email': ['john@example.com', 'jane.smith@firm.com', 'invalid-email', 'alice@wonderland.net', 'tom@topgun.com']
    })

    territory_map = pd.DataFrame({
        'ZipCode': ['12345', '67890', '99999'],
        'Territory': ['Northeast', 'Midwest', 'West'],
        'Wholesaler': ['Mike Ross', 'Harvey Specter', 'Louis Litt']
    })
    
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
    
    # New Analytics: Goals and Segmentation
    logger.info("Running advanced analytics...")
    enriched_df = track_goals(enriched_df, 'GrossSales', 'SalesGoal')
    enriched_df = segment_advisors_by_decile(enriched_df, 'GrossSales', num_deciles=3) # Using 3 for small dataset
    
    # 5. Enrichment
    logger.info("Enriching with external data...")
    enricher = ExternalDataEnricher()
    enriched_df = enricher.enrich_advisors(enriched_df, 'AdvisorName')

    territory_summary = summarize_sales_by_territory(enriched_df, 'Territory', 'NetFlows')
    print("\nSales Summary by Territory:")
    print(territory_summary)

    # 6. Reporting
    logger.info("Exporting reports...")
    export_to_csv(enriched_df, 'enriched_sales_report.csv')
    
    # HTML Report
    html_report = generate_html_report(enriched_df, "Advisor Sales Report")
    with open('sales_report.html', 'w') as f:
        f.write(html_report)
    logger.info("HTML report generated: sales_report.html")
    
    # Date Utils Demo
    from datetime import date
    fy, q = get_fiscal_year_and_quarter(date.today())
    logger.info(f"Current Fiscal Year: {fy}, Quarter: {q}")

    logger.info("Process completed successfully.")

    # Cleanup
    if os.path.exists('territory_map.csv'):
        os.remove('territory_map.csv')
    if os.path.exists('enriched_sales_report.csv'):
        os.remove('enriched_sales_report.csv')
    if os.path.exists('sales_report.html'):
        os.remove('sales_report.html')

if __name__ == "__main__":
    main()
