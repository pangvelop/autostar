"""Caption generation utilities."""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import Iterable, List, TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - import for typing only
    from transformers import Pipeline
else:  # pragma: no cover - runtime fallback when transformers isn't available
    Pipeline = Any

from news_scraper import NewsItem

LOGGER = logging.getLogger(__name__)
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
HF_TOKEN_ENV_VAR = "HUGGINGFACEHUB_API_TOKEN"


class CaptionGenerationError(RuntimeError):
    """Raised when captions cannot be generated using the requested backend."""


def _prompt_from_item(item: NewsItem) -> str:
    return (
        "You are a sports journalist creating short and engaging "
        "Instagram-style news posts.\n\n"
        "Write a stylish short paragraph (in <100 words) based on the following:\n\n"
        f"Title: {item.title}\n"
        f"Summary: {item.summary}\n\n"
        "Instagram Post:"
    )


@lru_cache(maxsize=1)
def _load_pipeline() -> "Pipeline":
    token = os.getenv(HF_TOKEN_ENV_VAR)
    if not token:
        raise CaptionGenerationError(
            "HuggingFace token not provided. Set the HUGGINGFACEHUB_API_TOKEN environment variable."
        )

    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    except ImportError as exc:  # pragma: no cover - depends on optional deps
        raise CaptionGenerationError("transformers package is not installed") from exc

    try:
        import torch
    except ImportError as exc:  # pragma: no cover - depends on optional deps
        raise CaptionGenerationError("torch package is not installed") from exc

    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=token)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            token=token,
            device_map="auto",
            torch_dtype=torch.float16,
        )
        return pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=300,
            temperature=0.7,
            top_p=0.95,
            repetition_penalty=1.1,
        )
    except Exception as exc:  # pragma: no cover - defensive: depends on env
        raise CaptionGenerationError(str(exc)) from exc


def _fallback_caption(item: NewsItem) -> str:
    """Return a deterministic, human readable fallback caption."""

    return (
        f"{item.title}\n"
        f"출처: {item.source}\n\n"
        f"핵심 요약: {item.summary[:250]}{'...' if len(item.summary) > 250 else ''}"
    )


def generate_caption(item: NewsItem) -> str:
    """Generate a caption for a single :class:`NewsItem`."""

    try:
        generator = _load_pipeline()
    except CaptionGenerationError as exc:
        LOGGER.warning("Falling back to simple caption: %s", exc)
        return _fallback_caption(item)

    prompt = _prompt_from_item(item)
    outputs = generator(prompt, do_sample=True)
    generated_text = outputs[0]["generated_text"]
    return generated_text.split("Instagram Post:")[-1].strip()


def generate_captions(items: Iterable[NewsItem]) -> List[str]:
    """Generate captions for each item in *items*."""

    return [generate_caption(item) for item in items]


__all__ = ["generate_captions"]
