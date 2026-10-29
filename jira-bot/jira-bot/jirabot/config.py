"""Settings: config.local.json, optionally overridden by a .env file or real environment variables.

The Jira token is never written to config.local.json."""
from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Set

from .envfile import read_env_file

CONFIG_NAME = "config.local.json"
ENV_NAME = ".env"
ENV_PREFIX = "JIRABOT_"
TOKEN_NAMES = ("JIRABOT_JIRA_API_TOKEN", "JIRA_API_TOKEN")


def default_home() -> Path:
    """Folder that holds config, skills and agents. Override with JIRABOT_HOME."""
    env = os.environ.get("JIRABOT_HOME")
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


@dataclass
class Settings:
    jira_site: str = ""
    jira_email: str = ""
    copilot_command: str = "copilot"
    copilot_model: str = ""
    copilot_extra_args: str = ""
    copilot_timeout: int = 180
    max_prompt_chars: int = 20000
    acli_command: str = "acli"
    acli_timeout: int = 120
    default_limit: int = 50
    default_fields: str = ""
    share_results: bool = True  # send result rows to Copilot for follow-ups and summaries
    home: Path = field(default_factory=default_home, repr=False, compare=False)
    env: Dict[str, str] = field(default_factory=dict, repr=False, compare=False)  # values from .env
    env_locked: Set[str] = field(default_factory=set, repr=False, compare=False)  # settings set by env
    file_values: Dict[str, object] = field(default_factory=dict, repr=False, compare=False)

    # ---- locations -------------------------------------------------------
    @property
    def config_path(self) -> Path:
        return self.home / CONFIG_NAME

    @property
    def skills_dir(self) -> Path:
        return self.home / "skills"

    @property
    def agents_dir(self) -> Path:
        return self.home / "agents"

    # ---- helpers ---------------------------------------------------------
    @property
    def site_host(self) -> str:
        """The Jira site without https:// or trailing slashes, e.g. mycompany.atlassian.net."""
        return normalize_site(self.jira_site)

    @property
    def env_path(self) -> Path:
        return self.home / ENV_NAME

    @property
    def env_token(self) -> str:
        """Jira API token from the environment or .env (kept in memory only, never saved or logged)."""
        for name in TOKEN_NAMES:
            value = os.environ.get(name) or self.env.get(name)
            if value and value.strip():
                return value.strip()
        return ""

    def to_dict(self) -> dict:
        """What gets written to config.local.json. Settings that come from .env keep their file value."""
        return {
            k: (self.file_values[k] if k in self.env_locked and k in self.file_values else getattr(self, k))
            for k in _PERSISTED
        }

    # ---- load / save -----------------------------------------------------
    @classmethod
    def load(cls, home: Optional[Path] = None) -> "Settings":
        settings = cls(home=Path(home) if home else default_home())
        path = settings.config_path
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                data = {}
            if isinstance(data, dict):
                for key in _PERSISTED:
                    if key in data:
                        _assign(settings, key, data[key])
        settings.file_values = {k: getattr(settings, k) for k in _PERSISTED}
        settings.env = read_env_file(settings.env_path)
        for key in _PERSISTED:  # real environment variables win over .env, which wins over the saved file
            name = ENV_PREFIX + key.upper()
            value = os.environ.get(name)
            if value is None:
                value = settings.env.get(name)
            if value is not None and value.strip() != "":
                _assign(settings, key, value.strip())
                settings.env_locked.add(key)
        return settings

    def save(self) -> None:
        self.home.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.to_dict(), indent=2) + "\n"
        fd, tmp = tempfile.mkstemp(dir=str(self.home), prefix=".config-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(payload)
            os.replace(tmp, self.config_path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)


_PERSISTED = [
    "jira_site",
    "jira_email",
    "copilot_command",
    "copilot_model",
    "copilot_extra_args",
    "copilot_timeout",
    "max_prompt_chars",
    "acli_command",
    "acli_timeout",
    "default_limit",
    "default_fields",
    "share_results",
]


def _assign(settings: Settings, key: str, value) -> None:
    current = getattr(settings, key)
    try:
        if isinstance(current, bool):
            setattr(settings, key, value if isinstance(value, bool) else str(value).lower() in ("1", "true", "yes"))
        elif isinstance(current, int):
            setattr(settings, key, int(value))
        else:
            setattr(settings, key, str(value))
    except (TypeError, ValueError):
        pass


def normalize_site(site: str) -> str:
    site = (site or "").strip()
    site = re.sub(r"^https?://", "", site, flags=re.I)
    return site.strip("/ ")
