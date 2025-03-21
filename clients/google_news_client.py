"""
Google News RSS client for retrieving stock-related news.

This module provides a client for retrieving news articles from Google News RSS
feeds related to specific stocks.
"""

import logging
import re
import xml.etree.ElementTree as ET
from typing import List, Optional
from datetime import datetime, timedelta
import requests
from models.news_models import NewsArticle

logger = logging.getLogger("news_agent")


class GoogleNewsClient:
    """Client for retrieving news from Google News RSS feeds."""

    def __init__(self):
        """Initialize the Google News client."""
        pass

    def get_news(self, query: str, days: int = 2) -> List[NewsArticle]:
        """Get news articles from Google News RSS feed.

        Args:
            query: Search query (typically stock ticker or company name)
            days: How many days back to search for news

        Returns:
            List of NewsArticle objects containing news articles
        """
        logger.info(f"Searching Google News RSS for {query}")
        articles = []

        try:
            # Encode the query for URL
            encoded_query = query.replace(" ", "+")
            url = f"https://news.google.com/rss/search?q={encoded_query}+stock&hl=en-US&gl=US&ceid=US:en"

            response = requests.get(url)
            response.raise_for_status()

            # Parse the XML response
            root = ET.fromstring(response.content)

            # Find all item elements (news articles)
            items = root.findall(".//item")

            cutoff_date = datetime.now() - timedelta(days=days)

            for item in items:
                article = self._process_item(item, cutoff_date)
                if article:
                    articles.append(article)

            logger.info(f"Found {len(articles)} Google News RSS articles for {query}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching Google RSS news for {query}: {str(e)}")
            return []

    def _process_item(
        self, item: ET.Element, cutoff_date: datetime
    ) -> Optional[NewsArticle]:
        """Process an RSS item and create a NewsArticle.

        Args:
            item: XML Element representing an RSS item
            cutoff_date: Cutoff date for articles

        Returns:
            NewsArticle object if the item is valid and recent, None otherwise
        """
        title_elem = item.find("title")
        link_elem = item.find("link")
        pubDate_elem = item.find("pubDate")
        description_elem = item.find("description")
        source_elem = item.find("source")

        if title_elem is not None and link_elem is not None:
            title = title_elem.text
            link = link_elem.text

            # Parse the publication date
            published_at = None
            if pubDate_elem is not None and pubDate_elem.text:
                published_at = self._parse_date(pubDate_elem.text)

            # Skip if article is older than the cutoff date
            if published_at and published_at < cutoff_date:
                return None

            # Extract description and source
            description = ""
            if description_elem is not None and description_elem.text:
                # The description often contains HTML, we'll extract just the text
                description = re.sub("<[^<]+?>", "", description_elem.text)

            source = ""
            if source_elem is not None:
                source = source_elem.text

            return NewsArticle(
                source=f"Google News - {source}" if source else "Google News",
                title=title,
                url=link,
                content=description,
                published_at=published_at,
            )

        return None

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse a date string from an RSS feed.

        Args:
            date_str: Date string to parse

        Returns:
            Parsed datetime object, or None if parsing fails
        """
        try:
            return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            # Try alternative format
            try:
                return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                logger.warning(f"Could not parse date: {date_str}")
                return None
