from __future__ import annotations

from io import BytesIO
import tempfile
from pathlib import Path

from fpdf import FPDF

from backend.models import GeneratedDocument
from backend.utils.text_utils import sanitize_text


class LegalPDF(FPDF):
    def __init__(self, logo_path: str | None = None) -> None:
        super().__init__(orientation="P", unit="mm", format="A4")
        self.logo_path = logo_path

    def header(self) -> None:
        if self.logo_path and Path(self.logo_path).exists():
            try:
                self.image(self.logo_path, x=93, y=10, w=24)
            except Exception:
                pass
        self.set_y(36)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 6, "LegalEase", align="C")
        self.ln(10)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, f"Generated with LegalEase - Draft for review - Page {self.page_no()}", align="C")


def build_pdf(document_data: GeneratedDocument, logo_bytes: bytes | None = None) -> bytes:
    temp_logo: str | None = None
    if logo_bytes:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.write(logo_bytes)
        tmp.close()
        temp_logo = tmp.name

    pdf = LegalPDF(temp_logo)
    pdf.set_margins(18, 18, 18)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 9, sanitize_text(document_data.title), align="C")
    pdf.ln(3)

    if document_data.introduction:
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(pdf.epw, 6, sanitize_text(document_data.introduction))
        pdf.ln(2)

    for section_text in document_data.sections:
        parts = section_text.split("\n", 1)
        heading = sanitize_text(parts[0].strip())
        body = sanitize_text(parts[1].strip()) if len(parts) > 1 else ""
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(pdf.epw, 7, heading)
        if body:
            pdf.set_font("Helvetica", size=10.5)
            pdf.multi_cell(pdf.epw, 5.5, body)
        pdf.ln(2)

    if document_data.clauses:
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(pdf.epw, 7, "KEY TERMS")
        pdf.set_font("Helvetica", size=10)
        for idx, clause in enumerate(document_data.clauses, 1):
            pdf.multi_cell(pdf.epw, 5.5, f"{idx}. {sanitize_text(clause)}")
        pdf.ln(2)

    if document_data.closing:
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(pdf.epw, 5.5, sanitize_text(document_data.closing))

    output = bytes(pdf.output())
    if temp_logo:
        try:
            Path(temp_logo).unlink(missing_ok=True)
        except Exception:
            pass
    return output
