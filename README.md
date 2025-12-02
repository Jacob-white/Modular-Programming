# Asset Management Distribution Analytics Tools

A modular Python library designed for Business and Data Analytics in the Asset Management Distribution space. This toolkit provides reusable components for database connections, data cleaning, territory management, and sales reporting.

## Features

- **Core Utilities**: Centralized configuration and standardized logging.
- **Data Connectors**:
  - SQL Server (via `pyodbc`)
  - PostgreSQL (via `psycopg2`)
  - Salesforce (via `simple-salesforce`)
- **Data Processing**:
  - Advisor name standardization
  - Zip code cleaning (5-digit standard)
  - Email validation
- **Analytics**:
  - Territory assignment based on Zip Code mapping
  - Net Flows and Market Share calculations
  - Sales summarization by territory and advisor
  - **New**: Geospatial analysis (nearest wholesaler)
  - **New**: Advisor segmentation (deciles, tiers)
  - **New**: Goal tracking and product mix analysis
- **Enrichment**: Mock external data integration.
- **Automation**: Email sending and task scheduling.
- **Reporting**: Export to CSV, Excel, and HTML.
- **Utilities**: Date calculations, currency conversion, and caching.
- **Sample Data**: Built-in generator for realistic mock data (Advisors, Sales, Activities).

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory with your credentials:

```env
# Option 1: Full Connection String
SQL_SERVER_CONN_STR="mssql+pyodbc://user:pass@host/db?driver=ODBC+Driver+17+for+SQL+Server"

# Option 2: Trusted Connection (Windows Auth)
SQL_SERVER_HOST="localhost"
SQL_SERVER_DB="MyDatabase"
SQL_SERVER_TRUSTED_CONNECTION="True"

POSTGRES_CONN_STR="postgresql+psycopg2://user:pass@host/db"
SF_USERNAME="your_username"
SF_PASSWORD="your_password"
SF_TOKEN="your_security_token"
LOG_LEVEL="INFO"
```

## Usage

See `main.py` for a basic example of how to use the library.

```bash
python3 main.py
```

For a more comprehensive demonstration of advanced features (Geospatial, Product Analytics, Automation), run:

```bash
python3 advanced_demo.py
```

## Testing

To run the test suite, install the dependencies and run `pytest`:

```bash
pip install -r requirements.txt
pytest tests/
```

## Project Structure

```
src/
├── core/           # Config and Logging
├── connectors/     # DB and CRM connectors
├── processing/     # Data cleaning functions
├── analytics/      # Business logic (Sales, Territory)
└── reporting/      # Export utilities
```
