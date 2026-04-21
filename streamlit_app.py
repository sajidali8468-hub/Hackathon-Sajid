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


def generate(description: str) -> dict:
    started = perf_counter()
    brand = generate_brand_identity(description)
    brand["latency_ms"] = round((perf_counter() - started) * 1000)
    return brand


def render_mock_homepage(brand: dict) -> None:
    st.html(
        f"""
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
    )


load_streamlit_secrets()

if "brand" not in st.session_state:
    st.session_state.brand = default_brand()

render_css(st.session_state.brand)

with st.sidebar:
    st.markdown("### Generation")
    has_key = bool(os.getenv("GROQ_API_KEY", "").strip())
    st.caption("Groq connected" if has_key else "Demo mode: add GROQ_API_KEY for live AI output")
    st.metric("Latency", f"{st.session_state.brand.get('latency_ms', 0)} ms")
    st.metric("Tokens", st.session_state.brand.get("token_count", 0))
    st.metric("Source", st.session_state.brand.get("source", "fallback-demo"))
    st.divider()
    sanity = st.session_state.brand.get("sanity_log") or ["Contrast checks passed."]
    st.markdown("### Sanity Log")
    for item in sanity:
        st.write(item)

left, right = st.columns([0.9, 1.1], gap="large")

with left:
    st.html('<section class="panel hero-panel">')
    st.html('<p class="overline">Prompt-to-Product</p>')
    st.html('<h1 class="hero-title">Brand Engine</h1>')
    st.html(
        '<p class="lede">Describe a startup and generate a grounded visual identity with palette, typography, tone, and social strategy.</p>',
    )

    with st.form("brand_form"):
        description = st.text_area(
            "Business description",
            value="A minimalist cafe in Dubai for founders who want quiet meetings, excellent coffee, and a refined local atmosphere.",
            height=190,
            max_chars=1200,
        )
        submitted = st.form_submit_button("Generate Identity", use_container_width=True)

    if submitted:
        try:
            with st.spinner("Designing the identity..."):
                st.session_state.brand = generate(description)
            st.rerun()
        except BrandGenerationError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Generation failed: {exc}")
    st.html("</section>")

with right:
    brand = st.session_state.brand
    palette = brand["palette"]
    st.html('<section class="panel preview-shell">')
    st.html('<p class="overline">Live Preview</p>')
    st.html(f'<h2 class="brand-heading">{escape(brand["brand_name"])}</h2>')
    st.html(
        f"""
        <div class="swatch-row">
          <div class="swatch" style="background:{palette["primary"]}"></div>
          <div class="swatch" style="background:{palette["secondary"]}"></div>
          <div class="swatch" style="background:{palette["accent"]}"></div>
        </div>
        """
    )

    preview_col, detail_col = st.columns([1.4, 0.8], gap="medium")
    with preview_col:
        render_mock_homepage(brand)
    with detail_col:
        strategy_items = "".join(
            f"<li>{escape(pillar)}</li>" for pillar in brand["social_strategy"]
        )
        st.html(
            f"""
            <section class="bento">
              <p class="overline">30-Day Social Pillars</p>
              <ol>{strategy_items}</ol>
            </section>
            """
        )

        st.html(
            f"""
            <section class="bento compact-card">
              <p class="overline">Grounding</p>
              <p>{escape(brand.get("grounding", {}).get("profile", "General Founder Brand"))}</p>
            </section>
            """
        )

        st.html(
            f"""
            <section class="bento compact-card">
              <p class="overline">Voice Guide</p>
              <p>{escape(brand["tone"])}</p>
            </section>
            """
        )
    st.html("</section>")
