from __future__ import annotations

from backend.models import GeneratedDocument
from backend.utils.text_utils import document_to_plain_text
from backend.document.docx_generator import build_docx
from backend.document.pdf_generator import build_pdf


def build_txt(document: GeneratedDocument) -> bytes:
    text = document_to_plain_text(
        document.title,
        document.introduction,
        document.sections,
        document.clauses,
        document.closing,
    )
    return text.encode("utf-8")


def build_docx_bytes(document: GeneratedDocument, logo_bytes: bytes | None = None) -> bytes:
    return build_docx(document, logo_bytes)


def build_pdf_bytes(document: GeneratedDocument, logo_bytes: bytes | None = None) -> bytes:
    return build_pdf(document, logo_bytes)
