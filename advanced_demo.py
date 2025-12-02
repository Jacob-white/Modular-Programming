import pandas as pd
import numpy as np
import time
from src.core.logger import logger
from src.utils.data_generator import generate_contacts, generate_reps, generate_firms, generate_sales_data, generate_activities
from src.analytics.geospatial import find_nearest_wholesaler
from src.analytics.product import analyze_product_mix
from src.analytics.crm_activity import summarize_activity_by_type, correlate_activity_sales
from src.utils.currency import convert_currency, format_currency
from src.automation.emailer import Emailer
from src.automation.scheduler import schedule_daily_report

def main():
    logger.info("Starting Advanced Analytics Demo...")

    # 1. Generate Data
    logger.info("Generating rich sample data...")
    contacts = generate_contacts(100)
    firms = generate_firms(10)
    reps = generate_reps(contacts, firms)
    sales = generate_sales_data(reps, 1000)
    activities = generate_activities(reps, 500)
    
    # Merge Reps with Contacts for full profile (optional, but good for display)
    full_reps = pd.merge(reps, contacts, on='CONTACT_ID')

    # 2. Geospatial Analysis: Find Nearest Wholesaler
    logger.info("Running Geospatial Analysis...")
    # Find nearest wholesaler for each advisor
    # Note: In new schema, we might use ZIP_CODE or existing Lat/Lon
    # For demo, let's assume we have Lat/Lon derived from Zip (mocked here)
    full_reps['Latitude'] = np.random.uniform(25.0, 48.0, size=len(full_reps))
    full_reps['Longitude'] = np.random.uniform(-125.0, -67.0, size=len(full_reps))
    
    # We need a mock wholesaler dataframe with Lat/Lon
    wholesalers_df = pd.DataFrame([
        {'Name': 'Mike Ross', 'Latitude': 40.7128, 'Longitude': -74.0060}, # NY
        {'Name': 'Harvey Specter', 'Latitude': 38.9072, 'Longitude': -77.0369}, # DC
        {'Name': 'Samantha Wheeler', 'Latitude': 34.0522, 'Longitude': -118.2437}, # LA
    ])
    
    full_reps['NearestWholesaler'] = full_reps.apply(
        lambda row: find_nearest_wholesaler(row['Latitude'], row['Longitude'], wholesalers_df)['Name'],
        axis=1
    )
    logger.info("Nearest wholesalers assigned.")

    # 3. Product Analytics
    logger.info("Running Product Analytics...")
    # Analyze product mix
    product_mix = analyze_product_mix(sales, 'PRODUCT_CODE', 'GROSS_AMOUNT')
    logger.info(f"Product Mix:\n{product_mix}")

    # 4. CRM Activity Analysis
    logger.info("Running CRM Activity Analysis...")
    activity_summary = summarize_activity_by_type(activities, 'ActivityType')
    logger.info(f"Activity Summary:\n{activity_summary}")
    
    # Correlate Activity with Sales
    # Need to aggregate sales by CONTACT_ID first
    sales_by_rep = sales.groupby('CONTACT_ID')['GROSS_AMOUNT'].sum().reset_index()
    activity_by_rep = activities.groupby('CONTACT_ID').size().reset_index(name='ActivityCount')
    
    correlation = correlate_activity_sales(
        activity_by_rep, 
        sales_by_rep, 
        'CONTACT_ID', 
        'ActivityCount', 
        'GROSS_AMOUNT'
    )
    logger.info(f"Correlation between Activity and Sales: {correlation:.2f}")

    # 5. Currency Conversion
    logger.info("Demonstrating Currency Conversion...")
    total_sales_usd = sales['GROSS_AMOUNT'].sum()
    total_sales_eur = convert_currency(total_sales_usd, 'USD', 'EUR')
    total_sales_gbp = convert_currency(total_sales_usd, 'USD', 'GBP')
    
    logger.info(f"Total Sales (USD): {format_currency(total_sales_usd, 'USD')}")
    logger.info(f"Total Sales (EUR): {format_currency(total_sales_eur, 'EUR')}")
    logger.info(f"Total Sales (GBP): {format_currency(total_sales_gbp, 'GBP')}")

    # 6. Automation Workflow
    logger.info("Demonstrating Automation Workflow...")
    
    # 7. Robustness: Validation and Reporting
    logger.info("Demonstrating Robustness Modules (Validation & Reporting)...")
    
    from src.processing.validator import DataValidator
    from src.core.models import TransactionHistory, RepProfile
        
    # Validate Sales Data
    try:
        # Validate against new Pydantic model
        # Note: validating 1000 rows might be verbose if errors, but good for demo
        # DataValidator.validate_dataframe(sales, TransactionHistory) 
        DataValidator.check_required_columns(sales, ['TRANSACTION_ID', 'CONTACT_ID', 'PRODUCT_CODE', 'GROSS_AMOUNT'])
        logger.info("Sales data schema validation passed.")
    except Exception as e:
        logger.error(f"Validation failed: {e}")

    # Generate Excel Report with Charts
    from src.reporting.excel_generator import generate_excel_report
    from src.visualization.charts import generate_bar_chart
    
    # Create a chart
    chart_img = generate_bar_chart(product_mix, 'PRODUCT_CODE', 'GROSS_AMOUNT', title="Sales by Product")
    
    generate_excel_report(
        dataframes={
            'Sales Summary': product_mix,
            'Activity Summary': activity_summary,
            'Advisors': full_reps.head(50) # Limit for demo
        },
        file_path="Advanced_Report.xlsx",
        charts={'Sales Summary': chart_img}
    )
    
    def job():
        logger.info("Executing scheduled job: Sending Daily Sales Report...")
        emailer = Emailer("smtp.example.com", 587, "bot@synfinii.com", "secret")
        # Mock sending email
        emailer.send_email("jacob.samuel.white@gmail.com", "Daily Sales Report", f"Total Sales today: {format_currency(total_sales_usd)}\nReport generated: Advanced_Report.xlsx")
    
    # Schedule it (Mock run)
    schedule_daily_report(job, "09:00")
    logger.info("Job scheduled. Running pending jobs now for demo purposes...")
    # Force run for demo
    job()

    logger.info("Advanced Demo Completed.")

if __name__ == "__main__":
    main()
