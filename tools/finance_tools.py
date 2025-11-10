# tools/finance_tools.py
"""
Finance Tools Module

Purpose:
- Contains helper functions for financial data processing and validation.
- Designed to centralize reusable utilities (e.g., ticker normalization, data formatting).

Current Features:
- normalize_ticker: standardizes stock ticker symbols for consistent data handling.
"""


def normalize_ticker(t: str) -> str:
    """
    Normalize a stock ticker symbol by removing whitespace and converting to uppercase.

    Args:
        t (str): The input ticker symbol (e.g., " aapl ", "msft").

    Returns:
        str: A standardized ticker string (e.g., "AAPL", "MSFT").
    """
    return t.strip().upper()