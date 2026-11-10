from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(
    title="JARVIS Cloud",
    version="0.1.0",
    description="Cloud communication service for the JARVIS assistant.",
    docs_url=None if os.getenv("JARVIS_ENV") == "production" else "/docs",
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


@app.get("/health")
async def health() -> dict[str, str]:
    """Public, non-sensitive liveness endpoint for hosting platforms."""
    return {"status": "ok", "service": "jarvis-cloud", "version": app.version}


@app.get("/api/status")
async def status() -> JSONResponse:
    """Report configured capabilities without exposing credentials."""
    voice_configured = bool(os.getenv("GEMINI_API_KEY"))
    return JSONResponse(
        {
            "service": "online",
            "voice": "provider_configured" if voice_configured else "not_configured",
            "desktop_agent": "not_connected",
        }
    )


@app.get("/", include_in_schema=False)
async def home() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/manifest.webmanifest", include_in_schema=False)
async def manifest() -> FileResponse:
    return FileResponse(
        WEB_DIR / "manifest.webmanifest",
        media_type="application/manifest+json",
    )


@app.get("/sw.js", include_in_schema=False)
async def service_worker() -> FileResponse:
    return FileResponse(
        WEB_DIR / "sw.js",
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"},
    )
