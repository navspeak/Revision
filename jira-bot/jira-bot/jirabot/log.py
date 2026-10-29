"""Small file logger. Prompts and replies are only logged when JIRABOT_DEBUG=1."""
from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

log = logging.getLogger("jirabot")
_configured = False


def debug_enabled() -> bool:
    return os.environ.get("JIRABOT_DEBUG", "") == "1"


def setup_logging(home: Path) -> None:
    """Write jirabot.log next to the app (git-ignored). Safe to call more than once."""
    global _configured
    if _configured:
        return
    _configured = True
    log.setLevel(logging.DEBUG if debug_enabled() else logging.INFO)
    try:
        handler = RotatingFileHandler(
            Path(home) / "jirabot.log", maxBytes=500_000, backupCount=2, encoding="utf-8"
        )
    except OSError:
        return
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(handler)
