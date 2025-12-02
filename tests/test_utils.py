import pytest
from datetime import date
from src.utils.date_utils import get_fiscal_year, get_fiscal_quarter, add_business_days
from src.utils.currency import convert_currency, format_currency
from src.utils.cache import simple_cache
from src.processing.cleaner import clean_zip_code, validate_email, standardize_advisor_name

# Date Utils Tests
def test_get_fiscal_year():
    assert get_fiscal_year(date(2023, 1, 15)) == 2023
    assert get_fiscal_year(date(2023, 12, 31)) == 2023

def test_get_fiscal_quarter():
    assert get_fiscal_quarter(date(2023, 1, 15)) == 1
    assert get_fiscal_quarter(date(2023, 4, 1)) == 2
    assert get_fiscal_quarter(date(2023, 10, 1)) == 4

def test_add_business_days():
    # Friday to Monday
    d = date(2023, 11, 24) # Friday
    assert add_business_days(d, 1) == date(2023, 11, 27) # Monday
    # Monday to Tuesday
    d = date(2023, 11, 27)
    assert add_business_days(d, 1) == date(2023, 11, 28)

# Currency Tests
def test_convert_currency():
    # Mock rate is 0.92 for USD to EUR
    assert convert_currency(100, 'USD', 'EUR') == 92.0
    # Mock rate is 0.79 for USD to GBP
    assert convert_currency(100, 'USD', 'GBP') == 79.0
    # Same currency
    assert convert_currency(100, 'USD', 'USD') == 100.0

def test_format_currency():
    assert format_currency(1234.56, 'USD') == '$1,234.56'
    assert format_currency(1234.56, 'EUR') == '€1,234.56'

# Cache Tests
def test_memory_cache():
    call_count = 0
    
    @simple_cache(ttl_seconds=1)
    def expensive_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    assert expensive_func(2) == 4
    assert expensive_func(2) == 4
    assert call_count == 1 # Should be cached

# Cleaner Tests
def test_clean_zip_code():
    assert clean_zip_code(12345) == '12345'
    assert clean_zip_code('12345-6789') == '12345'
    assert clean_zip_code('123') == '00123'
    assert clean_zip_code(None) is None

def test_validate_email():
    assert validate_email('test@example.com') is True
    assert validate_email('invalid-email') is False
    assert validate_email(None) is False

def test_standardize_name():
    assert standardize_advisor_name("  john   doe  ") == "John Doe"
    assert standardize_advisor_name("jane smith") == "Jane Smith"
    assert standardize_advisor_name(None) is None
