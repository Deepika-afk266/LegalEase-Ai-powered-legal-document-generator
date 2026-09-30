from __future__ import annotations

import base64

import requests
import streamlit as st


BACKEND_URL ="http://127.0.0.1:8000",



st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 0.15rem;
    }

    .subtitle {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }

    .card {
        background: #111827;
        padding: 1.1rem;
        border-radius: 16px;
        border: 1px solid #263449;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered legal document drafting, editing and export'
    '</div>',
    unsafe_allow_html=True,
)


with st.sidebar:

    st.header("Settings")

    backend_override = st.text_input(
        "Backend URL",
        value=BACKEND_URL,
    )

    BACKEND_URL = (
        backend_override.rstrip("/")
    )

    st.caption(
        "The backend and frontend are separate "
        "services, matching the project architecture."
    )

    st.divider()

    st.subheader("Workflow")

    st.write("1. Enter details")
    st.write("2. Generate AI draft")
    st.write("3. Review and edit")
    st.write("4. Export TXT / DOCX / PDF")


left, right = st.columns(
    [1, 1.2],
    gap="large",
)


with left:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.subheader(
        "1. Document Details"
    )

    document_type = st.selectbox(
        "Document type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Freelance Work Contract",
            "Employment Offer Letter",
            "Service Agreement",
            "General Contract",
        ],
    )

    parties = st.text_area(
        "Parties involved",
        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=100,
    )

    effective_date = st.text_input(
        "Effective date",
        placeholder="April 10, 2026",
    )

    jurisdiction = st.text_input(
        "Jurisdiction",
        value="Not specified",
    )

    language = st.selectbox(
        "Language",
        [
            "English",
            "Tamil",
            "Hindi",
            "Malayalam",
            "Telugu",
        ],
    )

    terms_raw = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=150,
        help=(
            "Separate each term with a semicolon "
            "or a new line."
        ),
    )

    additional = st.text_area(
        "Additional instructions (optional)",
        placeholder=(
            "Use clear numbered clauses and "
            "include a concise review note."
        ),
        height=100,
    )

    logo_file = st.file_uploader(
        "Optional company logo",
        type=[
            "png",
            "jpg",
            "jpeg",
        ],
    )

    company_name = st.text_input(
        "Company / branding name",
        value="LegalEase",
    )

    generate_clicked = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True,
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


if generate_clicked:

    terms = [
        t.strip()
        for t in terms_raw.replace(
            "\n",
            ";",
        ).split(";")
        if t.strip()
    ]

    if (
        not parties.strip()
        or not effective_date.strip()
        or not terms
    ):

        st.error(
            "Please provide parties, effective date, "
            "and at least one term."
        )

    else:

        payload = {
            "document_type":
                document_type,

            "parties":
                parties.strip(),

            "terms":
                terms,

            "effective_date":
                effective_date.strip(),

            "jurisdiction":
                jurisdiction.strip()
                or "Not specified",

            "language":
                language,

            "additional_instructions":
                additional.strip(),
        }

        try:

            with st.spinner(
                "Generating your document..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )

            if response.ok:

                result = response.json()

                st.session_state[
                    "document"
                ] = result["document"]

                st.session_state[
                    "text"
                ] = result["text"]

                st.session_state[
                    "ai_mode"
                ] = result.get(
                    "ai_mode",
                    "unknown",
                )

                st.session_state[
                    "model"
                ] = result.get(
                    "model",
                    "unknown",
                )

                st.success(
                    "Document generated using "
                    f"{st.session_state['ai_mode']} mode."
                )

            else:

                st.error(
                    f"Backend error "
                    f"{response.status_code}: "
                    f"{response.text}"
                )

        except requests.RequestException as exc:

            st.error(
                "Cannot connect to FastAPI backend: "
                f"{exc}"
            )


with right:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.subheader(
        "2. Preview & Edit"
    )

    if (
        "document"
        not in st.session_state
    ):

        st.info(
            "Generate a document to see "
            "the editable preview here."
        )

    else:

        doc = st.session_state[
            "document"
        ]

        st.caption(
            f"AI mode: "
            f"{st.session_state.get('ai_mode', 'unknown')} "
            f"| Model: "
            f"{st.session_state.get('model', 'unknown')}"
        )

        edited = st.text_area(
            "Editable document text",
            value=st.session_state.get(
                "text",
                "",
            ),
            height=580,
            key="editor",
        )

        st.session_state[
            "text"
        ] = edited

        st.markdown(
            "**Review warnings**"
        )

        for warning in doc.get(
            "warnings",
            [],
        ):

            st.warning(
                warning
            )

        logo_base64 = ""

        if logo_file is not None:

            logo_base64 = (
                base64.b64encode(
                    logo_file.getvalue()
                ).decode("utf-8")
            )

        col1, col2, col3 = st.columns(3)

        for col, fmt in zip(
            (
                col1,
                col2,
                col3,
            ),
            (
                "txt",
                "docx",
                "pdf",
            ),
        ):

            with col:

                if st.button(
                    f"Download {fmt.upper()}",
                    use_container_width=True,
                    key=f"export_{fmt}",
                ):

                    export_payload = {
                        "document_type":
                            document_type,

                        "title":
                            doc.get(
                                "title",
                                document_type,
                            ),

                        "text":
                            st.session_state[
                                "text"
                            ],

                        "company_name":
                            company_name,

                        "logo_base64":
                            logo_base64,
                    }

                    try:

                        r = requests.post(
                            f"{BACKEND_URL}/export/{fmt}",
                            json=export_payload,
                            timeout=60,
                        )

                        if r.ok:

                            st.download_button(
                                label=(
                                    f"Save "
                                    f"{fmt.upper()} file"
                                ),

                                data=r.content,

                                file_name=(
                                    f"legalease_document."
                                    f"{fmt}"
                                ),

                                mime=r.headers.get(
                                    "content-type",
                                    "application/octet-stream",
                                ),

                                use_container_width=True,

                                key=(
                                    f"save_{fmt}_"
                                    f"{len(r.content)}"
                                ),
                            )

                        else:

                            st.error(
                                f"Export error "
                                f"{r.status_code}: "
                                f"{r.text}"
                            )

                    except requests.RequestException as exc:

                        st.error(
                            "Export connection error: "
                            f"{exc}"
                        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


st.divider()

st.caption(
    "LegalEase produces drafts for review and editing. "
    "Check applicable law and obtain professional legal "
    "advice when necessary."
)