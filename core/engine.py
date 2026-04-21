from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from core.knowledge_base import retrieve_brand_context
from core.logger import get_logger, log_sanity
from core.prompts import BRAND_SYSTEM_PROMPT, build_user_prompt


HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
REQUIRED_KEYS = {"brand_name", "tagline", "palette", "typography", "tone", "social_strategy"}


class BrandGenerationError(Exception):
    """Raised when the model output cannot become a valid brand identity."""


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def _relative_luminance(hex_color: str) -> float:
    rgb = []
    for channel in _hex_to_rgb(hex_color):
        value = channel / 255
        rgb.append(value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def contrast_ratio(first: str, second: str) -> float:
    light = max(_relative_luminance(first), _relative_luminance(second))
    dark = min(_relative_luminance(first), _relative_luminance(second))
    return round((light + 0.05) / (dark + 0.05), 2)


def check_brand_consistency(brand: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    palette = brand.get("palette", {})
    pairs = [
        ("primary", "secondary"),
        ("secondary", "accent"),
    ]

    for left, right in pairs:
        left_color = palette.get(left, "")
        right_color = palette.get(right, "")
        if not HEX_RE.match(left_color) or not HEX_RE.match(right_color):
            warning = f"{left}/{right} contains an invalid hex color."
            warnings.append(warning)
            log_sanity(warning)
            continue

        ratio = contrast_ratio(left_color, right_color)
        if ratio < 4.5:
            warning = f"{left} and {right} contrast is {ratio}:1, below WCAG AA for body text."
            warnings.append(warning)
            log_sanity(warning)

    return warnings


def _validate_brand_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("error"):
        raise BrandGenerationError(str(payload["error"]))
    missing = REQUIRED_KEYS - set(payload)
    if missing:
        raise BrandGenerationError(f"Model response is missing: {', '.join(sorted(missing))}")

    palette = payload["palette"]
    for key in ("primary", "secondary", "accent"):
        color = palette.get(key)
        if not isinstance(color, str) or not HEX_RE.match(color):
            raise BrandGenerationError(f"Invalid {key} color returned by model.")

    social = payload["social_strategy"]
    if not isinstance(social, list) or len(social) != 5:
        raise BrandGenerationError("Model must return exactly five social strategy pillars.")

    return payload


def _fallback_identity(description: str, grounded_context: dict[str, str]) -> dict[str, Any]:
    text = description.lower()
    if "bank" in text or "fintech" in text:
        palette = {"primary": "#102A43", "secondary": "#F5F5F7", "accent": "#16A085"}
        name = "Northstar Ledger"
        fonts = {"heading": "Fraunces", "body": "Source Sans 3"}
    elif "cafe" in text or "coffee" in text or "dubai" in text:
        palette = {"primary": "#2F2A24", "secondary": "#F5F5F7", "accent": "#8A3B1D"}
        name = "Safa Table"
        fonts = {"heading": "Cormorant Garamond", "body": "Manrope"}
    elif "ai" in text or "saas" in text or "data" in text:
        palette = {"primary": "#111827", "secondary": "#F5F5F7", "accent": "#22D3EE"}
        name = "Signal Foundry"
        fonts = {"heading": "Sora", "body": "IBM Plex Sans"}
    else:
        palette = {"primary": "#1F2937", "secondary": "#F5F5F7", "accent": "#D97706"}
        name = "Fieldmark Studio"
        fonts = {"heading": "Outfit", "body": "Public Sans"}

    return {
        "brand_name": name,
        "tagline": "A sharper first impression for a faster launch.",
        "palette": palette,
        "typography": fonts,
        "tone": "The voice is precise, warm, and commercially confident. It explains value quickly while leaving enough texture to feel crafted rather than templated.",
        "social_strategy": [
            "Founder story and category point of view",
            "Customer problem breakdowns",
            "Behind-the-scenes product or service rituals",
            "Proof posts with testimonials, numbers, or demos",
            "Educational tips that make the buyer feel smarter",
        ],
        "grounding": grounded_context,
        "source": "fallback-demo",
        "token_count": 0,
    }


def generate_brand_identity(description: str) -> dict[str, Any]:
    load_dotenv()
    logger = get_logger()
    grounded_context = retrieve_brand_context(description)
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        logger.info("GROQ_API_KEY not set; using deterministic fallback identity.")
        brand = _fallback_identity(description, grounded_context)
    else:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": BRAND_SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(description, grounded_context)},
            ],
            temperature=0.72,
        )
        content = response.choices[0].message.content or "{}"
        try:
            brand = json.loads(content)
        except json.JSONDecodeError as exc:
            raise BrandGenerationError("Groq returned invalid JSON. Please try again.") from exc

        brand = _validate_brand_payload(brand)
        brand["grounding"] = grounded_context
        brand["source"] = "groq"
        brand["token_count"] = getattr(response.usage, "total_tokens", 0) if response.usage else 0

    brand["sanity_log"] = check_brand_consistency(brand)
    return brand


def save_brand_config(brand: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(brand, indent=2), encoding="utf-8")
