"""Entrypoint for generating Instagram-ready sports news assets."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Sequence

from caption_generator import generate_captions
from image_generator import create_image_cards
from news_scraper import NewsItem, get_daily_news

LOGGER = logging.getLogger(__name__)


def _build_output_directory(base_dir: os.PathLike[str] | str = "output") -> Path:
    today = datetime.today().strftime("%Y-%m-%d")
    output_dir = Path(base_dir) / today
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _create_captions(news_items: Sequence[NewsItem]) -> list[str]:
    captions = generate_captions(news_items)
    if not captions:
        raise RuntimeError("No captions were generated for the collected news items.")
    return captions


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    LOGGER.info("Collecting sports news…")
    news_items = get_daily_news()
    if not news_items:
        LOGGER.error("No news items could be fetched. Aborting run.")
        return

    LOGGER.info("Generating captions for %d articles…", len(news_items))
    captions = _create_captions(news_items)

    output_dir = _build_output_directory()
    create_image_cards(news_items, captions, output_dir)
    LOGGER.info("총 %d개의 인스타 콘텐츠가 생성되었습니다.", len(news_items))


if __name__ == "__main__":
    main()