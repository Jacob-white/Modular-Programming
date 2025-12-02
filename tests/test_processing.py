import pytest
import pandas as pd
from pydantic import BaseModel, Field
from src.processing.validator import DataValidator

class User(BaseModel):
    id: int
    name: str
    email: str

def test_validate_dataframe_valid():
    df = pd.DataFrame([
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
    ])
    assert DataValidator.validate_dataframe(df, User) is True

def test_validate_dataframe_invalid():
    df = pd.DataFrame([
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 'invalid', 'name': 'Bob', 'email': 'bob@example.com'} # Invalid ID type
    ])
    with pytest.raises(ValueError):
        DataValidator.validate_dataframe(df, User)

def test_check_required_columns():
    df = pd.DataFrame({'A': [1], 'B': [2]})
    assert DataValidator.check_required_columns(df, ['A', 'B']) is True
    
    with pytest.raises(ValueError):
        DataValidator.check_required_columns(df, ['A', 'C'])
