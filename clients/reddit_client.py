"""
Reddit API client for retrieving stock-related discussions.

This module provides a client for interacting with the Reddit API to retrieve
posts and comments related to specific stocks.
"""

import logging
import os
from typing import List, Optional, Set
from datetime import datetime, timedelta
import praw
from models.news_models import NewsArticle

logger = logging.getLogger("news_agent")

# Reddit API config
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.environ.get("REDDIT_USER_AGENT", "stock-watchlist-alert-agent")

# Subreddits to search
DEFAULT_SUBREDDITS = [
    "wallstreetbets",
    "stocks",
    "investing",
    "StockMarket",
    "ValueInvesting",
    "SecurityAnalysis",
    "TSMC",
    "NVDA",
    "TSLA",
    "Apple",
]

# Common stock tickers to check for to avoid cross-contamination
COMMON_TICKERS = [
    "AAPL",
    "TSLA",
    "MSFT",
    "AMZN",
    "GOOGL",
    "META",
    "NVDA",
    "JPM",
    "GS",
    "BAC",
]


class RedditClient:
    """Client for interacting with the Reddit API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        user_agent: Optional[str] = None,
        subreddits: Optional[List[str]] = None,
    ):
        """Initialize the Reddit client.

        Args:
            client_id: Reddit API client ID (defaults to environment variable)
            client_secret: Reddit API client secret (defaults to environment variable)
            user_agent: Reddit API user agent (defaults to environment variable)
            subreddits: List of subreddits to search (defaults to DEFAULT_SUBREDDITS)
        """
        self.client_id = client_id or REDDIT_CLIENT_ID
        self.client_secret = client_secret or REDDIT_CLIENT_SECRET
        self.user_agent = user_agent or REDDIT_USER_AGENT
        self.subreddits = subreddits or DEFAULT_SUBREDDITS
        self.reddit = None
        self.setup_client()

    def setup_client(self) -> None:
        """Set up the Reddit API client."""
        if not all([self.client_id, self.client_secret, self.user_agent]):
            logger.warning(
                "Reddit API credentials not complete. Reddit search will be skipped."
            )
            return

        try:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
                check_for_async=False,
                read_only=True,
            )
            # Verify the authentication worked
            logger.info(
                f"Reddit client initialized (read-only: {self.reddit.read_only})"
            )
            # Test the connection
            test_subreddit = self.reddit.subreddit("test")
            test_subreddit.title  # This will trigger an API call to verify authentication
        except Exception as e:
            logger.error(f"Failed to initialize Reddit client: {str(e)}")
            self.reddit = None

    def get_posts(
        self, ticker: str, search_query: Optional[str] = None, days: int = 2
    ) -> List[NewsArticle]:
        """Get posts and comments from Reddit about the stock.

        Args:
            ticker: Stock ticker symbol
            search_query: Search query in the form of "{ticker} {company_name}" (optional)
            days: How many days back to search for posts

        Returns:
            List of NewsArticle objects containing Reddit posts and discussions
        """
        if not self.reddit:
            logger.warning("Reddit client not available. Skipping Reddit search.")
            return []

        # Use search_query if provided, otherwise just use ticker
        effective_query = search_query if search_query else ticker
        logger.info(f"Searching Reddit for discussions about {effective_query}")
        articles = []
        cutoff_time = datetime.now() - timedelta(days=days)

        try:
            # We can search multiple subreddits at once using the '+' notation
            combined_subreddits = "+".join(self.subreddits)
            logger.info(f"Searching combined subreddits: {combined_subreddits}")

            # Create the multi-subreddit instance
            multi_subreddit = self.reddit.subreddit(combined_subreddits)

            # Search queries to try
            search_queries = []

            # If we have a search query (ticker + company name), use it for more targeted searches
            if search_query:
                search_queries = [
                    search_query,
                    f"{search_query} stock",
                    f"{search_query} price",
                ]
            else:
                # Fall back to ticker-only searches
                search_queries = [
                    ticker,
                    f"{ticker} stock",
                    f"{ticker} price",
                ]

            processed_permalinks: Set[str] = (
                set()
            )  # Keep track of already processed submissions
            other_tickers = [t for t in COMMON_TICKERS if t != ticker]

            # Search for the ticker with different queries
            articles.extend(
                self._search_with_queries(
                    multi_subreddit,
                    search_queries,
                    ticker,
                    other_tickers,
                    processed_permalinks,
                    cutoff_time,
                )
            )

            # Also search individual subreddits for better coverage
            for subreddit_name in self.subreddits:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    articles.extend(
                        self._search_subreddit_listings(
                            subreddit,
                            ticker,
                            other_tickers,
                            processed_permalinks,
                            cutoff_time,
                        )
                    )
                except Exception as sr_e:
                    logger.warning(
                        f"Error accessing subreddit {subreddit_name}: {str(sr_e)}"
                    )
                    continue

            logger.info(
                f"Found {len(articles)} Reddit posts for {ticker} across all subreddits"
            )

        except Exception as e:
            logger.error(f"Error in Reddit search process for {ticker}: {str(e)}")

        return articles

    def _search_with_queries(
        self,
        multi_subreddit,
        search_queries: List[str],
        ticker: str,
        other_tickers: List[str],
        processed_permalinks: Set[str],
        cutoff_time: datetime,
    ) -> List[NewsArticle]:
        """Search Reddit with multiple queries.

        Args:
            multi_subreddit: PRAW Subreddit object for searching multiple subreddits
            search_queries: List of search queries to try
            ticker: Stock ticker symbol
            other_tickers: List of other tickers to check for cross-contamination
            processed_permalinks: Set of already processed permalinks
            cutoff_time: Cutoff time for posts

        Returns:
            List of NewsArticle objects
        """
        articles = []

        for search_query in search_queries:
            logger.info(f"Searching with query: {search_query}")

            # Try different sort methods for more comprehensive results
            for sort in ["relevance", "hot", "new", "top"]:
                try:
                    for submission in multi_subreddit.search(
                        search_query, sort=sort, time_filter="week", limit=5
                    ):
                        article = self._process_submission(
                            submission,
                            ticker,
                            other_tickers,
                            processed_permalinks,
                            cutoff_time,
                        )
                        if article:
                            articles.append(article)
                except Exception as sort_e:
                    logger.warning(
                        f"Error with sort '{sort}' and query '{search_query}': {str(sort_e)}"
                    )
                    continue  # Try next sort method

        return articles

    def _search_subreddit_listings(
        self,
        subreddit,
        ticker: str,
        other_tickers: List[str],
        processed_permalinks: Set[str],
        cutoff_time: datetime,
    ) -> List[NewsArticle]:
        """Search a subreddit's listings for posts about a ticker.

        Args:
            subreddit: PRAW Subreddit object
            ticker: Stock ticker symbol
            other_tickers: List of other tickers to check for cross-contamination
            processed_permalinks: Set of already processed permalinks
            cutoff_time: Cutoff time for posts

        Returns:
            List of NewsArticle objects
        """
        articles = []

        # Check top and hot posts that might mention the ticker
        for listing_method in [subreddit.hot, subreddit.top]:
            try:
                for submission in listing_method(limit=50):
                    # Check if this post is relevant to the ticker
                    title_lower = submission.title.lower()
                    selftext_lower = (
                        submission.selftext.lower()
                        if hasattr(submission, "selftext")
                        else ""
                    )

                    # Determine if the post is primarily about this ticker
                    is_relevant = self._is_submission_relevant(
                        submission, ticker, other_tickers, title_lower, selftext_lower
                    )

                    if not is_relevant:
                        continue

                    # Process the submission if it's relevant
                    article = self._process_submission(
                        submission,
                        ticker,
                        other_tickers,
                        processed_permalinks,
                        cutoff_time,
                    )
                    if article:
                        articles.append(article)
            except Exception as listing_e:
                logger.warning(
                    f"Error with listing method in r/{subreddit.display_name}: {str(listing_e)}"
                )
                continue

        return articles

    def _is_submission_relevant(
        self,
        submission,
        ticker: str,
        other_tickers: List[str],
        title_lower: str,
        selftext_lower: str,
    ) -> bool:
        """Determine if a submission is relevant to the ticker.

        Args:
            submission: PRAW Submission object
            ticker: Stock ticker symbol
            other_tickers: List of other tickers to check for cross-contamination
            title_lower: Lowercase title of the submission
            selftext_lower: Lowercase selftext of the submission

        Returns:
            True if the submission is relevant, False otherwise
        """
        ticker_lower = ticker.lower()

        if ticker_lower in title_lower:
            # Check if another ticker appears more prominently in the title
            for other_ticker in other_tickers:
                if other_ticker.lower() in title_lower and title_lower.find(
                    other_ticker.lower()
                ) < title_lower.find(ticker_lower):
                    return False

            # If ticker is in the title and not overshadowed, it's likely relevant
            return True
        elif ticker_lower in selftext_lower:
            # If ticker is only in the body, check if it's mentioned prominently
            # Count occurrences of this ticker vs. other tickers
            ticker_count = selftext_lower.count(ticker_lower)
            other_ticker_counts = {
                other: selftext_lower.count(other.lower()) for other in other_tickers
            }

            # Skip if another ticker is mentioned more frequently
            if any(count > ticker_count for count in other_ticker_counts.values()):
                return False

            return True
        else:
            # Ticker not found in title or body
            return False

    def _process_submission(
        self,
        submission,
        ticker: str,
        other_tickers: List[str],
        processed_permalinks: Set[str],
        cutoff_time: datetime,
    ) -> Optional[NewsArticle]:
        """Process a submission and create a NewsArticle if relevant.

        Args:
            submission: PRAW Submission object
            ticker: Stock ticker symbol
            other_tickers: List of other tickers to check for cross-contamination
            processed_permalinks: Set of already processed permalinks
            cutoff_time: Cutoff time for posts

        Returns:
            NewsArticle object if the submission is relevant, None otherwise
        """
        # Skip if already processed
        if submission.permalink in processed_permalinks:
            return None

        # Check if this post is primarily about another ticker
        title_lower = submission.title.lower()

        # Skip if the title contains another ticker that appears more prominently
        for other_ticker in other_tickers:
            # If another ticker is in the title and our ticker isn't, or
            # if another ticker appears before our ticker in the title
            if (
                other_ticker.lower() in title_lower
                and ticker.lower() not in title_lower
            ) or (
                other_ticker.lower() in title_lower
                and title_lower.find(other_ticker.lower())
                < title_lower.find(ticker.lower())
            ):
                return None

        processed_permalinks.add(submission.permalink)

        created_time = datetime.fromtimestamp(submission.created_utc)
        # Skip if post is older than cutoff
        if created_time < cutoff_time:
            return None

        # Get the actual subreddit name from the submission
        subreddit_name = submission.subreddit.display_name

        # Compile content from post and top comments
        post_content = submission.selftext if hasattr(submission, "selftext") else ""
        content = f"Post: {post_content}\n\nTop comments:\n"

        # Try to get top comments, but don't fail the whole operation if it doesn't work
        try:
            # Get top 5 comments
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=0)  # Skip loading "more comments"

            for i, comment in enumerate(submission.comments[:5]):
                content += f"{i + 1}. {comment.body}\n"
        except Exception as comment_e:
            logger.warning(f"Error getting comments: {str(comment_e)}")
            content += "(Unable to fetch comments)\n"

        return NewsArticle(
            source="Reddit",
            subreddit=subreddit_name,
            title=submission.title,
            url=f"https://www.reddit.com{submission.permalink}",
            content=content,
            published_at=created_time,
        )
