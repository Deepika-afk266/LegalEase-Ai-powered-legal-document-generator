from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import router


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Generative-AI legal document drafting "
        "assistant based on the LegalEase project specification."
    ),
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:8501",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    router
)


@app.get("/")
def root():

    return {
        "message": "LegalEase API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
        "ai_mode": settings.ai_mode,
        "model": settings.gemini_model,
    }