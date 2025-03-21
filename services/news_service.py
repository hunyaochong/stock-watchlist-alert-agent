"""
News service for retrieving and processing news about stocks.

This module provides a service for retrieving and processing news about stocks
from multiple sources, including Seeking Alpha, Google News, and Reddit.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from models.news_models import StockNews
from clients.seeking_alpha_client import SeekingAlphaClient
from clients.google_news_client import GoogleNewsClient
from clients.reddit_client import RedditClient
from services.summarization_service import SummarizationService

logger = logging.getLogger("news_agent")


class NewsService:
    """Service for retrieving and processing news about stocks."""

    def __init__(
        self,
        seeking_alpha_client: Optional[SeekingAlphaClient] = None,
        google_news_client: Optional[GoogleNewsClient] = None,
        reddit_client: Optional[RedditClient] = None,
        summarization_service: Optional[SummarizationService] = None,
    ):
        """Initialize the news service.

        Args:
            seeking_alpha_client: Seeking Alpha client for retrieving news from Seeking Alpha
            google_news_client: Google News client for retrieving news from Google
            reddit_client: Reddit client for retrieving news from relevant subreddits
            summarization_service: Summarization service for generating summaries
        """
        self.seeking_alpha_client = seeking_alpha_client or SeekingAlphaClient()
        self.google_news_client = google_news_client or GoogleNewsClient()
        self.reddit_client = reddit_client or RedditClient()
        self.summarization_service = summarization_service or SummarizationService()

    def process_stock(
        self,
        ticker: str,
        company_name: Optional[str] = None,
        price_change_percent: Optional[float] = None,
    ) -> StockNews:
        """Process a stock to collect and summarize news from all sources.

        Args:
            ticker: Stock ticker symbol
            company_name: Company name (optional)
            price_change_percent: Price change percentage (optional)

        Returns:
            StockNews object with all collected news and summaries
        """
        logger.info(
            f"Processing news for {ticker} ({company_name if company_name else 'Unknown'})"
        )

        # Initialize stock news object
        stock_news = StockNews(
            ticker=ticker,
            company_name=company_name,
            price_change_percent=price_change_percent,
        )

        # Get search query (use ticker and company name if available)
        search_query = ticker
        if company_name:
            search_query = f"{ticker} {company_name}"

        # Get news from each source
        seeking_alpha_articles = self.seeking_alpha_client.get_news(ticker)
        google_articles = self.google_news_client.get_news(search_query)
        # Using search_query for Reddit to get more relevant results
        reddit_articles = self.reddit_client.get_posts(ticker, search_query)

        # Add all articles to the stock news
        stock_news.articles.extend(seeking_alpha_articles)
        stock_news.articles.extend(google_articles)
        stock_news.articles.extend(reddit_articles)

        # Create summaries
        stock_news.summary_seeking_alpha = (
            self.summarization_service.summarize_seeking_alpha(
                seeking_alpha_articles, ticker, price_change_percent
            )
        )
        stock_news.summary_google = self.summarization_service.summarize_google_news(
            google_articles, ticker, price_change_percent
        )
        stock_news.summary_reddit = (
            self.summarization_service.summarize_reddit_by_subreddit(
                reddit_articles, ticker, price_change_percent
            )
        )

        logger.info(f"Completed news processing for {ticker}")
        return stock_news

    def format_final_summary(self, stock_news: StockNews) -> str:
        """Format the final summary text.

        Args:
            stock_news: StockNews object with all summaries

        Returns:
            Formatted summary text with only the 3 bullet points
        """
        summary = []

        # Add header with stock info
        if stock_news.company_name:
            header = f"News Summary for {stock_news.ticker} ({stock_news.company_name})"
        else:
            header = f"News Summary for {stock_news.ticker}"

        if stock_news.price_change_percent is not None:
            header += f" | Price Change: {stock_news.price_change_percent:.2f}%"

        summary.append(header)
        summary.append("=" * len(header))
        summary.append("")

        # Generate concise bullet points if price change is available
        if stock_news.price_change_percent is not None:
            # Get the summarization service
            summarization_service = SummarizationService()

            # Generate concise bullet points
            bullet_points = summarization_service.generate_concise_bullet_points(
                stock_news.ticker,
                stock_news.price_change_percent,
                stock_news.summary_seeking_alpha,
                stock_news.summary_google,
                stock_news.summary_reddit,
            )

            # Add bullet points to summary
            summary.append("KEY FACTORS DRIVING PRICE CHANGE:")
            summary.append(bullet_points)
        else:
            summary.append("No price change information available.")

        return "\n".join(summary)

    def process_watchlist_results(
        self, results: Dict[str, List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """Process watchlist results from IBKR agent to collect news for volatile stocks.

        Args:
            results: Dictionary of watchlist results from IBKR agent

        Returns:
            List of dictionaries containing stock information and news summaries
        """
        logger.info("Processing watchlist results from IBKR agent")

        news_results = []

        for watchlist_name, instruments in results.items():
            logger.info(f"Processing watchlist: {watchlist_name}")

            for instrument in instruments:
                ticker = instrument.get("ticker")
                name = instrument.get("name")
                change_percent = instrument.get("change_percent")

                if not ticker:
                    logger.warning(f"Skipping instrument without ticker: {instrument}")
                    continue

                # Process the stock
                stock_news = self.process_stock(ticker, name, change_percent)

                # Format the summary
                summary_text = self.format_final_summary(stock_news)

                # Create result dictionary suitable for database storage
                result = {
                    "ticker": ticker,
                    "company_name": name,
                    "price_change_percent": change_percent,
                    "news_summary": summary_text,
                    "summary_seeking_alpha": stock_news.summary_seeking_alpha,
                    "summary_google": stock_news.summary_google,
                    "summary_reddit": stock_news.summary_reddit,
                    "timestamp": datetime.now().isoformat(),
                    "watchlist": watchlist_name,
                }

                news_results.append(result)

                logger.info(f"Completed news summary for {ticker}")

        logger.info(
            f"Completed processing {len(news_results)} stocks from watchlist results"
        )
        return news_results
