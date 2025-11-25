import pandas as pd
import numpy as np
import time
from src.core.logger import logger
from src.utils.data_generator import generate_advisors, generate_sales_data, generate_activities
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
    advisors = generate_advisors(100)
    sales = generate_sales_data(advisors, 1000)
    activities = generate_activities(advisors, 500)

    # 2. Geospatial Analysis: Find Nearest Wholesaler
    logger.info("Running Geospatial Analysis...")
    # Mock Wholesaler locations
    wholesalers = pd.DataFrame([
        {'Name': 'Mike Ross (NY)', 'Latitude': 40.7128, 'Longitude': -74.0060},
        {'Name': 'Harvey Specter (Chi)', 'Latitude': 41.8781, 'Longitude': -87.6298},
        {'Name': 'Louis Litt (LA)', 'Latitude': 34.0522, 'Longitude': -118.2437},
        {'Name': 'Jessica Pearson (Mia)', 'Latitude': 25.7617, 'Longitude': -80.1918}
    ])
    
    # Assign nearest wholesaler to each advisor
    # This might be slow for many advisors, so we demonstrate on a subset or just run it
    start_time = time.time()
    advisors['NearestWholesaler'] = advisors.apply(
        lambda row: find_nearest_wholesaler(row['Latitude'], row['Longitude'], wholesalers)['Name'], axis=1
    )
    logger.info(f"Assigned wholesalers in {time.time() - start_time:.2f} seconds.")
    print("\nSample Advisor Wholesaler Assignments:")
    print(advisors[['AdvisorName', 'ZipCode', 'NearestWholesaler']].head())

    # 3. Product Analytics
    logger.info("Running Product Analytics...")
    product_mix = analyze_product_mix(sales, 'Product', 'Amount')
    print("\nProduct Mix:")
    print(product_mix)

    # 4. CRM Activity Analysis
    logger.info("Running CRM Activity Analysis...")
    activity_summary = summarize_activity_by_type(activities, 'ActivityType')
    print("\nActivity Summary:")
    print(activity_summary)

    # Correlation
    # Aggregate sales and activity by advisor
    sales_by_advisor = sales.groupby('AdvisorID')['Amount'].sum().reset_index().rename(columns={'Amount': 'TotalSales'})
    activity_by_advisor = activities.groupby('AdvisorID').size().reset_index(name='ActivityCount')
    
    correlation = correlate_activity_sales(activity_by_advisor, sales_by_advisor, 'AdvisorID', 'ActivityCount', 'TotalSales')
    logger.info(f"Correlation between Activity Count and Total Sales: {correlation:.4f}")

    # 5. Currency Conversion
    logger.info("Demonstrating Currency Conversion...")
    total_sales_usd = sales['Amount'].sum()
    total_sales_eur = convert_currency(total_sales_usd, 'USD', 'EUR')
    total_sales_gbp = convert_currency(total_sales_usd, 'USD', 'GBP')
    
    print(f"\nTotal Sales (USD): {format_currency(total_sales_usd, 'USD')}")
    print(f"Total Sales (EUR): {format_currency(total_sales_eur, 'EUR')}")
    print(f"Total Sales (GBP): {format_currency(total_sales_gbp, 'GBP')}")

    # 6. Automation Workflow
    logger.info("Demonstrating Automation Workflow...")
    
    def job():
        logger.info("Executing scheduled job: Sending Daily Sales Report...")
        emailer = Emailer("smtp.example.com", 587, "bot@synfinii.com", "secret")
        # Mock sending email
        emailer.send_email("jacob.samuel.white@gmail.com", "Daily Sales Report", f"Total Sales today: {format_currency(total_sales_usd)}")
    
    # Schedule it (Mock run)
    schedule_daily_report(job, "09:00")
    logger.info("Job scheduled. Running pending jobs now for demo purposes...")
    # Force run for demo
    job()

    logger.info("Advanced Demo Completed.")

if __name__ == "__main__":
    main()
