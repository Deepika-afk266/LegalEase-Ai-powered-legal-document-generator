from typing import List

from pydantic import BaseModel, Field, field_validator


SUPPORTED_DOCUMENT_TYPES = [
    "Employment Contract",
    "Employment Offer Letter",
    "NDA (Non-Disclosure Agreement)",
    "Lease Agreement",
    "Freelance Work Contract",
    "Service Agreement",
    "General Agreement",
]


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=3, max_length=4000)
    terms: str = Field(..., min_length=3, max_length=12000)
    effective_date: str = Field(..., min_length=3, max_length=120)
    jurisdiction: str = Field(default="", max_length=200)
    language: str = Field(default="English", max_length=50)
    additional_instructions: str = Field(default="", max_length=3000)

    @field_validator("document_type", "parties", "terms", "effective_date")
    @classmethod
    def strip_required(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank.")
        return value


class GeneratedDocument(BaseModel):
    title: str
    introduction: str = ""
    sections: List[str] = Field(default_factory=list)
    clauses: List[str] = Field(default_factory=list)
    closing: str = ""
    warnings: List[str] = Field(default_factory=list)


class GenerateResponse(BaseModel):
    success: bool
    mode: str
    model: str
    document: GeneratedDocument
