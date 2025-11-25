import pandas as pd
import numpy as np
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
from src.utils.data_generator import generate_advisors, generate_sales_data, generate_territory_mapping

def main():
    logger.info("Starting Asset Management Analytics Tool...")

    # 1. Mock Data Creation
    # 1. Mock Data Creation
    logger.info("Generating mock data...")
    
    # Generate Advisors
    advisors_df = generate_advisors(num_advisors=50)
    
    # Generate Sales linked to Advisors
    sales_transactions = generate_sales_data(advisors_df, num_records=500)
    
    # Aggregate sales for the main dataframe structure used previously
    # We need to pivot or aggregate transactions to get GrossSales/Redemptions per advisor for the demo flow
    sales_summary = sales_transactions.groupby(['AdvisorID', 'TransactionType'])['Amount'].sum().unstack(fill_value=0).reset_index()
    if 'Purchase' not in sales_summary.columns: sales_summary['Purchase'] = 0
    if 'Redemption' not in sales_summary.columns: sales_summary['Redemption'] = 0
    
    sales_summary.rename(columns={'Purchase': 'GrossSales', 'Redemption': 'Redemptions'}, inplace=True)
    # Redemptions are negative in transaction table, but usually positive in summary columns (Net = Gross - Redemptions)
    # The generator returns negative amounts for redemptions.
    # So sum of 'Redemption' column will be negative.
    # Let's make it positive for the column 'Redemptions'
    sales_summary['Redemptions'] = sales_summary['Redemptions'].abs()
    
    # Merge back with Advisor info
    sales_data = pd.merge(advisors_df, sales_summary, on='AdvisorID', how='left').fillna(0)
    
    # Add a mock Sales Goal
    sales_data['SalesGoal'] = np.random.randint(100000, 1000000, len(sales_data))

    # Generate Territory Map
    territory_map = generate_territory_mapping()
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
