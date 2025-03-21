"""
OpenAI API client for generating summaries.

This module provides a client for interacting with the OpenAI API to generate
summaries of news articles and discussions.
"""

import logging
import os
from typing import Optional
import openai

logger = logging.getLogger("news_agent")

# OpenAI API config
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class OpenAIClient:
    """Client for interacting with the OpenAI API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OpenAI client.

        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        # Get the API key from the environment if not provided
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

        if not self.api_key:
            logger.warning(
                "OpenAI API key not set. Summarization will not be available."
            )
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=self.api_key)

    def generate_summary(
        self,
        content: str,
        ticker: str,
        price_change_percent: Optional[float] = None,
        source: str = "news",
    ) -> str:
        """Generate a summary using GPT-4.

        Args:
            content: The content to summarize
            ticker: Stock ticker symbol
            price_change_percent: Price change percentage (optional)
            source: Source of the content (e.g., "reddit", "news", "seeking_alpha")

        Returns:
            Summarized text from GPT-4
        """
        if not self.api_key:
            return "GPT-4 summarization not available (API key not set)."

        try:
            # Create prompt based on source and price change
            price_direction = (
                "increase"
                if price_change_percent and price_change_percent > 0
                else "decrease"
            )

            if source == "reddit":
                prompt = f"""Analyze these Reddit discussions about {ticker} stock and provide a concise, coherent summary that explains what Redditors believe is causing the stock's {price_direction} ({price_change_percent:.2f}% change). 
                Focus on the most insightful points about market sentiment, catalysts, and predictions. 
                Organize the summary into 3 key points with clear explanations that comprehensively captures the most insightful points. 
                Be specific about factors driving the price change.
                
                Reddit content:
                {content}
                """
            elif source == "seeking_alpha":
                prompt = f"""Analyze these Seeking Alpha articles about {ticker} stock and provide a concise, coherent summary that explains what analysts believe is causing the stock's {price_direction} ({price_change_percent:.2f}% change).
                Focus on the most insightful points about fundamentals, catalysts, and analyst opinions. 
                Organize the summary into 3 key points with clear explanations that comprehensively captures the most insightful points. 
                Be specific about factors driving the price change.
                
                Seeking Alpha content:
                {content}
                """
            else:  # General news
                prompt = f"""Analyze these news headlines and articles about {ticker} stock and provide a concise, coherent summary that explains what is likely causing the stock's {price_direction} ({price_change_percent:.2f}% change).
                Focus on the most important news, events, and market reactions. 
                Organize the summary into 3 key points with clear explanations that comprehensively captures the most insightful points. 
                Be specific about factors driving the price change.
                
                News content:
                {content}
                """

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial analyst specializing in stock market analysis. Provide concise, insightful summaries of market news and sentiment, as well as earnings-related news that may have direct impact to price change",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=500,
            )

            # Extract and return the summary
            summary = response.choices[0].message.content.strip()
            return summary

        except Exception as e:
            logger.error(f"Error generating GPT-4 summary: {str(e)}")
            return f"Error generating summary: {str(e)}"
