"""
Seeking Alpha API client for retrieving stock-related news and analysis.

This module provides a client for interacting with the Seeking Alpha API to retrieve
news articles and analysis related to specific stocks.
"""

import logging
import os
import json
import http.client
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from models.news_models import NewsArticle
from clients.openai_client import OpenAIClient

logger = logging.getLogger("news_agent")

# Seeking Alpha API config
SEEKING_ALPHA_KEY = os.environ.get("SEEKING_ALPHA_API_KEY")
SEEKING_ALPHA_HOST = os.environ.get(
    "SEEKING_ALPHA_HOST", "seeking-alpha.p.rapidapi.com"
)


class SeekingAlphaClient:
    """Client for interacting with the Seeking Alpha API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        host: Optional[str] = None,
        openai_client: Optional[OpenAIClient] = None,
    ):
        """Initialize the Seeking Alpha client.

        Args:
            api_key: Seeking Alpha API key (defaults to environment variable)
            host: Seeking Alpha API host (defaults to environment variable)
            openai_client: OpenAI client for summarization
        """
        self.api_key = api_key or SEEKING_ALPHA_KEY
        self.host = host or SEEKING_ALPHA_HOST
        self.openai_client = openai_client or OpenAIClient()

        if not self.api_key:
            logger.warning(
                "Seeking Alpha API key not set. Seeking Alpha search will be skipped."
            )

    def get_news(self, ticker: str, days: int = 2) -> List[NewsArticle]:
        """Get news articles from Seeking Alpha API.

        Args:
            ticker: Stock ticker symbol
            days: How many days back to search for news

        Returns:
            List of NewsArticle objects containing news articles
        """
        if not self.api_key:
            logger.warning(
                "Seeking Alpha API key not set. Skipping Seeking Alpha search."
            )
            return []

        logger.info(f"Searching Seeking Alpha for news about {ticker}")
        articles = []

        try:
            conn = http.client.HTTPSConnection(self.host)

            headers = {
                "x-rapidapi-key": self.api_key,
                "x-rapidapi-host": self.host,
            }

            # Get analysis articles
            analysis_articles = self._get_analysis_articles(conn, headers, ticker)

            # Get news articles
            news_articles = self._get_news_articles(conn, headers, ticker)

            # Combine articles
            all_articles = analysis_articles + news_articles

            # Filter by date if needed
            if days > 0:
                cutoff_date = datetime.now() - timedelta(days=days)
                all_articles = [
                    article
                    for article in all_articles
                    if article.published_at and article.published_at >= cutoff_date
                ]

            # Create a single article with summarized content
            if all_articles:
                # Extract titles for summarization
                titles = [article.title for article in all_articles]

                # Generate a summary of the titles
                summary = self._summarize_titles(ticker, titles)

                # Create a single article with the summary
                summary_article = NewsArticle(
                    source="SeekingAlpha",
                    title=f"Seeking Alpha articles about {ticker}",
                    url=f"https://seekingalpha.com/symbol/{ticker}",
                    content=summary,
                    published_at=datetime.now(),
                )

                articles.append(summary_article)

            logger.info(
                f"Found {len(all_articles)} Seeking Alpha articles for {ticker}, summarized into 1 article"
            )
            return articles

        except Exception as e:
            logger.error(f"Error fetching Seeking Alpha news for {ticker}: {str(e)}")
            return []

    def _get_analysis_articles(self, conn, headers, ticker: str) -> List[NewsArticle]:
        """Get analysis articles from Seeking Alpha API.

        Args:
            conn: HTTP connection
            headers: HTTP headers
            ticker: Stock ticker symbol

        Returns:
            List of NewsArticle objects containing analysis articles
        """
        articles = []
        analysis_endpoint = f"/analysis/v2/list?id={ticker.lower()}&size=20&number=1"
        logger.info(f"Requesting Seeking Alpha analysis: {analysis_endpoint}")

        try:
            conn.request("GET", analysis_endpoint, headers=headers)
            res = conn.getresponse()
            analysis_data = json.loads(res.read().decode("utf-8"))

            # Process analysis articles
            if "data" in analysis_data and analysis_data["data"]:
                for article in analysis_data["data"]:
                    # Extract basic article info without getting details
                    article_attributes = article.get("attributes", {})
                    title = article_attributes.get("title", "Unknown Title")

                    # Get publish time
                    publish_time_str = article_attributes.get("publishOn")
                    published_date = None
                    if publish_time_str:
                        try:
                            # Parse the date and make it timezone-naive to avoid comparison issues
                            dt = datetime.fromisoformat(
                                publish_time_str.replace("-05:00", "-0500")
                            )
                            # Convert to naive datetime by replacing with local time
                            published_date = datetime(
                                dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
                            )
                        except (ValueError, TypeError):
                            # If we can't parse the date, just use current time
                            published_date = datetime.now()

                    # Get URL
                    url = None
                    if "links" in article and "self" in article["links"]:
                        url = f"https://seekingalpha.com{article['links']['self']}"

                    # Create article object
                    articles.append(
                        NewsArticle(
                            source="SeekingAlpha",
                            title=title,
                            url=url,
                            content=title,  # Just use title as content
                            published_at=published_date,
                        )
                    )
        except Exception as e:
            logger.error(
                f"Error fetching Seeking Alpha analysis for {ticker}: {str(e)}"
            )

        return articles

    def _get_news_articles(self, conn, headers, ticker: str) -> List[NewsArticle]:
        """Get news articles from Seeking Alpha API.

        Args:
            conn: HTTP connection
            headers: HTTP headers
            ticker: Stock ticker symbol

        Returns:
            List of NewsArticle objects containing news articles
        """
        articles = []
        news_endpoint = f"/news/v2/list?id={ticker.lower()}&size=20"
        logger.info(f"Requesting Seeking Alpha news: {news_endpoint}")

        try:
            conn.request("GET", news_endpoint, headers=headers)
            news_res = conn.getresponse()
            news_data = json.loads(news_res.read().decode("utf-8"))

            # Process news articles
            if "data" in news_data and news_data["data"]:
                for news_item in news_data["data"]:
                    # Extract basic article info without getting details
                    news_attributes = news_item.get("attributes", {})
                    title = news_attributes.get("title", "Unknown Title")

                    # Get publish time
                    publish_time_str = news_attributes.get("publishOn")
                    published_date = None
                    if publish_time_str:
                        try:
                            # Parse the date and make it timezone-naive to avoid comparison issues
                            dt = datetime.fromisoformat(
                                publish_time_str.replace("-05:00", "-0500")
                            )
                            # Convert to naive datetime by replacing with local time
                            published_date = datetime(
                                dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
                            )
                        except (ValueError, TypeError):
                            # If we can't parse the date, just use current time
                            published_date = datetime.now()

                    # Get URL
                    url = None
                    if "links" in news_item and "self" in news_item["links"]:
                        url = f"https://seekingalpha.com{news_item['links']['self']}"

                    # Create article object
                    articles.append(
                        NewsArticle(
                            source="SeekingAlpha",
                            title=title,
                            url=url,
                            content=title,  # Just use title as content
                            published_at=published_date,
                        )
                    )
            else:
                logger.info(f"No news articles found for {ticker}")
        except Exception as e:
            logger.error(f"Error fetching Seeking Alpha news for {ticker}: {str(e)}")

        return articles

    def _summarize_titles(self, ticker: str, titles: List[str]) -> str:
        """Summarize article titles using OpenAI.

        Args:
            ticker: Stock ticker symbol
            titles: List of article titles

        Returns:
            Summarized text
        """
        if not titles:
            return "No Seeking Alpha articles found."

        if not self.openai_client or not self.openai_client.api_key:
            # If OpenAI is not available, just return the titles
            return "Recent Seeking Alpha headlines:\n- " + "\n- ".join(titles[:5])

        try:
            # Create prompt for OpenAI
            prompt = f"""
            Here are recent Seeking Alpha article titles about {ticker} stock:
            
            {chr(10).join(["- " + title for title in titles])}
            
            Based on these headlines, provide a single concise sentence that summarizes 
            the overall sentiment and key themes in Seeking Alpha's coverage of {ticker}.
            """

            # Call OpenAI API
            response = self.openai_client.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial analyst specializing in stock market analysis. Provide concise, insightful summaries of financial news headlines.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=100,
            )

            # Extract and return the summary
            summary = response.choices[0].message.content.strip()

            # Add the titles as reference
            full_content = f"{summary}\n\nRecent headlines:\n" + "\n".join(
                [f"- {title}" for title in titles[:10]]
            )

            return full_content

        except Exception as e:
            logger.error(f"Error generating summary for {ticker} titles: {str(e)}")
            return "Recent Seeking Alpha headlines:\n- " + "\n- ".join(titles[:5])
