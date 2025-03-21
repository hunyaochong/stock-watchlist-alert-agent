# IBKR Watchlist Alerting Agent

This tool connects to Interactive Brokers (IBKR) API to retrieve your watchlists and track price movements of securities.

## Setup and Configuration

### Prerequisites

1. IBKR account with enabled API access
2. IBKR Client Portal Web API running locally
3. Python 3.8 or higher

### Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

2. Configure your `.env` file:

```
# IBKR API Configuration
IBKR_BASE_URL=https://localhost:5000/v1/api
IBKR_DISABLE_SSL_VERIFY=true
```

## Important: IBKR API Connection

The agent communicates with the IBKR Client Portal Web API, which must be:

1. Running locally on your machine
2. Already authenticated with your IBKR account
3. Available at the URL specified in `IBKR_BASE_URL` (default is `https://localhost:5000/v1/api`)

### Starting the IBKR Client Portal Web API

1. Download the Client Portal Web API from [IBKR's website](https://interactivebrokers.github.io/cpwebapi/)
2. Start the API gateway (instructions depend on your OS)
3. Authenticate the session when prompted
4. Keep the gateway running while using this agent

Once the API gateway is running and authenticated, this agent will be able to access your actual IBKR watchlists.

## Performance Notes

The `get_watchlist_instruments_with_market_data()` function may take some time to complete because:

1. It makes multiple sequential API calls:
   - First to get all your watchlists
   - Then for each watchlist, it fetches detailed information
   - Finally, it retrieves market data for each instrument

2. The IBKR API may have rate limits or slow response times

3. If you have many watchlists with many instruments, the total time will increase

The script now includes detailed timing information to help identify any performance bottlenecks.

## Usage

Run the main script:

```bash
python ibkr_agent.py
```

This will:
1. Connect to your IBKR account via the Client Portal Web API
2. Fetch all your watchlists
3. Get market data for all instruments in these watchlists
4. Display a summary of all instruments with their current change percentages

## Troubleshooting

If you encounter errors:

1. **Connection errors**: Make sure the IBKR Client Portal Web API is running and authenticated
2. **Authentication errors**: You may need to re-authenticate your session in the IBKR Client Portal Web API
3. **No watchlists found**: Verify you have created watchlists in your IBKR account
4. **Long execution times**: This is normal if you have many watchlists or instruments; the script now logs timing information to help identify delays
