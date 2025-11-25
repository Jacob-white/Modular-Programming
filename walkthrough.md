# Walkthrough - Asset Management Distribution Analytics Tools

I have implemented a modular Python library for your Asset Management Distribution analytics needs. This library provides a structured way to handle database connections, data cleaning, territory management, and sales reporting.

## Features Implemented

### 1. Core Utilities

- **Configuration**: Centralized settings management using `.env` files.
- **Logging**: Standardized logging to console.

### 2. Data Connectors

- **SQL Server**: Connection wrapper using `sqlalchemy` and `pyodbc`.
- **PostgreSQL**: Connection wrapper using `sqlalchemy` and `psycopg2`.
- **Salesforce**: Wrapper around `simple-salesforce` for querying CRM data.

### 3. Data Processing

- **Cleaning**: Functions to standardize advisor names, clean zip codes (5-digit standard), and validate emails.

### 4. Analytics

- **Territory Management**: Logic to assign territories and wholesalers based on zip codes using a mapping file.
- **Sales Analytics**: Functions to calculate Net Flows, Market Share, and summarize sales by territory.

### 5. Reporting

- **Export**: Utilities to export DataFrames to CSV and Excel.

## How to Use

### Prerequisites

You need to install the required Python packages. Since `pip` was not available in the current environment, please run the following command in your terminal where `pip` is installed:

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory (`Modular-Programming/.env`) with your credentials:

```env
SQL_SERVER_CONN_STR="mssql+pyodbc://user:pass@host/db?driver=ODBC+Driver+17+for+SQL+Server"
POSTGRES_CONN_STR="postgresql+psycopg2://user:pass@host/db"
SF_USERNAME="your_username"
SF_PASSWORD="your_password"
SF_TOKEN="your_security_token"
LOG_LEVEL="INFO"
```

### Running the Example

I have created a `main.py` script that demonstrates the end-to-end flow using mock data. You can run it to see the tools in action:

```bash
python3 main.py
```

This script will:

1. Generate mock sales and territory data.
2. Clean the data (standardize names, zip codes).
3. Assign territories based on the mock mapping.
4. Calculate net flows and summarize by territory.
5. Export the enriched report to `enriched_sales_report.csv`.

## Next Steps

- Integrate with your actual SQL Server / PostgreSQL databases by updating the `.env` file.
- Expand the `TerritoryManager` to load mappings from a database instead of a CSV.
- Add more complex analytics metrics as needed.
