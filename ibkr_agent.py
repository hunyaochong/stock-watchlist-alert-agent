#!/usr/bin/env python3
"""
IBKR Agent - Retrieves watchlists and market data from Interactive Brokers API.

This agent fetches all instruments from IBKR watchlists and gets their percentage changes
using the live market data API.
"""

import logging
import os
import requests
import time
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ibkr_agent")

# Base URL for IBKR API
IBKR_BASE_URL = os.environ.get("IBKR_BASE_URL", "https://localhost:5001/v1/api")


# --------------------------------------------------------------
# Step 1: Define the data models for each stage
# --------------------------------------------------------------


# Pydantic models for data validation
class Watchlist(BaseModel):
    """Model representing a watchlist summary."""

    id: str = Field(..., description="Watchlist ID")
    name: str = Field(..., description="Display name of the watchlist")


class Instrument(BaseModel):
    """Model representing an instrument in a watchlist."""

    conid: int = Field(..., description="IB contract ID of the instrument")
    name: Optional[str] = Field(None, description="Display name of the instrument")
    ticker: Optional[str] = Field(None, description="Symbol of the instrument")
    asset_class: Optional[str] = Field(
        None, alias="assetClass", description="Security type identifier"
    )

    @validator("conid")
    def conid_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("conid must be positive")
        return v


class WatchlistDetails(BaseModel):
    """Model representing details of a watchlist."""

    id: str = Field(..., description="Identifier of the watchlist")
    name: str = Field(..., description="Display name of the watchlist")
    read_only: bool = Field(
        ..., alias="readOnly", description="Indicates if watchlist can be edited"
    )
    instruments: List[Instrument] = Field(
        [], description="Instruments in the watchlist"
    )
    hash: Optional[str] = Field(None, description="Hash value of the watchlist")
    instruments: List[Instrument] = Field(
        [], description="Instruments in the watchlist"
    )

    class Config:
        allow_population_by_field_name = True


class WatchlistsResponse(BaseModel):
    """Model representing the response from the watchlists API."""

    data: Dict[str, Any] = Field(..., description="Response data container")

    @property
    def user_lists(self) -> List[Watchlist]:
        """Get the list of watchlists from the data."""
        return [Watchlist(**wl) for wl in self.data.get("user_lists", [])]


class MarketDataSnapshot(BaseModel):
    """Model representing market data for an instrument."""

    conid: int = Field(..., description="Contract ID")
    last_price: Optional[float] = Field(None, description="Last price")
    change: Optional[float] = Field(None, description="Change from previous close")
    change_percent: Optional[float] = Field(None, description="Change percentage")

    @validator("change_percent")
    def validate_change_percent(cls, v):
        if v is not None and (v < -100 or v > 100):
            logger.warning(f"Unusual change percentage detected: {v}%")
        return v


# --------------------------------------------------------------
# Step 2: Define the functions
# --------------------------------------------------------------


class IBKRAgent:
    """Agent for interacting with IBKR API to retrieve watchlists and market data."""

    def __init__(self, base_url: str = IBKR_BASE_URL):
        """Initialize the IBKR Agent.

        Args:
            base_url: Base URL for the IBKR API
        """
        self.base_url = base_url
        self.session = requests.Session()

        # Disable SSL verification based on environment variable
        disable_ssl_verify = (
            os.environ.get("IBKR_DISABLE_SSL_VERIFY", "false").lower() == "true"
        )
        self.session.verify = not disable_ssl_verify

        if disable_ssl_verify:
            # Suppress only the single warning from urllib3 needed.
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logger.warning(
                "SSL verification is disabled. This should only be used in development."
            )

        logger.info(f"Initialized IBKR Agent with base URL: {base_url}")

    def _make_request(
        self, method: str, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Dict:
        """Make a request to the IBKR API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(
                method=method, url=url, params=params, json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {url}: {str(e)}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            raise

    def verify_api_connection(self):
        """Verify connection to the IBKR API is working and authenticated.

        Returns:
            bool: True if connection is working, raises exception otherwise
        """
        logger.info("Verifying API connection to IBKR")
        try:
            # Try to get server time which is a simple endpoint that requires authentication
            self._make_request("GET", "/iserver/auth/status")
            logger.info("API connection verified")
            return True
        except Exception as e:
            logger.error(f"API connection failed: {str(e)}")
            raise ConnectionError(
                f"Failed to connect to IBKR API at {self.base_url}. "
                f"Make sure the IBKR Client Portal Web API is running and authenticated. "
                f"Error: {str(e)}"
            )

    def get_all_watchlists(self) -> List[Watchlist]:
        """Get all watchlists from IBKR.

        Returns:
            List of watchlists
        """
        logger.info("Fetching all watchlists")
        start_time = time.time()

        # Verify API connection before proceeding
        self.verify_api_connection()

        params = {"SC": "USER_WATCHLIST"}
        response_data = self._make_request("GET", "/iserver/watchlists", params=params)

        # Log the raw response for debugging
        logger.debug(f"Watchlists API response: {response_data}")

        try:
            watchlists_response = WatchlistsResponse(**response_data)
            elapsed_time = time.time() - start_time
            logger.info(
                f"Successfully retrieved {len(watchlists_response.user_lists)} watchlists in {elapsed_time:.2f} seconds"
            )
            return watchlists_response.user_lists
        except Exception as e:
            logger.error(f"Error parsing watchlists response: {str(e)}")
            logger.error(f"Raw response: {response_data}")
            raise

    def get_watchlist_details(self, watchlist_id: str) -> WatchlistDetails:
        """Get details of a specific watchlist.

        Args:
            watchlist_id: ID of the watchlist

        Returns:
            Watchlist details including instruments
        """
        logger.info(f"Fetching details for watchlist ID: {watchlist_id}")
        start_time = time.time()

        params = {"id": watchlist_id}
        response_data = self._make_request("GET", "/iserver/watchlist", params=params)

        # Log the raw response for debugging
        logger.debug(f"Watchlist details API response: {response_data}")

        try:
            watchlist_details = WatchlistDetails(**response_data)
            elapsed_time = time.time() - start_time
            logger.info(
                f"Successfully retrieved watchlist '{watchlist_details.name}' with "
                f"{len(watchlist_details.instruments)} instruments in {elapsed_time:.2f} seconds"
            )
            return watchlist_details
        except Exception as e:
            logger.error(f"Error parsing watchlist details response: {str(e)}")
            logger.error(f"Raw response: {response_data}")
            raise

    def get_market_data(
        self, conids: List[int], fields: List[str] = None
    ) -> Dict[int, MarketDataSnapshot]:
        """Get market data for specified contract IDs.

        Args:
            conids: List of contract IDs
            fields: List of fields to retrieve (defaults to last price, change, and change percent)

        Returns:
            Dictionary mapping contract IDs to market data
        """
        if not conids:
            logger.warning("No contract IDs provided for market data request")
            return {}

        # Default fields if none provided
        if fields is None:
            fields = ["31", "82", "83"]  # Last price, change, change percent

        logger.info(f"Fetching market data for {len(conids)} instruments")

        params = {
            "conids": ",".join(str(conid) for conid in conids),
            "fields": ",".join(fields),
        }

        response_data = self._make_request(
            "GET", "/iserver/marketdata/snapshot", params=params
        )

        # Log the raw response for debugging
        if len(conids) < 10:  # Only log if small number of conids to avoid huge logs
            logger.debug(f"Market data API response: {response_data}")

        market_data = {}
        for item in response_data:
            try:
                conid = int(item.get("conid", 0))
                if conid <= 0:
                    logger.warning(f"Invalid conid in market data response: {item}")
                    continue

                # Extract relevant fields
                last_price = None
                change = None
                change_percent = None

                # Field 31 is last price
                if "31" in item:
                    try:
                        last_price = float(item["31"])
                    except (ValueError, TypeError):
                        logger.warning(
                            f"Invalid last price value for conid {conid}: {item.get('31')}"
                        )

                # Field 82 is change
                if "82" in item:
                    try:
                        change = float(item["82"])
                    except (ValueError, TypeError):
                        logger.warning(
                            f"Invalid change value for conid {conid}: {item.get('82')}"
                        )

                # Field 83 is change percent
                if "83" in item:
                    try:
                        change_percent = float(item["83"])
                    except (ValueError, TypeError):
                        logger.warning(
                            f"Invalid change percent value for conid {conid}: {item.get('83')}"
                        )

                market_data[conid] = MarketDataSnapshot(
                    conid=conid,
                    last_price=last_price,
                    change=change,
                    change_percent=change_percent,
                )
            except Exception as e:
                logger.error(
                    f"Error processing market data for item: {item}, error: {str(e)}"
                )

        logger.info(
            f"Successfully retrieved market data for {len(market_data)} instruments"
        )
        return market_data

    def get_watchlist_instruments_with_market_data(
        self,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Fetch all watchlists and their instruments with market data."""
        logger.info("Starting to fetch watchlist instruments with market data")

        result = {}
        watchlists = self.get_all_watchlists()

        for watchlist in watchlists:
            try:
                logger.info(
                    f"Processing watchlist: {watchlist.name} (ID: {watchlist.id})"
                )

                # Get watchlist details with instruments
                watchlist_details = self.get_watchlist_details(watchlist.id)

                if not watchlist_details.instruments:
                    continue

                # Get market data for instruments
                instruments_with_data = []
                market_data = self.get_market_data(
                    [i.conid for i in watchlist_details.instruments]
                )

                for instrument in watchlist_details.instruments:
                    instrument_data = instrument.model_dump()

                    # Add market data if available
                    md = market_data.get(instrument.conid)
                    if md:
                        instrument_data["change_percent"] = md.change_percent
                        # Only include instruments with significant percent changes (>3% or <-3%)
                        if (
                            instrument_data["change_percent"] is not None
                            and abs(instrument_data["change_percent"]) >= 3.0
                        ):
                            instruments_with_data.append(instrument_data)

                if (
                    instruments_with_data
                ):  # Only add watchlist if it has instruments with valid data
                    result[watchlist.name] = instruments_with_data
                    logger.info(
                        f"Added {len(instruments_with_data)} instruments for watchlist '{watchlist.name}'"
                    )

            except Exception as e:
                logger.error(
                    f"Error processing watchlist {watchlist.name} (ID: {watchlist.id}): {str(e)}"
                )
                continue

        return result


def print_watchlist_summary(watchlist_data: Dict[str, List[Dict[str, Any]]]) -> None:
    """Print a summary of watchlists and their instruments with percentage changes.

    Args:
        watchlist_data: Dictionary mapping watchlist names to lists of instruments with market data
    """
    print("\nWatchlist Summary:")
    print("=" * 50)

    # Sort watchlists by name
    for watchlist_name, instruments in sorted(watchlist_data.items()):
        if not instruments:  # Skip empty watchlists
            continue

        print(f"\nWatchlist: {watchlist_name}")
        print("-" * 50)

        # Sort instruments by percentage change (descending)
        sorted_instruments = sorted(
            instruments,
            key=lambda x: float(x.get("change_percent", 0) or 0),
            reverse=True,
        )

        for instrument in sorted_instruments:
            ticker = instrument.get("ticker", "Unknown")
            name = instrument.get("name", "Unknown")
            change_percent = instrument.get("change_percent")

            # Only print instruments with valid data
            if change_percent is not None:
                change_str = f"{change_percent:.2f}%"
                print(f"{ticker} ({name}): {change_str}")


# --------------------------------------------------------------
# Step 3: Chain the functions together in main function
# --------------------------------------------------------------


def main():
    """Main function to run the IBKR Agent."""
    try:
        agent = IBKRAgent()
        watchlist_data = agent.get_watchlist_instruments_with_market_data()
        print_watchlist_summary(watchlist_data)
        logger.info("IBKR Agent completed successfully")
        return watchlist_data  # Return the data for further processing
    except Exception as e:
        logger.error(f"Error running IBKR Agent: {str(e)}")
        return {}  # Return empty dict on error


if __name__ == "__main__":
    main()
