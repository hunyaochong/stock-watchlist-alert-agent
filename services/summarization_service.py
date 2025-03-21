"""
Summarization service for generating summaries of news articles and discussions.

This module provides a service for generating summaries of news articles and
discussions using the OpenAI API.
"""

import logging
from typing import Dict, List, Optional
from models.news_models import NewsArticle
from clients.openai_client import OpenAIClient

logger = logging.getLogger("news_agent")


class SummarizationService:
    """Service for generating summaries of news articles and discussions."""

    def __init__(self, openai_client: Optional[OpenAIClient] = None):
        """Initialize the summarization service.

        Args:
            openai_client: OpenAI client for generating summaries
        """
        self.openai_client = openai_client or OpenAIClient()

    def summarize_seeking_alpha(
        self,
        articles: List[NewsArticle],
        ticker: str,
        price_change_percent: Optional[float] = None,
    ) -> str:
        """Summarize Seeking Alpha articles using GPT-4.

        Args:
            articles: List of NewsArticle objects from Seeking Alpha
            ticker: Stock ticker symbol
            price_change_percent: Price change percentage (optional)

        Returns:
            Summary text of key points from Seeking Alpha
        """
        if not articles:
            return "No relevant Seeking Alpha articles found."

        # Prepare content for GPT-4
        content = ""
        for article in articles:
            title = article.title
            article_content = article.content or ""
            # Truncate very long articles to avoid token limits
            if len(article_content) > 5000:
                article_content = article_content[:5000] + "... [truncated]"
            content += f"ARTICLE: {title}\n\n{article_content}\n\n---\n\n"

        # Generate summary using GPT-4
        if content:
            return self.openai_client.generate_summary(
                content, ticker, price_change_percent, "seeking_alpha"
            )
        else:
            return "No content available from Seeking Alpha articles."

    def summarize_google_news(
        self,
        articles: List[NewsArticle],
        ticker: str,
        price_change_percent: Optional[float] = None,
    ) -> str:
        """Summarize Google News articles using GPT-4.

        Args:
            articles: List of NewsArticle objects from Google News
            ticker: Stock ticker symbol
            price_change_percent: Price change percentage (optional)

        Returns:
            Summary text explaining key news factors affecting the stock price
        """
        if not articles:
            return "No relevant Google News articles found."

        # Prepare content for GPT-4
        content = "Recent headlines and news:\n\n"

        # Sort by published date (newest first)
        sorted_articles = sorted(
            articles,
            key=lambda x: x.published_at if x.published_at else None,
            reverse=True,
        )

        # Take up to 15 most recent articles
        for article in sorted_articles[:15]:
            source = article.source.replace("Google News - ", "")
            title = article.title
            article_content = article.content or ""
            # Truncate very long descriptions
            if len(article_content) > 1000:
                article_content = article_content[:1000] + "... [truncated]"
            content += f"HEADLINE: {title} ({source})\n"
            if article_content:
                content += f"CONTENT: {article_content}\n"
            content += "---\n"

        # Generate summary using GPT-4
        return self.openai_client.generate_summary(
            content, ticker, price_change_percent, "news"
        )

    def summarize_reddit_by_subreddit(
        self,
        articles: List[NewsArticle],
        ticker: str,
        price_change_percent: Optional[float] = None,
    ) -> Dict[str, str]:
        """Summarize Reddit posts grouped by subreddit using GPT-4.

        Args:
            articles: List of NewsArticle objects from Reddit
            ticker: Stock ticker symbol
            price_change_percent: Price change percentage (optional)

        Returns:
            Dictionary mapping subreddit names to summary text
        """
        subreddit_summaries = {}

        # Group articles by subreddit
        subreddit_articles = {}
        for article in articles:
            if article.subreddit:
                if article.subreddit not in subreddit_articles:
                    subreddit_articles[article.subreddit] = []
                subreddit_articles[article.subreddit].append(article)

        # Generate summary for each subreddit
        for subreddit, sub_articles in subreddit_articles.items():
            if not sub_articles:
                continue

            # Sort by published date (newest first)
            sorted_articles = sorted(
                sub_articles,
                key=lambda x: x.published_at if x.published_at else None,
                reverse=True,
            )

            # Prepare content for GPT-4
            content = f"Reddit discussions from r/{subreddit} about {ticker}:\n\n"

            for article in sorted_articles[:5]:  # Take up to 5 most recent discussions
                title = article.title
                post_content = article.content or ""
                # Truncate very long posts
                if len(post_content) > 3000:
                    post_content = post_content[:3000] + "... [truncated]"
                content += f"POST: {title}\n{post_content}\n---\n"

            # Generate summary using GPT-4
            subreddit_summaries[subreddit] = self.openai_client.generate_summary(
                content, ticker, price_change_percent, "reddit"
            )

        return subreddit_summaries

    def generate_concise_bullet_points(
        self,
        ticker: str,
        price_change_percent: float,
        seeking_alpha_summary: str,
        google_summary: str,
        reddit_summaries: Dict[str, str],
    ) -> str:
        """Generate concise bullet points summarizing all sources.

        Args:
            ticker: Stock ticker symbol
            price_change_percent: Price change percentage
            seeking_alpha_summary: Summary from Seeking Alpha
            google_summary: Summary from Google News
            reddit_summaries: Summaries from Reddit by subreddit

        Returns:
            Three concise bullet points capturing the essence of the price change
        """
        if not self.openai_client or not self.openai_client.api_key:
            return "GPT-4 summarization not available (API key not set)."

        try:
            # Combine all summaries
            combined_content = f"Seeking Alpha Summary:\n{seeking_alpha_summary}\n\n"
            combined_content += f"Google News Summary:\n{google_summary}\n\n"

            for subreddit, summary in reddit_summaries.items():
                combined_content += f"Reddit r/{subreddit} Summary:\n{summary}\n\n"

            # Create prompt for OpenAI
            direction = "increase" if price_change_percent > 0 else "decrease"
            prompt = f"""
            Based on the following summaries about {ticker} stock, create exactly 3 concise bullet points 
            that capture the most important factors driving the stock's {direction} of {abs(price_change_percent):.2f}%.
            
            Focus on the most significant and impactful factors mentioned across multiple sources.
            Each bullet point should be clear, specific, and directly related to the stock price movement.
            
            {combined_content}
            
            Return ONLY the 3 bullet points, numbered 1-3, with no introduction or conclusion.
            Each bullet point should be 1-2 sentences maximum.
            ENSURE THAT ALL BULLET POINTS ARE STRICTLY RELATED TO THE STOCK PRICE MOVMENT, PLEASE DO NOT INCLUDE FILLER NEWS THAT ARE NOT DIRECTLY RELATED TO THE STOCK
            IF THERE ARE NO NEWS ASSOCIATED WITH THE STOCK PRICE MOVEMENT, PLEASE JUST OMIT THE BULLET POINTS
            """

            # Call OpenAI API
            response = self.openai_client.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial analyst specializing in stock market analysis. Provide concise, insightful bullet points explaining stock price movements.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=300,
            )

            # Extract and return the bullet points
            bullet_points = response.choices[0].message.content.strip()
            return bullet_points

        except Exception as e:
            logger.error(
                f"Error generating concise bullet points for {ticker}: {str(e)}"
            )
            return f"Error generating concise bullet points: {str(e)}"
