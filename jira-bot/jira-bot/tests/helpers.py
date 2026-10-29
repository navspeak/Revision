"""Shared test helpers: settings that point at the fake copilot and acli."""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from jirabot.config import Settings  # noqa: E402

FAKES = Path(__file__).resolve().parent / "fakes"


def quote(path) -> str:
    return '"' + str(path) + '"'


def make_settings(home=None) -> Settings:
    home = Path(home) if home else Path(tempfile.mkdtemp(prefix="jirabot-test-"))
    s = Settings(home=home)
    s.copilot_command = f"{quote(sys.executable)} {quote(FAKES / 'fake_copilot.py')}"
    s.acli_command = f"{quote(sys.executable)} {quote(FAKES / 'fake_acli.py')}"
    s.jira_site = "demo.atlassian.net"
    s.jira_email = "me@example.com"
    s.copilot_timeout = 30
    s.acli_timeout = 30
    return s
