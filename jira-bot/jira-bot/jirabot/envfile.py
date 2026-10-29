"""Read a .env file (KEY=VALUE lines). No third-party package needed."""
from __future__ import annotations

from pathlib import Path
from typing import Dict


def parse_env(text: str) -> Dict[str, str]:
    """Supports comments, blank lines, `export KEY=value`, and single or double quotes."""
    values: Dict[str, str] = {}
    for raw in (text or "").lstrip("﻿").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not key or not key.replace("_", "").isalnum():
            continue
        if value[:1] in ("'", '"'):
            quote = value[0]
            end = value.find(quote, 1)
            value = value[1:end] if end != -1 else value[1:]
        else:
            hash_at = value.find(" #")  # trailing comment
            if hash_at != -1:
                value = value[:hash_at].rstrip()
        values[key] = value
    return values


def read_env_file(path: Path) -> Dict[str, str]:
    try:
        return parse_env(Path(path).read_text(encoding="utf-8"))
    except OSError:
        return {}
