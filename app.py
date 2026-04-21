from pathlib import Path
from time import perf_counter

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from core.engine import BrandGenerationError, generate_brand_identity, save_brand_config


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Prompt-to-Product Brand Engine",
    description="Transforms a startup description into a grounded visual identity.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class BrandRequest(BaseModel):
    description: str = Field(..., min_length=8, max_length=1200)


@app.get("/")
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/preview.html")
def preview() -> FileResponse:
    return FileResponse(STATIC_DIR / "preview.html")


@app.post("/api/generate")
def generate_identity(payload: BrandRequest):
    started = perf_counter()
    try:
        brand = generate_brand_identity(payload.description)
    except BrandGenerationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    brand["latency_ms"] = round((perf_counter() - started) * 1000)
    save_brand_config(brand, STATIC_DIR / "brand_config.json")
    return brand


@app.get("/api/current-brand")
def current_brand():
    config_path = STATIC_DIR / "brand_config.json"
    if not config_path.exists():
        raise HTTPException(status_code=404, detail="No brand has been generated yet.")
    return FileResponse(config_path)
