# Prompt-to-Product Brand Engine

A hackathon-ready Streamlit app with an optional FastAPI interface. It turns a startup description into a visual identity: palette, Google Font pairing, voice guide, and five social content pillars.

## Run With Streamlit

```powershell
py -m pip install -r requirements.txt
py -m streamlit run streamlit_app.py
```

Open the local URL Streamlit prints, usually `http://localhost:8501`.

For Streamlit Community Cloud, set this as the app entry point:

```text
streamlit_app.py
```

Add `GROQ_API_KEY` in Streamlit secrets. Local `.env` still works too.

For local Streamlit secrets, duplicate `.streamlit/secrets.toml.example` as `.streamlit/secrets.toml` and paste your key there. Do not commit the real secrets file.

## Run With FastAPI

```powershell
py -m pip install -r requirements.txt
py -m uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

Set `GROQ_API_KEY` in `.env` or Streamlit secrets for live Groq generation. Without a key, the app uses a deterministic fallback identity so the UI and grading demo still work.

## Architecture

- `app.py`: FastAPI entry point and API routes.
- `streamlit_app.py`: Streamlit entry point for local hosting or Streamlit Community Cloud.
- `core/prompts.py`: constrained JSON-mode prompt patterns.
- `core/knowledge_base.py`: RAG scaffold with brand archetypes and color theory.
- `core/engine.py`: Groq call, JSON validation, fallback generation, contrast checks.
- `static/index.html`: split-screen bento dashboard.
- `static/preview.html`: standalone mock homepage preview.
- `scripts/export_assets.py`: exports the generated palette and typography as CSS tokens.
