"""Utilities for scraping sports news from a handful of providers."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Iterable, List, Optional

import requests
from bs4 import BeautifulSoup

from utils.sentenceController import truncate_to_full_sentence

LOGGER = logging.getLogger(__name__)
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUEST_TIMEOUT = 10


@dataclass(slots=True)
class NewsItem:
    """Container describing a single scraped article."""

    title: str
    summary: str
    source: str
    url: Optional[str] = None


def _clean_text(text: str) -> str:
    """Normalise whitespace and strip surrounding spaces."""

    return re.sub(r"\s+", " ", text).strip()


def _fetch_html(url: str, *, headers: Optional[dict] = None) -> Optional[BeautifulSoup]:
    """Fetch *url* and return a :class:`BeautifulSoup` parser if successful."""

    try:
        response = requests.get(
            url,
            headers=headers or DEFAULT_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        LOGGER.warning("Failed to fetch %s: %s", url, exc)
        return None
    return BeautifulSoup(response.text, "html.parser")


def get_naver_sports_news(limit: int = 5) -> List[NewsItem]:
    """Return up to *limit* news items from Naver sports."""

    soup = _fetch_html("https://sports.news.naver.com/index")
    if soup is None:
        return []

    news_items: List[NewsItem] = []
    for item in soup.select(".today_item .text"):
        anchor = item.find("a")
        if not anchor or not anchor.get("href"):
            continue
        title = item.get_text(strip=True)
        link = anchor["href"]
        full_url = "https://sports.news.naver.com" + link
        summary = fetch_naver_article_summary(full_url)
        news_items.append(
            NewsItem(
                title=title,
                summary=summary,
                source="Naver Sports",
                url=full_url,
            )
        )
        if len(news_items) >= limit:
            break
    return news_items


def fetch_naver_article_summary(article_url: str) -> str:
    """Fetch and summarise a Naver article."""

    soup = _fetch_html(article_url)
    if soup is None:
        return "기사 내용을 불러오지 못했습니다."

    content = soup.select_one(".news_end") or soup.select_one("#newsEndContents")
    if not content:
        return "기사 내용을 불러오지 못했습니다."

    text = _clean_text(content.get_text())
    return truncate_to_full_sentence(text, max_len=300)


def get_espn_headlines(limit: int = 5) -> List[NewsItem]:
    """Return up to *limit* news items from ESPN."""

    base_url = "https://www.espn.com"
    soup = _fetch_html(base_url)
    if soup is None:
        return []

    news_items: List[NewsItem] = []
    for item in soup.select("section[class*='headlineStack'] li a"):
        href = item.get("href")
        if not href:
            continue
        title = item.get_text(strip=True)
        link = base_url + href if href.startswith("/") else href
        summary = fetch_espn_article_summary(link)
        news_items.append(
            NewsItem(
                title=title,
                summary=summary,
                source="ESPN",
                url=link,
            )
        )
        if len(news_items) >= limit:
            break
    return news_items


def fetch_espn_article_summary(url: str) -> str:
    """Fetch and summarise an ESPN article."""

    soup = _fetch_html(url)
    if soup is None:
        return "기사 내용을 불러오지 못했습니다."

    paragraphs = soup.select("p")
    text = " ".join(
        _clean_text(p.get_text()) for p in paragraphs if len(p.get_text()) > 50
    )
    if not text:
        return "기사 내용을 불러오지 못했습니다."
    return text[:300] + "..." if len(text) > 300 else text


def get_daily_news(limit_per_source: int = 5) -> List[NewsItem]:
    """Collect news from all providers."""

    providers: Iterable[List[NewsItem]] = (
        get_naver_sports_news(limit=limit_per_source),
        get_espn_headlines(limit=limit_per_source),
    )
    aggregated: List[NewsItem] = []
    for provider_items in providers:
        aggregated.extend(provider_items)
    return aggregated


__all__ = ["NewsItem", "get_daily_news"]
