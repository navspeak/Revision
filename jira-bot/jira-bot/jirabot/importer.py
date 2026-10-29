"""Read a skill document from disk (uploaded through the file picker or typed as a path).

Supported: .md .markdown .txt .jql .json .yaml .yml .csv .docx (Word).
"""
from __future__ import annotations

import os
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import List
from xml.etree import ElementTree as ET

from .store import FRONTMATTER_RE, one_line, slugify

TEXT_EXTS = {".md", ".markdown", ".txt", ".text", ".jql", ".json", ".yaml", ".yml", ".csv"}
SUPPORTED_EXTS = TEXT_EXTS | {".docx"}
MAX_FILE_BYTES = 5_000_000
MAX_DOCX_XML_BYTES = 20_000_000

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


class ImportProblem(Exception):
    """A document could not be read. The message is safe to show to the user."""


@dataclass
class Document:
    name: str
    path: str
    text: str


# ------------------------------------------------------------------- paths


def normalize_path(raw: str) -> Path:
    """Accept pasted paths, including the quoted form that Windows 'Copy as path' produces."""
    text = (raw or "").strip().strip("\"'").strip()
    if text.lower().startswith("file:///"):
        text = text[8:] if re.match(r"file:///[A-Za-z]:", text) else text[7:]
    return Path(os.path.expandvars(os.path.expanduser(text)))


def parse_path_list(raw: str) -> List[str]:
    """Split a box full of paths: quoted paths, or paths separated by ; or new lines."""
    raw = (raw or "").strip()
    if not raw:
        return []
    quoted = re.findall(r'"([^"]+)"', raw)
    if quoted:
        return [q.strip() for q in quoted if q.strip()]
    return [p.strip() for p in re.split(r"[;\n]", raw) if p.strip()]


# ----------------------------------------------------------------- reading


def _decode(data: bytes) -> str:
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1", errors="replace")


def _docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as zf:
            try:
                info = zf.getinfo("word/document.xml")
            except KeyError:
                raise ImportProblem(f"'{path.name}' does not look like a Word (.docx) document.")
            if info.file_size > MAX_DOCX_XML_BYTES:
                raise ImportProblem(f"'{path.name}' is too large to read.")
            xml = zf.read(info)
    except zipfile.BadZipFile:
        raise ImportProblem(f"'{path.name}' is not a valid .docx file.")
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        raise ImportProblem(f"Could not read the text inside '{path.name}'.")

    lines: List[str] = []
    for para in root.iter(f"{W_NS}p"):
        parts: List[str] = []
        for node in para.iter():
            if node.tag == f"{W_NS}t":
                parts.append(node.text or "")
            elif node.tag == f"{W_NS}tab":
                parts.append("\t")
            elif node.tag in (f"{W_NS}br", f"{W_NS}cr"):
                parts.append("\n")
        lines.append("".join(parts))
    return "\n".join(lines).strip()


def read_document(raw_path: str) -> Document:
    path = normalize_path(raw_path)
    if not str(path).strip():
        raise ImportProblem("Enter the path to a file.")
    if not path.exists():
        raise ImportProblem(f"I cannot find '{path}'. Check the path and try again.")
    if path.is_dir():
        raise ImportProblem(f"'{path}' is a folder. Pick one or more files inside it.")
    ext = path.suffix.lower()
    if ext == ".pdf":
        raise ImportProblem(
            f"'{path.name}' is a PDF, which is not supported. Save it as .docx or .txt, "
            "or paste its text into the paste box."
        )
    if ext == ".doc":
        raise ImportProblem(f"'{path.name}' is an old .doc file. Open it in Word and save it as .docx.")
    if ext not in SUPPORTED_EXTS:
        raise ImportProblem(
            f"'{path.name}' has an unsupported type ({ext or 'no extension'}). "
            f"Supported: {', '.join(sorted(SUPPORTED_EXTS))}."
        )
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise ImportProblem(f"Cannot read '{path.name}': {exc}")
    if size > MAX_FILE_BYTES:
        raise ImportProblem(f"'{path.name}' is larger than {MAX_FILE_BYTES // 1_000_000} MB.")

    if ext == ".docx":
        text = _docx_text(path)
    else:
        try:
            text = _decode(path.read_bytes())
        except OSError as exc:
            raise ImportProblem(f"Cannot read '{path.name}': {exc}")
    text = text.replace("\x00", "").strip()
    if not text:
        raise ImportProblem(f"'{path.name}' is empty.")
    return Document(name=path.name, path=str(path), text=text)


def document_from_text(text: str, name: str = "pasted-text") -> Document:
    text = (text or "").replace("\x00", "").strip()
    if not text:
        raise ImportProblem("There is no text to import.")
    return Document(name=name, path="", text=text)


# --------------------------------------------------------- format sniffing


def looks_like_skill_file(text: str) -> bool:
    match = FRONTMATTER_RE.match(text or "")
    if not match:
        return False
    header = match.group(1)
    return bool(re.search(r"^name\s*:", header, re.M | re.I)) and bool(
        re.search(r"^##\s+jql\b", match.group(2), re.M | re.I)
    )


_JQL_HINT = re.compile(
    r"\b(project|assignee|reporter|status|statusCategory|issuetype|type|priority|sprint|created|"
    r"updated|resolution|labels?|fixVersion|component|text|summary|parent|epic)\b\s*"
    r"(=|!=|~|!~|>=|<=|>|<|\bin\b|\bnot in\b|\bis\b|\bwas\b)",
    re.I,
)


def find_jql_candidates(text: str) -> List[str]:
    found: List[str] = []

    def add(candidate: str) -> None:
        candidate = one_line(candidate).strip("`").strip()
        if len(candidate) >= 8 and _JQL_HINT.search(candidate) and candidate not in found:
            found.append(candidate)

    for match in re.finditer(r"```[a-zA-Z]*\r?\n(.*?)```", text, re.S):
        add(match.group(1))
    for match in re.finditer(r"(?im)^\s*[-*]?\s*jql\s*[:=]\s*(.+)$", text):
        add(match.group(1))
    for match in re.finditer(r"`([^`\n]{12,400})`", text):
        inner = match.group(1)
        if re.search(r"\b(AND|OR|ORDER BY)\b|=|~", inner):
            add(inner)
    return found[:5]


def read_upload(name: str, data: bytes) -> Document:
    """Read a file the user uploaded in the browser (same rules as a file on disk)."""
    import tempfile

    safe = re.sub(r"[^\w.\- ]", "_", os.path.basename(name or "")) or "upload.txt"
    if len(data) > MAX_FILE_BYTES:
        raise ImportProblem(f"'{safe}' is larger than {MAX_FILE_BYTES // 1_000_000} MB.")
    with tempfile.TemporaryDirectory(prefix="jirabot-upload-") as tmp:
        target = Path(tmp) / safe
        target.write_bytes(data)
        doc = read_document(str(target))
    return Document(name=safe, path="", text=doc.text)
