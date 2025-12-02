# Asset Management Analytics Library Walkthrough

This walkthrough demonstrates the capabilities of the modular analytics library, including data generation, advanced analytics, and automated reporting.

## Features Implemented

1.  **Core Architecture**: Modular design with `core`, `connectors`, `processing`, `analytics`, `reporting`, `automation`, and `visualization` packages.
2.  **Data Connectors**: Support for SQL Server (Trusted Auth), PostgreSQL, and Salesforce.
3.  **Advanced Analytics**:
    - **Geospatial**: Nearest wholesaler assignment using Haversine distance.
    - **Segmentation**: Advisor tiering and decile analysis.
    - **Product**: Product mix analysis.
    - **CRM**: Activity correlation with sales.
4.  **Robustness**:
    - **Validation**: Pydantic-based schema validation for data integrity.
    - **Visualization**: Static chart generation (Bar, Line).
    - **Reporting**: Professional Excel reports with embedded charts.
5.  **Automation**: Task scheduling and email notifications.

## Phase 2: Deep Data Model Integration (Completed)

The system now fully aligns with the provided SQL schema:

- **Contact Entity**: Personal details (`FIRST_NAME`, `LAST_NAME`, `EMAIL`) are stored in a dedicated `Contact` model.
- **Rep Profile**: Linked to `Contact` via `CONTACT_ID`. Includes rich attributes like `CHANNEL`, `SUB_CHANNEL`, and `TERR` codes.
- **Transaction History**: Uses `CONTACT_ID` and includes `CUSIP`.
- **Analytics**: Updated to leverage these new fields (e.g., sales by channel, firm type).

## Verification Results

### Automated Tests

All 29 tests passed successfully, covering:

- Analytics modules (geospatial, goals, product, sales, territory, crm)
- Connectors (SQL Server, Postgres, Salesforce)
- Utilities (date, currency, cache)
- Reporting (Excel generation)
- New `Contact` and `RepProfile` schema validation.
- Analytics using `CONTACT_ID`.
- Sales summaries by Channel and Firm Type.

### Manual Verification

The `advanced_demo.py` script ran successfully, demonstrating:

1.  Data generation and validation against the new schema.
2.  Geospatial analysis (nearest wholesaler).
3.  Product mix analysis.
4.  CRM activity analysis.
5.  Excel report generation with charts.
6.  Automated email scheduling (mocked).
7.  Generation of `Contact`, `Firm`, `RepProfile`, and `TransactionHistory` data.
8.  End-to-end analytics flow using the new schema.
9.  Seamless integration with reporting and automation modules.

### Next Steps

- Deploy to a staging environment with real database connections.
- Configure actual Salesforce credentials in `.env`.
- Set up a cron job for the daily report script.

## Running the Advanced Demo

The `advanced_demo.py` script showcases the full workflow:

1.  **Data Generation**: Creates realistic mock data for Advisors, Sales, and CRM Activities.
2.  **Geospatial Analysis**: Assigns the nearest wholesaler to each advisor based on coordinates.
3.  **Analytics**: Calculates product mix and correlates CRM activity with sales performance.
4.  **Validation**: Checks data integrity using `DataValidator`.
5.  **Reporting**: Generates `Advanced_Report.xlsx` containing summary tables and a sales chart.
6.  **Automation**: Simulates sending the report via email.

### Prerequisites

Ensure you have the virtual environment set up:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Execution

Run the demo script:

```bash
./venv/bin/python advanced_demo.py
```

### Output

- **Console Logs**: Detailed logs of the analysis steps.
- **Advanced_Report.xlsx**: A multi-sheet Excel report with:
  - **Sales Summary**: Product mix data with an embedded bar chart.
  - **Activity Summary**: Breakdown of CRM activities.
  - **Advisors**: List of advisors with assigned wholesalers.

## Testing

The library includes a test suite using `pytest`.

```bash
./venv/bin/pytest tests/
```
