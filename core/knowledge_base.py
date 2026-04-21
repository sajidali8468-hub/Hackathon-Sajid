from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BrandProfile:
    name: str
    signals: tuple[str, ...]
    psychology: str
    color_guidance: str
    archetype: str


COLOR_THEORY = {
    "trust": "Blue, deep green, and restrained neutrals communicate reliability, safety, and institutional confidence.",
    "energy": "Red, orange, and hot accent colors communicate momentum, urgency, appetite, and bold action.",
    "luxury": "Black, ivory, champagne, and metallic accents communicate scarcity, refinement, and premium positioning.",
    "wellness": "Soft greens, clay, warm whites, and low-saturation palettes communicate care, restoration, and balance.",
    "innovation": "Electric blue, cyan, lime, and crisp monochrome systems communicate intelligence and technological progress.",
    "community": "Warm coral, sunlit yellow, teal, and approachable neutrals communicate friendliness and belonging.",
}


BRAND_ARCHETYPES = [
    BrandProfile(
        name="Financial Trust",
        signals=("bank", "fintech", "insurance", "wealth", "payments", "accounting", "investment"),
        psychology=COLOR_THEORY["trust"],
        color_guidance="Prefer high-contrast navy, blue, green, or ink tones with one bright but controlled accent.",
        archetype="The Sage: clear, credible, calm, and useful.",
    ),
    BrandProfile(
        name="Food and Hospitality",
        signals=("cafe", "restaurant", "coffee", "bakery", "hotel", "hospitality", "dubai"),
        psychology=COLOR_THEORY["community"],
        color_guidance="Use warm neutrals or appetite-friendly accents balanced with a clean premium surface.",
        archetype="The Everyperson: welcoming, sensory, and easy to trust.",
    ),
    BrandProfile(
        name="Health and Care",
        signals=("clinic", "health", "wellness", "therapy", "care", "fitness", "medical"),
        psychology=COLOR_THEORY["wellness"],
        color_guidance="Choose soothing greens, blues, or warm soft tones with clinically legible contrast.",
        archetype="The Caregiver: reassuring, supportive, and grounded.",
    ),
    BrandProfile(
        name="Disruptive Technology",
        signals=("ai", "automation", "robot", "saas", "developer", "data", "cyber", "cloud"),
        psychology=COLOR_THEORY["innovation"],
        color_guidance="Use crisp dark-light contrast with one vivid innovation accent.",
        archetype="The Magician: transformative, precise, and future-facing.",
    ),
    BrandProfile(
        name="Bold Consumer Brand",
        signals=("fashion", "streetwear", "gaming", "creator", "music", "sports", "youth"),
        psychology=COLOR_THEORY["energy"],
        color_guidance="Use memorable, punchy contrast and avoid corporate blue unless the concept demands it.",
        archetype="The Rebel: provocative, confident, and culturally sharp.",
    ),
    BrandProfile(
        name="Premium Lifestyle",
        signals=("luxury", "jewelry", "real estate", "perfume", "concierge", "gallery", "private"),
        psychology=COLOR_THEORY["luxury"],
        color_guidance="Use restrained dark or ivory surfaces, small accent moments, and elegant typography.",
        archetype="The Ruler: composed, aspirational, and exacting.",
    ),
]


def retrieve_brand_context(description: str) -> dict[str, str]:
    text = description.lower()
    scored = []
    for profile in BRAND_ARCHETYPES:
        score = sum(1 for signal in profile.signals if signal in text)
        scored.append((score, profile))

    best_score, best_profile = max(scored, key=lambda item: item[0])
    if best_score == 0:
        best_profile = BrandProfile(
            name="General Founder Brand",
            signals=(),
            psychology="Use color meaning to clarify category expectations while leaving one distinctive memory hook.",
            color_guidance="Avoid generic palettes; choose a primary color that matches the category and an accent that adds personality.",
            archetype="The Creator: original, practical, and expressive.",
        )

    return {
        "profile": best_profile.name,
        "psychology": best_profile.psychology,
        "color_guidance": best_profile.color_guidance,
        "archetype": best_profile.archetype,
    }
