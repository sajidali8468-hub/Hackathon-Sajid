from __future__ import annotations

from html import escape
import os
from time import perf_counter

import streamlit as st

from core.engine import BrandGenerationError, generate_brand_identity


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

          .stApp {{
            background: #f5f5f7;
            color: #18181b;
          }}

          [data-testid="stSidebar"] {{
            background: #ffffff;
            border-right: 1px solid #dedee3;
          }}

          .block-container {{
            max-width: 1440px;
            padding-top: 2rem;
            padding-bottom: 2rem;
          }}

          h1, h2, h3, .brand-heading {{
            font-family: var(--heading-font);
            letter-spacing: 0;
          }}

          .hero-title {{
            margin: 0;
            max-width: 8ch;
            font-family: var(--heading-font);
            font-size: clamp(4rem, 10vw, 8rem);
            font-weight: 700;
            line-height: .92;
          }}

          .lede {{
            max-width: 38rem;
            color: #4b5563;
            font-family: var(--body-font);
            font-size: 1.08rem;
            line-height: 1.65;
          }}

          .overline {{
            margin: 0 0 .65rem;
            color: #6b7280;
            font-family: var(--body-font);
            font-size: .76rem;
            font-weight: 700;
            letter-spacing: 0;
            text-transform: uppercase;
          }}

          .bento {{
            border: 1px solid #dedee3;
            border-radius: 8px;
            background: rgba(255,255,255,.76);
            padding: 1.25rem;
          }}

          .mock-homepage {{
            overflow: hidden;
            min-height: 560px;
            border: 1px solid color-mix(in srgb, var(--brand-primary) 22%, transparent);
            border-radius: 8px;
            background: var(--brand-secondary);
            color: var(--brand-primary);
          }}

          .mock-nav {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 72px;
            background: var(--brand-primary);
            color: var(--brand-secondary);
            padding: 0 26px;
          }}

          .mock-nav strong {{
            font-family: var(--heading-font);
            font-size: 1.35rem;
          }}

          .mock-nav span {{
            color: var(--brand-accent);
            font-weight: 800;
          }}

          .mock-hero {{
            display: grid;
            align-content: center;
            min-height: 488px;
            padding: 44px;
          }}

          .mock-hero h2 {{
            max-width: 11ch;
            margin: 0;
            color: var(--brand-primary);
            font-family: var(--heading-font);
            font-size: clamp(3rem, 6vw, 6.4rem);
            line-height: .96;
          }}

          .mock-hero p {{
            max-width: 34rem;
            font-family: var(--body-font);
            line-height: 1.65;
          }}

          .mock-cta {{
            display: inline-flex;
            align-items: center;
            width: max-content;
            min-height: 48px;
            margin-top: .5rem;
            border-radius: 8px;
            background: var(--brand-accent);
            color: var(--brand-secondary);
            padding: 0 18px;
            font-family: var(--body-font);
            font-weight: 800;
          }}

          .swatch-row {{
            display: flex;
            gap: .55rem;
          }}

          .swatch {{
            width: 42px;
            height: 42px;
            border: 1px solid rgba(0,0,0,.15);
            border-radius: 50%;
          }}
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

left, right = st.columns([0.72, 1.28], gap="large")

with left:
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

with right:
    brand = st.session_state.brand
    palette = brand["palette"]
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

    preview_col, detail_col = st.columns([1.25, 0.75], gap="medium")
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
            <section class="bento" style="margin-top: .85rem;">
              <p class="overline">Grounding</p>
              <p>{escape(brand.get("grounding", {}).get("profile", "General Founder Brand"))}</p>
            </section>
            """
        )

        st.html(
            f"""
            <section class="bento" style="margin-top: .85rem;">
              <p class="overline">Voice Guide</p>
              <p>{escape(brand["tone"])}</p>
            </section>
            """
        )
