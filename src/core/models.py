from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class Contact(BaseModel):
    """
    Represents a Contact entity based on dbo.CONTACT table.
    """
    CONTACT_ID: str
    FIRST_NAME: str
    LAST_NAME: str
    EMAIL_ADDRESS: Optional[str] = None

class Firm(BaseModel):
    """
    Represents a Firm entity based on dbo.FIRM table.
    """
    FIRM_ID: str
    FIRM_NAME: str
    FIRM_TYPE: str
    CRD_NUMBER: Optional[str] = None
    MASTER_FIRM_ID: Optional[str] = None

class RepProfile(BaseModel):
    """
    Represents a Representative Profile based on dbo.REP_PROFILE table.
    """
    CONTACT_ID: str # Renamed from REP_ID
    FIRM_ID: str
    OFFICE_ID: Optional[str] = None
    CHANNEL: Optional[str] = None
    SUB_CHANNEL: Optional[str] = None
    CRD_NUMBER: Optional[str] = None
    ZIP_CODE: Optional[str] = None # Kept for geospatial logic
    # Territory codes
    TERR1: Optional[str] = None
    TERR2: Optional[str] = None
    TERR3: Optional[str] = None
    TERR4: Optional[str] = None
    TERR5: Optional[str] = None
    TERR6: Optional[str] = None
    TERR7: Optional[str] = None
    TERR8: Optional[str] = None
    TERR9: Optional[str] = None
    TERR10: Optional[str] = None
    TERR11: Optional[str] = None

class TransactionHistory(BaseModel):
    """
    Represents a Sales Transaction based on dbo.TRANSACTION_HISTORY table.
    """
    TRANSACTION_ID: str
    TRANSACTION_DATE: date
    CONTACT_ID: str # Renamed from REP_ID
    FIRM_ID: Optional[str] = None
    PRODUCT_CODE: str
    CUSIP: Optional[str] = None
    GROSS_AMOUNT: float
    TRANSACTION_TYPE: str # Purchase/Redemption
