# Stock Watchlist Alert Agent

## Overview

The Stock Watchlist Alert Agent is an automated system that monitors your Interactive Brokers (IBKR) watchlists for significant price movements, collects relevant news from multiple sources, summarizes the information, and sends you email alerts with actionable insights.

### Key Features

- **Watchlist Monitoring**: Connects to IBKR API to track price movements of securities in your watchlists
- **Multi-source News Collection**: Gathers news from Seeking Alpha, Google News, and Reddit
- **AI-powered Summarization**: Generates concise summaries explaining price movements
- **Automated Email Alerts**: Sends formatted email reports with stock news summaries
- **Duplicate Ticker Filtering**: Prevents redundant processing of stocks that appear in multiple watchlists

### System Components

1. **IBKR Agent** (`ibkr_agent.py`): Connects to IBKR API to retrieve watchlist data and price movements
2. **News Agent** (`news_agent.py`): Processes stock data, collects news, and generates summaries
3. **Email Agent** (`email_agent.py`): Formats and sends email alerts with stock news summaries
4. **Client Libraries**: Interfaces with various news sources (Reddit, Google News, Seeking Alpha)
5. **Summarization Service**: Processes news articles to generate concise, relevant summaries

## Setup and Configuration

### Prerequisites

1. IBKR account with enabled API access
2. IBKR Client Portal Web API running locally
3. Python 3.8 or higher
4. API credentials for:
   - Reddit API (for Reddit news)
   - Mailgun API (for sending emails)
   - OpenAI API (optional, for enhanced summarization)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/stock-watchlist-alert-agent.git
   cd stock-watchlist-alert-agent
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example` and configure your API credentials:
   ```
   # IBKR API Configuration
   IBKR_BASE_URL=https://localhost:5000/v1/api
   IBKR_DISABLE_SSL_VERIFY=true

   # Reddit API Configuration
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=stock-watchlist-alert-agent

   # OpenAI API Configuration (optional)
   OPENAI_API_KEY=your_openai_api_key

   # Mailgun API Configuration
   MAILGUN_API_KEY=your_mailgun_api_key
   MAILGUN_DOMAIN=your_mailgun_domain
   FROM_EMAIL=Stock Alert <postmaster@your_mailgun_domain>
   TO_EMAIL=your_email@example.com
   ```

### API Setup Instructions

#### IBKR API Setup

1. Download the Client Portal Web API from [IBKR's website](https://interactivebrokers.github.io/cpwebapi/)
2. Start the API gateway (instructions depend on your OS)
3. Authenticate the session when prompted
4. Keep the gateway running while using this agent

#### Reddit API Setup

1. Create a Reddit account if you don't have one
2. Go to [Reddit's App Preferences](https://www.reddit.com/prefs/apps)
3. Click "Create App" or "Create Another App" at the bottom
4. Fill in the details:
   - Name: Stock Watchlist Alert Agent
   - App type: Script
   - Description: App to fetch stock-related posts from Reddit
   - About URL: (leave blank)
   - Redirect URI: http://localhost:8080
5. Click "Create app"
6. Note your Client ID (the string under the app name) and Client Secret

#### Mailgun API Setup

1. Create a Mailgun account at [Mailgun's website](https://www.mailgun.com/)
2. Verify your domain or use the sandbox domain provided by Mailgun
3. Get your API key from the dashboard
4. Update your `.env` file with the API key and domain

## Usage

### Running the Complete System

To run the entire system (fetch watchlist data, collect news, and send email alerts):

```bash
python news_agent.py
```

This will:
1. Connect to your IBKR account via the Client Portal Web API
2. Fetch all your watchlists and filter out duplicate tickers
3. Collect news from multiple sources for stocks with significant price movements
4. Generate summaries explaining the price movements
5. Send an email alert with the summarized information

### Running Individual Components

#### IBKR Agent Only

To only fetch watchlist data without processing news or sending emails:

```bash
python ibkr_agent.py
```

#### Email Agent Only

To send an email with previously generated news results:

```bash
python email_agent.py
```

### Mock Data for Testing

The system includes mock data for testing without connecting to IBKR:

```bash
python news_agent.py --mock
```

or

```python
from news_agent import main
main(use_mock_data=True)
```

## Troubleshooting

### IBKR Connection Issues

1. **Connection errors**: Make sure the IBKR Client Portal Web API is running and authenticated
2. **Authentication errors**: You may need to re-authenticate your session in the IBKR Client Portal Web API
3. **No watchlists found**: Verify you have created watchlists in your IBKR account

### API Credential Issues

1. **Reddit API errors**: Verify your Reddit API credentials in the `.env` file
2. **Mailgun API errors**: Check your Mailgun API key and domain configuration
3. **OpenAI API errors**: Verify your OpenAI API key if using enhanced summarization

### Performance Considerations

1. The system makes multiple API calls which may take time to complete
2. If you have many watchlists with many instruments, the total processing time will increase
3. The script includes logging to help identify any performance bottlenecks

## For Contributors

### Project Structure

```
stock-watchlist-alert-agent/
├── clients/                  # API client libraries
│   ├── google_news_client.py # Google News API client
│   ├── reddit_client.py      # Reddit API client
│   ├── seeking_alpha_client.py # Seeking Alpha client
│   └── openai_client.py      # OpenAI API client
├── models/                   # Data models
│   └── news_models.py        # News data models
├── services/                 # Business logic services
│   ├── news_service.py       # News processing service
│   └── summarization_service.py # Text summarization service
├── utils/                    # Utility functions
│   └── mock_data.py          # Mock data for testing
├── docs/                     # Documentation
├── ibkr_agent.py             # IBKR API integration
├── news_agent.py             # News processing main script
├── email_agent.py            # Email sending functionality
└── requirements.txt          # Python dependencies
```

### Development Guidelines

1. **Code Style**: Follow PEP 8 guidelines for Python code
2. **Documentation**: Add docstrings to all functions and classes
3. **Error Handling**: Implement proper error handling and logging
4. **Testing**: Add unit tests for new functionality
5. **Environment Variables**: Never hardcode credentials; use environment variables

### Adding New Features

#### Adding a New News Source

1. Create a new client in the `clients/` directory
2. Implement the required methods to fetch news
3. Update the `NewsService` class in `services/news_service.py` to use the new client
4. Update the summarization service if needed

#### Enhancing Summarization

1. Modify the `SummarizationService` class in `services/summarization_service.py`
2. Consider using different NLP techniques or API services
3. Ensure the output format remains consistent

#### Adding New Alert Methods

1. Create a new agent file (e.g., `slack_agent.py`)
2. Implement the functionality to send alerts via the new channel
3. Update the main script to use the new alert method

### Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Submit a pull request with a clear description of the changes

## License

This project is licensed under the MIT License - see the LICENSE file for details.
