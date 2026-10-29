"""Talks to Jira through the Atlassian CLI (ACLI). No REST code.

Only read-only commands are ever issued: auth status, auth login, and work item search.
"""
from __future__ import annotations

import csv
import io
import json
import re
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .config import Settings, normalize_site
from .log import log
from .proc import CommandError, RunResult, run, split_command, tail


@dataclass
class SearchResult:
    jql: str
    columns: List[str] = field(default_factory=list)
    rows: List[Dict[str, str]] = field(default_factory=list)
    raw: str = ""


def clean_jql(jql: str) -> str:
    """One line, no trailing semicolon. Raises ValueError if empty or absurdly long."""
    text = (jql or "").strip().strip("`").strip()
    text = re.sub(r"\s+", " ", text).rstrip(";").strip()
    if not text:
        raise ValueError("The JQL is empty.")
    if len(text) > 4000:
        raise ValueError("The JQL is too long (over 4000 characters).")
    return text


# ----------------------------------------------------------- output parsing


def _adf_text(node) -> str:
    if isinstance(node, dict):
        if node.get("type") == "text":
            return str(node.get("text", ""))
        return " ".join(t for t in (_adf_text(c) for c in node.get("content", []) or []) if t)
    if isinstance(node, list):
        return " ".join(t for t in (_adf_text(c) for c in node) if t)
    return ""


def display_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, float, str)):
        return str(value)
    if isinstance(value, list):
        return ", ".join(v for v in (display_value(x) for x in value) if v)
    if isinstance(value, dict):
        if value.get("type") == "doc" or "content" in value:
            text = _adf_text(value)
            if text:
                return text
        for key in ("displayName", "name", "value", "key", "emailAddress", "title"):
            if value.get(key):
                return str(value[key])
        return json.dumps(value, ensure_ascii=False)[:200]
    return str(value)


def _items_from_json(data) -> list:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("issues", "workitems", "workItems", "values", "results", "items"):
            if isinstance(data.get(key), list):
                return data[key]
        if "key" in data:
            return [data]
    return []


def parse_search_output(text: str, requested_fields: str = "") -> Tuple[List[str], List[Dict[str, str]]]:
    """Turn ACLI output into (columns, rows). Accepts JSON (preferred) or CSV."""
    text = (text or "").strip()
    if not text:
        return [], []

    rows: List[Dict[str, str]] = []
    if text[0] in "[{":
        try:
            data = json.loads(text)
        except ValueError:
            data = None
        if data is not None:
            for item in _items_from_json(data):
                if not isinstance(item, dict):
                    continue
                fields = item.get("fields")
                if isinstance(fields, dict):
                    row = {"key": display_value(item.get("key", ""))}
                    for name, value in fields.items():
                        row[name] = display_value(value)
                else:
                    row = {name: display_value(value) for name, value in item.items()}
                rows.append(row)
    elif "," in text.splitlines()[0]:
        try:
            reader = csv.DictReader(io.StringIO(text))
            rows = [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in reader]
        except csv.Error:
            rows = []

    columns: List[str] = []
    for row in rows:
        for name in row:
            if name not in columns:
                columns.append(name)
    wanted = [f.strip() for f in requested_fields.split(",") if f.strip()]
    ordered = [c for w in wanted for c in columns if c.lower() == w.lower()]
    ordered += [c for c in columns if c not in ordered]
    if "key" in ordered:
        ordered.remove("key")
        ordered.insert(0, "key")
    return ordered, rows


# ------------------------------------------------------------------ client


class AcliClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _argv(self, *args: str) -> list:
        return split_command(self.settings.acli_command) + list(args)

    def auth_status(self, cancel: Optional[threading.Event] = None) -> RunResult:
        return run(self._argv("jira", "auth", "status"), timeout=self.settings.acli_timeout, cancel=cancel)

    def login(self, site: str, email: str, token: str, cancel: Optional[threading.Event] = None) -> RunResult:
        """Log ACLI in. The token goes to ACLI on stdin and is not stored or logged by this app."""
        site = normalize_site(site)
        if not site or not email.strip() or not token.strip():
            raise ValueError("Site, email and API token are all required.")
        argv = self._argv("jira", "auth", "login", "--site", site, "--email", email.strip(), "--token")
        return run(argv, input_text=token.strip() + "\n", timeout=self.settings.acli_timeout, cancel=cancel)

    def search(
        self,
        jql: str,
        fields: str = "",
        limit: Optional[int] = None,
        cancel: Optional[threading.Event] = None,
        paginate: bool = False,
    ) -> SearchResult:
        """Run a JQL search. paginate=True asks ACLI for every page instead of stopping at limit."""
        jql = clean_jql(jql)
        fields = (fields or self.settings.default_fields or "").strip()
        limit = int(limit or self.settings.default_limit or 50)
        state = {"fmt": "--json", "paginate": bool(paginate)}

        def attempt() -> RunResult:
            argv = self._argv("jira", "workitem", "search", "--jql", jql, state["fmt"])
            argv += ["--paginate"] if state["paginate"] else ["--limit", str(limit)]
            if fields:
                argv += ["--fields", re.sub(r"\s+", "", fields)]
            return run(argv, timeout=self.settings.acli_timeout, cancel=cancel)

        result = attempt()
        for _ in range(2):  # at most two compatibility retries
            if result.returncode == 0:
                break
            text = (result.stderr or "") + (result.stdout or "")
            if state["paginate"] and re.search(r"unknown (shorthand )?flag[^\n]*paginate", text, re.I):
                log.info("acli did not accept --paginate; retrying with --limit")
                state["paginate"] = False
            elif state["fmt"] == "--json" and re.search(
                r"unknown (shorthand )?flag[^\n]*json|json[^\n]*(unknown|not supported)", text, re.I
            ):
                log.info("acli did not accept --json; retrying with --csv")
                state["fmt"] = "--csv"
            else:
                break
            result = attempt()
        log.info("acli search: rc=%s %.1fs stdout=%d chars", result.returncode, result.seconds, len(result.stdout))
        if result.returncode != 0:
            detail = tail(result.stderr or result.stdout)
            raise CommandError(f"ACLI exited with code {result.returncode}.\n{detail}")
        columns, rows = parse_search_output(result.stdout, fields)
        return SearchResult(jql=jql, columns=columns, rows=rows, raw=result.stdout)
