#!/usr/bin/env python3
"""
News Agent - Retrieves and summarizes news about stocks experiencing volatility.

This agent takes stock data from the IBKR Agent, identifies stocks with significant
volatility, and fetches relevant news from multiple sources: Seeking Alpha, Reddit,
and Google RSS. It then summarizes the news and formats it for storage.
"""

import logging
import os
from dotenv import load_dotenv
from services.news_service import NewsService
from utils.mock_data import get_mock_watchlist_data

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("news_agent")

# Check API credentials
logger.info("Checking API credentials...")
# Reddit credentials
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "stock-watchlist-alert-agent")

if REDDIT_CLIENT_ID:
    logger.info("Reddit Client ID is set")
else:
    logger.error("Reddit Client ID is missing")

if REDDIT_CLIENT_SECRET:
    logger.info("Reddit Client Secret is set")
else:
    logger.error("Reddit Client Secret is missing")

if REDDIT_USER_AGENT:
    logger.info(f"Reddit User Agent is: {REDDIT_USER_AGENT}")
else:
    logger.error("Reddit User Agent is missing")

# OpenAI credentials
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    logger.info("OpenAI API key is set")
else:
    logger.warning(
        "OpenAI API key is not set. GPT-4 summarization will not be available."
    )


def filter_duplicate_tickers(watchlist_data):
    """Filter out duplicate tickers from watchlist data.

    Args:
        watchlist_data: Dictionary where keys are watchlist names and values are
                       lists of instruments (stocks)

    Returns:
        Dictionary with the same structure but with duplicate tickers removed
    """
    logger.info("Filtering out duplicate tickers from watchlist data")

    # Keep track of tickers we've seen
    seen_tickers = set()
    # Create a new filtered watchlist data structure
    filtered_data = {}

    for watchlist_name, instruments in watchlist_data.items():
        filtered_instruments = []

        for instrument in instruments:
            ticker = instrument.get("ticker")
            if not ticker:
                continue

            # Only add this instrument if we haven't seen this ticker before
            if ticker not in seen_tickers:
                seen_tickers.add(ticker)
                filtered_instruments.append(instrument)

        # Only add the watchlist if it has instruments after filtering
        if filtered_instruments:
            filtered_data[watchlist_name] = filtered_instruments

    # Log how many duplicates were removed
    total_original = sum(len(instruments) for instruments in watchlist_data.values())
    total_filtered = sum(len(instruments) for instruments in filtered_data.values())
    duplicates_removed = total_original - total_filtered

    logger.info(f"Removed {duplicates_removed} duplicate ticker(s)")
    logger.info(f"Original count: {total_original}, Filtered count: {total_filtered}")

    return filtered_data


def main(use_mock_data=False):
    """Main function to run the News Agent.

    Args:
        use_mock_data: If True, use mock data instead of calling IBKR API

    Returns:
        List of dictionaries containing stock information and news summaries
    """
    try:
        # Get watchlist data
        logger.info("Getting watchlist data")

        if use_mock_data:
            logger.info("Using mock data for testing")
            watchlist_data = get_mock_watchlist_data()
        else:
            # Import IBKR agent and get real data
            try:
                from ibkr_agent import main as ibkr_main

                logger.info("Getting real data from IBKR agent")
                watchlist_data = ibkr_main()
            except Exception as e:
                logger.error(f"Error getting data from IBKR agent: {str(e)}")
                logger.info("Falling back to mock data")
                watchlist_data = get_mock_watchlist_data()

        if not watchlist_data:
            logger.warning("No watchlist data received")
            return []

        # Filter out duplicate tickers
        filtered_watchlist_data = filter_duplicate_tickers(watchlist_data)

        # Create and run news service
        news_service = NewsService()
        news_results = news_service.process_watchlist_results(filtered_watchlist_data)

        # Print the results
        for result in news_results:
            print("\n" + "=" * 80)
            print(f"NEWS FOR {result['ticker']} ({result['price_change_percent']}%)")
            print("=" * 80)
            print(result["news_summary"])

        # Return the results for further processing (e.g. database storage)
        return news_results

    except Exception as e:
        logger.error(f"Error running News Agent: {str(e)}")
        return []


if __name__ == "__main__":
    news_results = main()

    # Send email with the news results
    try:
        from email_agent import main as email_main

        logger.info("Sending news results via email...")
        email_success = email_main(news_results)

        if email_success:
            logger.info("Email sent successfully")
        else:
            logger.warning("Failed to send email")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
