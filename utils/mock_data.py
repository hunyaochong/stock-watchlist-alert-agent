"""
Mock data utilities for testing the news agent.

This module provides utilities for generating mock data for testing the news agent
when the IBKR API is not available.
"""


def get_mock_watchlist_data():
    """Generate mock watchlist data for testing when IBKR API is not available.

    Returns:
        Dictionary of watchlist results with mock data
    """
    mock_data = {
        "Tech Stocks": [
            {
                "ticker": "AAPL",
                "name": "Apple Inc.",
                "conid": 265598,
                "change_percent": -5.7,
            },
            {
                "ticker": "TSLA",
                "name": "Tesla, Inc.",
                "conid": 76792991,
                "change_percent": 8.4,
            },
        ],
    }
    return mock_data
