"""Lightweight utilities for rendering caption cards."""

from __future__ import annotations

import logging
import os
import textwrap
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageDraw, ImageFont

from news_scraper import NewsItem

LOGGER = logging.getLogger(__name__)
CARD_SIZE = (800, 600)
BACKGROUND_COLOUR = "white"
TEXT_COLOUR = "black"
TEXT_START_Y = 100
TEXT_LINE_HEIGHT = 30
TEXT_WRAP_WIDTH = 40


def _ensure_output_directory(directory: os.PathLike[str] | str) -> Path:
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_image_cards(
    news_items: Sequence[NewsItem],
    captions: Iterable[str],
    output_dir: os.PathLike[str] | str,
) -> None:
    """Persist image cards and caption text files to *output_dir*."""

    output_path = _ensure_output_directory(output_dir)
    captions_list = list(captions)
    if len(news_items) != len(captions_list):
        LOGGER.warning(
            "Number of captions (%s) does not match number of news items (%s). Using the minimum count.",
            len(captions_list),
            len(news_items),
        )

    for idx, (item, caption) in enumerate(zip(news_items, captions_list), 1):
        img = Image.new("RGB", CARD_SIZE, color=BACKGROUND_COLOUR)
        drawer = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        lines = textwrap.wrap(item.title, width=TEXT_WRAP_WIDTH)
        y_text = TEXT_START_Y
        for line in lines:
            drawer.text((50, y_text), line, fill=TEXT_COLOUR, font=font)
            y_text += TEXT_LINE_HEIGHT

        image_path = output_path / f"post_{idx}.jpg"
        text_path = output_path / f"post_{idx}.txt"

        img.save(image_path)
        text_path.write_text(caption, encoding="utf-8")


__all__ = ["create_image_cards"]
