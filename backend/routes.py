from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.ai_core.mock_generator import generate_mock_document
from backend.config import get_settings
from backend.models import DocumentRequest, GenerateResponse

router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    settings = get_settings()
    return {
        "app": settings.app_name,
        "message": "LegalEase API is running",
        "docs": "/docs",
    }


@router.get("/health")
def health() -> dict[str, str | bool]:
    settings = get_settings()
    return {
        "status": "ok",
        "ai_mode": "mock" if settings.use_mock_ai else "gemini",
        "model": settings.gemini_model,
    }


@router.post("/generate", response_model=GenerateResponse)
def generate(request: DocumentRequest) -> GenerateResponse:
    settings = get_settings()
    try:
        if settings.use_mock_ai:
            document = generate_mock_document(request)
            mode = "mock"
        else:
            document = GeminiDocumentGenerator(settings).generate_document(request)
            mode = "gemini"

        return GenerateResponse(
            success=True,
            mode=mode,
            model=settings.gemini_model,
            document=document,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Document generation failed: {exc}") from exc
