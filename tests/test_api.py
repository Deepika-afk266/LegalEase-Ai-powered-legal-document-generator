from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root_and_health() -> None:
    assert client.get("/").status_code == 200
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"


def test_generate_document() -> None:
    payload = {
        "document_type": "NDA (Non-Disclosure Agreement)",
        "parties": "Alice Smith (Disclosing Party), ABC Corp (Receiving Party)",
        "terms": "Confidentiality must be maintained; Term is 2 years; 15 days written notice",
        "effective_date": "April 10, 2026",
        "jurisdiction": "Tamil Nadu, India",
        "language": "English",
        "additional_instructions": "Use clear headings.",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["document"]["title"]
    assert body["document"]["clauses"]
