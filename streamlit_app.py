from __future__ import annotations

from html import escape
import os
from pathlib import Path
from time import perf_counter

import streamlit as st

from core.engine import BrandGenerationError, generate_brand_identity


BASE_DIR = Path(__file__).resolve().parent
STREAMLIT_CSS = BASE_DIR / "static" / "streamlit.css"


st.set_page_config(
    page_title="Brand Engine",
    page_icon="BE",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_streamlit_secrets() -> None:
    for key in ("GROQ_API_KEY", "GROQ_MODEL"):
        try:
            value = st.secrets.get(key)
        except Exception:
            value = None
        if value and not os.getenv(key):
            os.environ[key] = str(value)


def render_css(brand: dict | None = None) -> None:
    palette = (brand or {}).get(
        "palette",
        {"primary": "#2F2A24", "secondary": "#F5F5F7", "accent": "#8A3B1D"},
    )
    typography = (brand or {}).get(
        "typography",
        {"heading": "Cormorant Garamond", "body": "Manrope"},
    )
    app_css = STREAMLIT_CSS.read_text(encoding="utf-8")
    st.html(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family={typography["heading"].replace(" ", "+")}:wght@400;600;700&family={typography["body"].replace(" ", "+")}:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
          :root {{
            --brand-primary: {palette["primary"]};
            --brand-secondary: {palette["secondary"]};
            --brand-accent: {palette["accent"]};
            --heading-font: "{typography["heading"]}", Georgia, serif;
            --body-font: "{typography["body"]}", system-ui, sans-serif;
          }}
          {app_css}
        </style>
        """
    )


def default_brand() -> dict:
    return {
        "brand_name": "Safa Table",
        "tagline": "A sharper first impression for a faster launch.",
        "palette": {"primary": "#2F2A24", "secondary": "#F5F5F7", "accent": "#8A3B1D"},
        "typography": {"heading": "Cormorant Garamond", "body": "Manrope"},
        "tone": "The voice is precise, warm, and commercially confident. It explains value quickly while leaving enough texture to feel crafted rather than templated.",
        "social_strategy": [
            "Founder story and category point of view",
            "Customer problem breakdowns",
            "Behind-the-scenes product or service rituals",
            "Proof posts with testimonials, numbers, or demos",
            "Educational tips that make the buyer feel smarter",
        ],
        "grounding": {"profile": "Food and Hospitality"},
        "source": "fallback-demo",
        "token_count": 0,
        "latency_ms": 0,
        "sanity_log": [],
    }


def get_grounding_label(brand: dict) -> str:
    return brand.get("grounding", {}).get("profile", "General Founder Brand")


def get_first_sentence(text: str) -> str:
    sentences = [segment.strip() for segment in text.split(".") if segment.strip()]
    if not sentences:
        return ""
    return f"{sentences[0]}."


def lower_start(text: str) -> str:
    if not text:
        return ""
    return text[0].lower() + text[1:]


def build_brand_bio(brand: dict) -> str:
    focus = brand.get("social_strategy", ["clear positioning"])[0]
    first_sentence = get_first_sentence(brand.get("tone", ""))
    return (
        f'{brand["brand_name"]} is a {get_grounding_label(brand).lower()} concept designed '
        "to make a stronger first impression. "
        f"{first_sentence} "
        f"The identity is built around {lower_start(focus)}, giving the business a brand "
        "system that feels distinctive, useful, and ready to launch."
    )


def build_launch_caption(brand: dict) -> str:
    proof = brand.get("social_strategy", ["clear customer insight"])[1]
    voice = get_first_sentence(brand.get("tone", "")).rstrip(".")
    return (
        f'Introducing {brand["brand_name"]} - {brand["tagline"]} '
        f"Built with a {lower_start(voice)} voice, a grounded palette, and a sharper point "
        f"of view. Start with {lower_start(proof)} and turn attention into trust."
    )


def build_taglines(brand: dict) -> list[str]:
    lead_word = brand["brand_name"].split(" ")[0]
    grounding = get_grounding_label(brand).lower()
    return [
        brand["tagline"],
        f"{lead_word} for sharper brand moments.",
        f"Clear positioning for {grounding}.",
        "A cleaner story, a stronger first impression.",
    ]


def build_messaging_style(brand: dict) -> str:
    tone = brand.get("tone", "").lower()
    if "warm" in tone and "confident" in tone:
        return "Concise, premium, persuasive, and human."
    if "precise" in tone:
        return "Sharp, intelligent, and grounded in value."
    return "Clear, distinctive, and launch-ready."


def build_ad_headline(brand: dict) -> str:
    return f'{brand["brand_name"]}: {brand["tagline"]}'


def build_positioning_note(brand: dict) -> str:
    pillar = brand.get("social_strategy", ["clear positioning"])[0]
    return (
        f'{brand["brand_name"]} stands out with a more intentional point of view, stronger '
        f"trust cues, and content built around {lower_start(pillar)} instead of generic "
        "marketing language."
    )


def derive_outputs(brand: dict) -> dict:
    return {
        "brand_bio": build_brand_bio(brand),
        "launch_caption": build_launch_caption(brand),
        "taglines": build_taglines(brand),
        "messaging_style": build_messaging_style(brand),
        "ad_headline": build_ad_headline(brand),
        "positioning_note": build_positioning_note(brand),
        "font_pairing": f'{brand["typography"]["heading"]} + {brand["typography"]["body"]}',
        "moodboard": (
            f"{get_grounding_label(brand)}, refined color contrast, and a brand voice that "
            "feels deliberate rather than generic."
        ),
    }


def generation_steps(status: str = "ready", detail: str = "") -> list[dict[str, str]]:
    if status == "complete":
        return [
            {
                "state": "complete",
                "title": "Analyze the brief",
                "detail": "Mapped the category, audience, and whitespace opportunity.",
            },
            {
                "state": "complete",
                "title": "Ground the brand",
                "detail": "Matched the idea to an industry profile and positioning cues.",
            },
            {
                "state": "complete",
                "title": "Generate identity",
                "detail": "Created the name, tagline, palette, typography, and tone.",
            },
            {
                "state": "complete",
                "title": "Validate the system",
                "detail": "Checked the brand payload and contrast sanity notes.",
            },
            {
                "state": "complete",
                "title": "Prepare launch assets",
                "detail": "Built the social plan, bio, launch caption, and tagline set.",
            },
        ]
    if status == "error":
        return [
            {
                "state": "error",
                "title": "Generation needs attention",
                "detail": detail or "The current request could not be completed.",
            }
        ]
    return [
        {
            "state": "ready",
            "title": "Ready to generate",
            "detail": "Submit a startup description to build the brand system and launch assets.",
        },
        {
            "state": "pending",
            "title": "Derived outputs",
            "detail": "Brand bio, launch caption, and tagline variations will appear after generation.",
        },
    ]


def set_brand_state(brand: dict) -> None:
    st.session_state.brand = brand
    st.session_state.outputs = derive_outputs(brand)
    st.session_state.generation_steps = generation_steps("complete")


def initialize_state() -> None:
    if "brand" not in st.session_state:
        st.session_state.brand = default_brand()
    if "outputs" not in st.session_state:
        st.session_state.outputs = derive_outputs(st.session_state.brand)
    if "generation_steps" not in st.session_state:
        st.session_state.generation_steps = generation_steps()


def generate(description: str) -> dict:
    started = perf_counter()
    brand = generate_brand_identity(description)
    brand["latency_ms"] = round((perf_counter() - started) * 1000)
    return brand


def render_step_flow(steps: list[dict[str, str]]) -> None:
    items = []
    for index, step in enumerate(steps, start=1):
        items.append(
            f"""
            <article class="step-card step-card--{escape(step["state"])}">
              <span class="step-card__number">{index:02d}</span>
              <div>
                <strong>{escape(step["title"])}</strong>
                <p>{escape(step["detail"])}</p>
              </div>
            </article>
            """
        )
    st.html(f'<section class="panel flow-panel">{"".join(items)}</section>')


def render_mock_homepage_html(brand: dict) -> str:
    return f"""
    <section class="mock-homepage">
      <div class="mock-nav">
        <strong>{escape(brand["brand_name"])}</strong>
        <span>Launch</span>
      </div>
      <div class="mock-hero">
        <p class="overline">Generated Brand System</p>
        <h2>{escape(brand["tagline"])}</h2>
        <p>{escape(brand["tone"])}</p>
        <div class="mock-cta">Start the story</div>
      </div>
    </section>
    """


def render_text_card(title: str, body: str, extra_class: str = "") -> None:
    card_class = f"output-card {extra_class}".strip()
    st.html(
        f"""
        <section class="{card_class}">
          <p class="overline">{escape(title)}</p>
          <p>{escape(body)}</p>
        </section>
        """
    )


load_streamlit_secrets()
initialize_state()
render_css(st.session_state.brand)

with st.sidebar:
    st.markdown("### Session")
    st.caption(
        "Groq connected"
        if bool(os.getenv("GROQ_API_KEY", "").strip())
        else "Demo mode: add GROQ_API_KEY for live AI output"
    )
    st.metric("Latency", f'{st.session_state.brand.get("latency_ms", 0)} ms')
    st.metric("Tokens", st.session_state.brand.get("token_count", 0))
    st.metric("Source", st.session_state.brand.get("source", "fallback-demo"))
    st.divider()
    st.markdown("### Working Outputs")
    st.write("Generate Identity")
    st.write("Write Brand Bio")
    st.write("Create Launch Caption")
    st.write("Spin Taglines")

left, center, right = st.columns([0.82, 1.24, 0.94], gap="large")

with left:
    st.html('<p class="overline">Prompt-to-Product</p>')
    st.html('<h1 class="hero-title">Brand Engine</h1>')
    st.html(
        '<p class="lede">Describe a startup and generate a grounded visual identity with palette, typography, tone, and social strategy.</p>'
    )

    with st.form("brand_form"):
        description = st.text_area(
            "Business description",
            value="A minimalist cafe in Dubai for founders who want quiet meetings, excellent coffee, and a refined local atmosphere.",
            height=180,
            max_chars=1200,
        )
        submitted = st.form_submit_button("Generate Identity", use_container_width=True)

    if submitted:
        try:
            with st.spinner("Designing the identity..."):
                brand = generate(description)
            set_brand_state(brand)
        except BrandGenerationError as exc:
            st.session_state.generation_steps = generation_steps("error", str(exc))
            st.error(str(exc))
        except Exception as exc:
            st.session_state.generation_steps = generation_steps("error", str(exc))
            st.error(f"Generation failed: {exc}")

    action_cols = st.columns(3, gap="small")
    with action_cols[0]:
        bio_clicked = st.button("Write Brand Bio", use_container_width=True)
    with action_cols[1]:
        caption_clicked = st.button("Create Launch Caption", use_container_width=True)
    with action_cols[2]:
        taglines_clicked = st.button("Spin Taglines", use_container_width=True)

    if bio_clicked:
        outputs = dict(st.session_state.outputs)
        outputs["brand_bio"] = build_brand_bio(st.session_state.brand)
        st.session_state.outputs = outputs
    if caption_clicked:
        outputs = dict(st.session_state.outputs)
        outputs["launch_caption"] = build_launch_caption(st.session_state.brand)
        st.session_state.outputs = outputs
    if taglines_clicked:
        outputs = dict(st.session_state.outputs)
        outputs["taglines"] = build_taglines(st.session_state.brand)
        st.session_state.outputs = outputs

    metrics_top = st.columns(2, gap="small")
    with metrics_top[0]:
        st.metric("Latency", f'{st.session_state.brand.get("latency_ms", 0)} ms')
    with metrics_top[1]:
        st.metric("Tokens", st.session_state.brand.get("token_count", 0))

    st.metric("Grounding", get_grounding_label(st.session_state.brand))

with center:
    brand = st.session_state.brand
    outputs = st.session_state.outputs
    palette = brand["palette"]

    st.html(
        f"""
        <section class="panel preview-shell">
          <p class="overline">Live Preview</p>
          <h2 class="brand-heading">{escape(brand["brand_name"])}</h2>
          <div class="swatch-row">
            <div class="swatch" style="background:{palette["primary"]}"></div>
            <div class="swatch" style="background:{palette["secondary"]}"></div>
            <div class="swatch" style="background:{palette["accent"]}"></div>
          </div>
          {render_mock_homepage_html(brand)}
        </section>
        """
    )

    output_left, output_right = st.columns(2, gap="medium")
    with output_left:
        render_text_card("Brand Bio", outputs["brand_bio"])
    with output_right:
        render_text_card("Launch Caption", outputs["launch_caption"])

    tagline_markup = "".join(f"<li>{escape(item)}</li>" for item in outputs["taglines"])
    st.html(
        f"""
        <section class="output-card output-card--wide">
          <p class="overline">Tagline Variations</p>
          <ul class="output-list">{tagline_markup}</ul>
        </section>
        """
    )

    render_step_flow(st.session_state.generation_steps)

with right:
    brand = st.session_state.brand
    outputs = st.session_state.outputs
    strategy_items = "".join(
        f"<li>{escape(pillar)}</li>" for pillar in brand["social_strategy"]
    )
    sanity_items = brand.get("sanity_log") or ["Contrast checks passed."]
    sanity_markup = "".join(f"<li>{escape(item)}</li>" for item in sanity_items)

    st.html(
        f"""
        <section class="panel side-stack">
          <section class="bento">
            <p class="overline">30-Day Social Pillars</p>
            <ol>{strategy_items}</ol>
          </section>
          <section class="bento compact-card">
            <p class="overline">Voice Guide</p>
            <p>{escape(brand["tone"])}</p>
          </section>
          <section class="bento compact-card">
            <p class="overline">Sanity Log</p>
            <ul class="output-list">{sanity_markup}</ul>
          </section>
        </section>
        """
    )

    side_left, side_right = st.columns(2, gap="medium")
    with side_left:
        render_text_card("Messaging Style", outputs["messaging_style"])
        render_text_card("Font Pairing", outputs["font_pairing"], "tight-card")
    with side_right:
        render_text_card("Ad Headline", outputs["ad_headline"])
        render_text_card("Grounding", get_grounding_label(brand), "tight-card")

    render_text_card("Positioning Note", outputs["positioning_note"], "output-card--wide")
    render_text_card("Moodboard Direction", outputs["moodboard"], "tight-card")
