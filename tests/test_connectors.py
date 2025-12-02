import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from src.connectors.db_connector import SQLServerConnector, PostgresConnector
from src.connectors.crm_connector import SalesforceConnector

# DB Connector Tests
@patch('src.connectors.db_connector.settings')
def test_sql_server_connector_connection_string(mock_settings):
    mock_settings.SQL_SERVER_CONNECTION_STRING = "mssql+pyodbc://user:pass@host/db"
    mock_settings.SQL_SERVER_HOST = None
    connector = SQLServerConnector()
    assert connector.connection_string == "mssql+pyodbc://user:pass@host/db"

@patch('src.connectors.db_connector.settings')
def test_postgres_connector_connection_string(mock_settings):
    mock_settings.POSTGRES_CONNECTION_STRING = "postgresql://user:pass@localhost/testdb"
    connector = PostgresConnector()
    assert connector.connection_string == "postgresql://user:pass@localhost/testdb"

@patch('src.connectors.db_connector.create_engine')
@patch('src.connectors.db_connector.settings')
@patch('src.connectors.db_connector.pd.read_sql')
def test_execute_query(mock_read_sql, mock_settings, mock_create_engine):
    mock_settings.POSTGRES_CONNECTION_STRING = "postgresql://user:pass@localhost/testdb"
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value.__enter__.return_value = mock_connection
    
    # Mock read_sql return value
    mock_read_sql.return_value = pd.DataFrame({'id': [1], 'name': ['test']})
    
    connector = PostgresConnector()
    df = connector.execute_query("SELECT * FROM table")
    assert not df.empty
    assert df.iloc[0]['id'] == 1

# CRM Connector Tests
@patch('src.connectors.crm_connector.Salesforce')
def test_salesforce_connector(mock_sf_class):
    mock_sf_instance = MagicMock()
    mock_sf_class.return_value = mock_sf_instance
    
    connector = SalesforceConnector(username='u', password='p', token='t')
    connector.connect()
    
    assert connector.sf is not None
    mock_sf_class.assert_called_once()
