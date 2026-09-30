from backend.models import DocumentRequest, GeneratedDocument
from backend.utils.text_utils import split_semicolon_terms


def generate_mock_document(request: DocumentRequest) -> GeneratedDocument:
    terms = split_semicolon_terms(request.terms)
    title = request.document_type.strip()
    clauses = terms or ["The parties shall perform their obligations in good faith."]
    warnings = [
        "Offline demo mode is enabled. This draft was generated locally and not by Gemini.",
        "Review the document for jurisdiction-specific requirements before use.",
    ]
    if not request.jurisdiction:
        warnings.append("Jurisdiction was not specified; governing-law language should be reviewed.")

    sections = [
        f"PARTIES\nThis {request.document_type.lower()} is entered into by the parties identified by the user: {request.parties}.",
        f"EFFECTIVE DATE\nThe intended effective date provided by the user is {request.effective_date}.",
        "PURPOSE AND SCOPE\nThe purpose and scope of this document should be interpreted from the user-supplied terms and the selected document type.",
        "OBLIGATIONS\nEach party is responsible for the obligations expressly stated in this draft and any terms accepted by the parties.",
        "TERM AND TERMINATION\nThe parties should review the desired duration, renewal mechanism, and termination notice requirements before execution.",
        "GOVERNING LAW\nThe governing law and dispute-resolution provisions should be completed or confirmed for the intended jurisdiction.",
        "SIGNATURES\nEach party should sign and date the final version where applicable.",
    ]
    closing = "This is a draft for review and editing. It is not a substitute for legal advice."
    return GeneratedDocument(
        title=title,
        introduction="LegalEase draft generated in offline demo mode from the supplied inputs.",
        sections=sections,
        clauses=clauses,
        closing=closing,
        warnings=warnings,
    )
