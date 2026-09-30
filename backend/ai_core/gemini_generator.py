from __future__ import annotations

from backend.config import Settings
from backend.models import DocumentRequest, GeneratedDocument
from backend.ai_core.prompts import SYSTEM_INSTRUCTION, build_prompt


class GeminiDocumentGenerator:
    """Generate structured legal drafting content using Gemini."""

    def __init__(self, settings: Settings) -> None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        self.settings = settings
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "Google GenAI SDK is not installed. Run: pip install -r requirements.txt"
            ) from exc
        self.genai = genai
        from google.genai import types
        self.types = types
        self.client = genai.Client(api_key=settings.gemini_api_key)

    def generate_document(self, request: DocumentRequest) -> GeneratedDocument:
        prompt = build_prompt(request)
        config = self.types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
            max_output_tokens=5000,
            response_mime_type="application/json",
            response_schema=GeneratedDocument,
        )
        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=config,
        )
        if not getattr(response, "text", None):
            raise RuntimeError("Gemini returned an empty response.")
        if getattr(response, "parsed", None) is not None:
            parsed = response.parsed
            if isinstance(parsed, GeneratedDocument):
                return parsed
            return GeneratedDocument.model_validate(parsed)
        return GeneratedDocument.model_validate_json(response.text)
