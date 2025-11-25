from simple_salesforce import Salesforce
import pandas as pd
from ..core.logger import logger
from ..core.config import settings

class SalesforceConnector:
    """
    Connector for Salesforce using simple-salesforce.
    """
    def __init__(self, username: str = None, password: str = None, token: str = None):
        self.username = username or settings.SF_USERNAME
        self.password = password or settings.SF_PASSWORD
        self.token = token or settings.SF_TOKEN
        self.sf = None

    def connect(self):
        if not all([self.username, self.password, self.token]):
            logger.error("Salesforce credentials incomplete.")
            raise ValueError("Salesforce credentials incomplete.")
        try:
            self.sf = Salesforce(username=self.username, password=self.password, security_token=self.token)
            logger.info("Successfully connected to Salesforce.")
        except Exception as e:
            logger.error(f"Failed to connect to Salesforce: {e}")
            raise

    def query(self, soql: str) -> pd.DataFrame:
        if not self.sf:
            self.connect()
        try:
            logger.debug(f"Executing SOQL: {soql}")
            results = self.sf.query_all(soql)
            records = results.get('records', [])
            if not records:
                return pd.DataFrame()
            
            # Remove attributes field which is metadata
            for record in records:
                if 'attributes' in record:
                    del record['attributes']
            
            return pd.DataFrame(records)
        except Exception as e:
            logger.error(f"Error executing SOQL: {e}")
            raise
