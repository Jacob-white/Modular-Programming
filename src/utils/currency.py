from typing import Dict

# Mock exchange rates
EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
    'CAD': 1.35,
    'JPY': 150.0
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Converts amount from one currency to another using mock rates.
    """
    if from_currency == to_currency:
        return amount
    
    if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        raise ValueError(f"Currency pair {from_currency}-{to_currency} not supported.")
    
    # Convert to USD first
    amount_usd = amount / EXCHANGE_RATES[from_currency]
    
    # Convert to target
    return amount_usd * EXCHANGE_RATES[to_currency]

def format_currency(amount: float, currency: str = 'USD') -> str:
    """
    Formats a number as a currency string.
    """
    if currency == 'USD':
        return f"${amount:,.2f}"
    elif currency == 'EUR':
        return f"€{amount:,.2f}"
    elif currency == 'GBP':
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"
