"""
Data models for the news agent.

This module defines the data models used throughout the news agent application.
"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    """Model representing a news article."""

    source: str = Field(
        ..., description="Source of the news (SeekingAlpha, Reddit, Google)"
    )
    title: str = Field(..., description="Title of the article or post")
    url: Optional[str] = Field(None, description="URL to the article")
    content: Optional[str] = Field(
        None, description="Content or summary of the article"
    )
    published_at: Optional[datetime] = Field(None, description="Publication date")
    subreddit: Optional[str] = Field(None, description="Subreddit name if from Reddit")


class StockNews(BaseModel):
    """Model representing all news for a specific stock."""

    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: Optional[str] = Field(None, description="Company name")
    price_change_percent: Optional[float] = Field(
        None, description="Price change percentage"
    )
    summary_seeking_alpha: Optional[str] = Field(
        None, description="Summary from Seeking Alpha"
    )
    summary_google: Optional[str] = Field(None, description="Summary from Google RSS")
    summary_reddit: Dict[str, str] = Field(
        default_factory=dict, description="Summaries from Reddit keyed by subreddit"
    )
    articles: List[NewsArticle] = Field(
        default_factory=list, description="List of all news articles"
    )
