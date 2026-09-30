from __future__ import annotations

import html
import re
from typing import Iterable


def sanitize_text(text: str) -> str:
    """Normalize smart punctuation and control characters for exports."""
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
        "\u00a9": "(c)",
        "\u00ae": "(R)",
        "\u2122": "(TM)",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = "".join(ch for ch in text if ch in "\n\r\t" or ord(ch) >= 32)
    return re.sub(r"[ \t]+", " ", text).strip()


def split_semicolon_terms(terms: str) -> list[str]:
    return [item.strip(" -\t") for item in terms.split(";") if item.strip()]


def document_to_plain_text(title: str, introduction: str, sections: Iterable[str], clauses: Iterable[str], closing: str) -> str:
    lines = [title.strip(), "=" * max(10, len(title.strip())), ""]
    if introduction.strip():
        lines.extend([introduction.strip(), ""])
    for section in sections:
        if "\n" in section:
            lines.extend([section.strip(), ""])
        else:
            lines.extend([section.strip(), ""])
    if clauses:
        lines.extend(["KEY TERMS", "---------"])
        lines.extend([f"- {clause.strip()}" for clause in clauses if clause.strip()])
        lines.append("")
    if closing.strip():
        lines.extend([closing.strip(), ""])
    return sanitize_text("\n".join(lines))


def markdown_to_html(text: str) -> str:
    """Convert simple markdown-ish text into safe HTML for Streamlit preview."""
    safe = html.escape(sanitize_text(text))
    safe = re.sub(r"^#{1,6}\s*(.+)$", r"<h3>\1</h3>", safe, flags=re.MULTILINE)
    safe = re.sub(r"^[-*]\s+(.+)$", r"<li>\1</li>", safe, flags=re.MULTILINE)
    safe = safe.replace("\n\n", "</p><p>").replace("\n", "<br>")
    safe = safe.replace("<li>", "<ul><li>", 1) if "<li>" in safe else safe
    if "<ul><li>" in safe:
        safe = safe.replace("</li><br>", "</li>").replace("<br><li>", "</li><li>")
        safe += "</ul>"
    return f"<div class='legal-preview'><p>{safe}</p></div>"
