from abc import ABC, abstractmethod
import pandas as pd
from sqlalchemy import create_engine, text
from ..core.logger import logger
from ..core.config import settings

class DatabaseConnector(ABC):
    """
    Abstract base class for database connectors.
    """
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        pass

class SQLServerConnector(DatabaseConnector):
    """
    Connector for SQL Server using SQLAlchemy and pyodbc.
    """
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or settings.SQL_SERVER_CONNECTION_STRING
        
        if not self.connection_string and settings.SQL_SERVER_HOST and settings.SQL_SERVER_DB:
            driver = "ODBC+Driver+17+for+SQL+Server"
            if settings.SQL_SERVER_TRUSTED_CONNECTION:
                self.connection_string = (
                    f"mssql+pyodbc://@{settings.SQL_SERVER_HOST}/{settings.SQL_SERVER_DB}"
                    f"?driver={driver}&trusted_connection=yes"
                )
                logger.info("Constructed SQL Server connection string using Trusted Connection.")
            else:
                # Fallback to standard user/pass if provided in env, though usually they are in the full conn str
                # But if we want to support building it:
                # We would need SQL_SERVER_USER and SQL_SERVER_PASS in config too if we go down this route fully.
                # For now, let's just support the Trusted Connection case as requested.
                pass

        self.engine = None

    def connect(self):
        if not self.connection_string:
            logger.error("SQL Server connection string not provided.")
            raise ValueError("SQL Server connection string not provided.")
        try:
            self.engine = create_engine(self.connection_string)
            logger.info("Successfully connected to SQL Server.")
        except Exception as e:
            logger.error(f"Failed to connect to SQL Server: {e}")
            raise

    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        if not self.engine:
            self.connect()
        try:
            logger.debug(f"Executing query: {query}")
            with self.engine.connect() as connection:
                return pd.read_sql(text(query), connection, params=params)
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise

class PostgresConnector(DatabaseConnector):
    """
    Connector for PostgreSQL using SQLAlchemy and psycopg2.
    """
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or settings.POSTGRES_CONNECTION_STRING
        self.engine = None

    def connect(self):
        if not self.connection_string:
            logger.error("PostgreSQL connection string not provided.")
            raise ValueError("PostgreSQL connection string not provided.")
        try:
            self.engine = create_engine(self.connection_string)
            logger.info("Successfully connected to PostgreSQL.")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        if not self.engine:
            self.connect()
        try:
            logger.debug(f"Executing query: {query}")
            with self.engine.connect() as connection:
                return pd.read_sql(text(query), connection, params=params)
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
