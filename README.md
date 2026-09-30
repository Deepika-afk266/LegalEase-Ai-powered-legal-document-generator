# LegalEase — AI-Powered Legal Document Generator

LegalEase is a full-stack prototype based on the supplied project documentation. It uses:

- Streamlit for the user interface
- FastAPI for the backend API
- Google Gemini through the current `google-genai` SDK
- Structured output with Pydantic models
- python-docx for DOCX export
- FPDF2 for PDF export
- Plain TXT export
- Optional offline mock generation so the UI/export pipeline can be tested without an API key

## Important model note

The supplied document specifies Gemini 1.5 Pro and `google-generativeai`. Those are kept as the conceptual reference in the project documentation, but the implementation uses the current Google GenAI SDK and a configurable current model (`gemini-3.8-flash` by default). Change `GEMINI_MODEL` in `.env` when you need another model.

## Disclaimer

LegalEase is a drafting aid. Generated text can contain omissions or errors and should be reviewed by a qualified legal professional before use. The application does not represent that a generated document is legally valid in a particular jurisdiction.

## Project layout

```text
LegalEase/
├── assets/
│   └── logo.png
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── ai_core/
│   │   ├── __init__.py
│   │   ├── gemini_generator.py
│   │   ├── mock_generator.py
│   │   └── prompts.py
│   ├── document/
│   │   ├── __init__.py
│   │   ├── docx_generator.py
│   │   ├── export_service.py
│   │   └── pdf_generator.py
│   └── utils/
│       ├── __init__.py
│       └── text_utils.py
├── frontend/
│   └── app.py
├── tests/
│   ├── test_api.py
│   └── test_documents.py
├── .env.example
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Windows / VS Code quick start

1. Open the `LegalEase` folder in VS Code.
2. In the VS Code terminal create a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`. To use the real Gemini API, put your API key in `GEMINI_API_KEY`. For a no-key demo set `AI_MODE=mock`.
4. Start the backend in Terminal 1:

```powershell
.\.venv\Scripts\activate
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

5. Start the frontend in Terminal 2:

```powershell
.\.venv\Scripts\activate
streamlit run frontend\app.py
```

6. Open `http://127.0.0.1:8501`. The FastAPI interactive API is at `http://127.0.0.1:8000/docs`.

### Offline test mode

Set `AI_MODE=mock` in `.env`. The complete frontend → FastAPI → generation → editing → export pipeline works without a Gemini API key.

### Automated tests

```powershell
.\.venv\Scripts\activate
$env:PYTHONPATH='.'
pytest -q
```

### Docker Compose

```powershell
docker compose up --build
```

This starts FastAPI on port 8000 and Streamlit on port 8501.
