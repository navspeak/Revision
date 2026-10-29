"""Skills and agents saved as plain Markdown files.

A skill file looks like this:

    ---
    name: bug-triage-weekly
    description: Open bugs for a project, newest first
    fields: key,summary,status,priority,assignee
    limit: 50
    parameters:
      - project | Jira project key | ABC
      - days | Look-back window in days | 7
    ---

    ## JQL

    project = {project} AND issuetype = Bug AND created >= -{days}d ORDER BY created DESC

    ## Output

    Group by priority and call out unassigned bugs.

    ## Notes

    Anything worth remembering.
"""
from __future__ import annotations

import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")
FRONTMATTER_RE = re.compile(r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)(.*)\Z", re.S)


# ---------------------------------------------------------------- helpers


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return slug[:64].strip("-")


def valid_name(name: str) -> bool:
    return bool(NAME_RE.match(name or ""))


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def strip_fence(text: str) -> str:
    text = (text or "").strip()
    match = re.match(r"^```[a-zA-Z]*\s*\n(.*?)\n?```\s*$", text, re.S)
    return match.group(1).strip() if match else text


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=".md")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _parse_frontmatter(block: str) -> Dict[str, object]:
    data: Dict[str, object] = {}
    current: Optional[str] = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        if raw[0] in " \t" or stripped.startswith("- "):
            if current is None:
                continue
            item = stripped[1:].strip() if stripped.startswith("-") else stripped
            data[current].append(item)  # type: ignore[union-attr]
            continue
        if ":" not in raw:
            raise ValueError(f"Cannot read this header line: {raw!r}")
        key, _, value = raw.partition(":")
        key = key.strip().lower()
        value = value.strip()
        if value == "":
            data[key] = []
            current = key
        else:
            data[key] = _unquote(value)
            current = None
    return data


def _as_text(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value or "")


def _parse_sections(body: str) -> Dict[str, str]:
    sections: Dict[str, str] = {}
    current: Optional[str] = None
    buf: List[str] = []

    def flush() -> None:
        if current is not None:
            sections[current] = "\n".join(buf).strip()

    for line in body.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            flush()
            current = match.group(1).strip().lower()
            buf = []
        elif current is not None:
            buf.append(line)
    flush()
    return sections


def _split_document(text: str) -> Tuple[Dict[str, object], Dict[str, str]]:
    match = FRONTMATTER_RE.match(text or "")
    if not match:
        raise ValueError("The file must start with a header between two lines of ---.")
    return _parse_frontmatter(match.group(1)), _parse_sections(match.group(2))


# ----------------------------------------------------------------- skills


@dataclass
class Param:
    name: str
    description: str = ""
    default: str = ""

    def to_line(self) -> str:
        return " | ".join(
            [self.name, one_line(self.description).replace("|", "/"), one_line(self.default)]
        )


def parse_param_line(line: str) -> Optional[Param]:
    line = (line or "").strip()
    if not line:
        return None
    parts = [p.strip() for p in line.split("|", 2)]
    name = parts[0]
    if not re.fullmatch(r"\w+", name):
        raise ValueError(
            f"'{name}' is not a valid parameter name. Use letters, digits and underscores."
        )
    return Param(name, parts[1] if len(parts) > 1 else "", parts[2] if len(parts) > 2 else "")


@dataclass
class Skill:
    name: str
    description: str = ""
    jql: str = ""
    parameters: List[Param] = field(default_factory=list)
    fields: str = ""
    limit: Optional[int] = None
    output: str = ""
    notes: str = ""
    path: Optional[Path] = field(default=None, repr=False, compare=False)

    def placeholders(self) -> List[str]:
        seen: List[str] = []
        for name in PLACEHOLDER_RE.findall(self.jql or ""):
            if name not in seen:
                seen.append(name)
        return seen

    def sync_parameters(self) -> None:
        """Declare every {placeholder} used in the JQL."""
        known = {p.name for p in self.parameters}
        for name in self.placeholders():
            if name not in known:
                self.parameters.append(Param(name))

    def render(self, values: Optional[Dict[str, str]] = None) -> Tuple[str, List[str]]:
        """Fill placeholders. Returns (jql, names of parameters that still have no value)."""
        values = values or {}
        defaults = {p.name: p.default for p in self.parameters}
        missing: List[str] = []

        def repl(match: "re.Match[str]") -> str:
            name = match.group(1)
            value = values.get(name)
            if value is None or str(value).strip() == "":
                value = defaults.get(name, "")
            value = one_line(str(value))
            if value == "":
                if name not in missing:
                    missing.append(name)
                return match.group(0)
            return value

        return PLACEHOLDER_RE.sub(repl, self.jql or ""), missing


def dump_skill(skill: Skill) -> str:
    lines = ["---", f"name: {skill.name}", f"description: {one_line(skill.description)}"]
    if skill.fields.strip():
        lines.append(f"fields: {one_line(skill.fields)}")
    if skill.limit:
        lines.append(f"limit: {int(skill.limit)}")
    if skill.parameters:
        lines.append("parameters:")
        lines.extend(f"  - {p.to_line()}" for p in skill.parameters)
    lines.append("---")
    out = ["\n".join(lines), "", "## JQL", "", one_line(skill.jql)]
    if skill.output.strip():
        out += ["", "## Output", "", skill.output.strip()]
    if skill.notes.strip():
        out += ["", "## Notes", "", skill.notes.strip()]
    return "\n".join(out) + "\n"


def parse_skill(text: str, fallback_name: str = "") -> Skill:
    header, sections = _split_document(text)
    name = _as_text(header.get("name")).strip() or fallback_name
    if not valid_name(name):
        raise ValueError(
            f"Skill name '{name}' is not valid. Use lowercase letters, digits, - and _ (max 64)."
        )
    jql = one_line(strip_fence(sections.get("jql", "")))
    if not jql:
        raise ValueError("The skill has no '## JQL' section.")
    params: List[Param] = []
    raw_params = header.get("parameters", [])
    if isinstance(raw_params, list):
        for line in raw_params:
            param = parse_param_line(line)
            if param:
                params.append(param)
    limit_text = _as_text(header.get("limit")).strip()
    limit = int(limit_text) if limit_text.isdigit() else None
    skill = Skill(
        name=name,
        description=_as_text(header.get("description")).strip(),
        jql=jql,
        parameters=params,
        fields=_as_text(header.get("fields")).strip(),
        limit=limit,
        output=sections.get("output", ""),
        notes=sections.get("notes", ""),
    )
    skill.sync_parameters()
    return skill


# ----------------------------------------------------------------- agents


@dataclass
class Agent:
    name: str
    description: str = ""
    instructions: str = ""
    skills: List[str] = field(default_factory=list)
    defaults: Dict[str, str] = field(default_factory=dict)
    path: Optional[Path] = field(default=None, repr=False, compare=False)


def dump_agent(agent: Agent) -> str:
    lines = ["---", f"name: {agent.name}", f"description: {one_line(agent.description)}"]
    if agent.skills:
        lines.append(f"skills: {', '.join(agent.skills)}")
    if agent.defaults:
        lines.append("defaults:")
        lines.extend(f"  - {k} | {one_line(v)}" for k, v in agent.defaults.items())
    lines.append("---")
    out = ["\n".join(lines), "", "## Instructions", "", agent.instructions.strip()]
    return "\n".join(out) + "\n"


def parse_agent(text: str, fallback_name: str = "") -> Agent:
    header, sections = _split_document(text)
    name = _as_text(header.get("name")).strip() or fallback_name
    if not valid_name(name):
        raise ValueError(
            f"Agent name '{name}' is not valid. Use lowercase letters, digits, - and _ (max 64)."
        )
    skills = [s.strip() for s in _as_text(header.get("skills")).split(",") if s.strip()]
    defaults: Dict[str, str] = {}
    raw_defaults = header.get("defaults", [])
    if isinstance(raw_defaults, list):
        for line in raw_defaults:
            key, _, value = line.partition("|")
            key = key.strip()
            if key:
                defaults[key] = value.strip()
    return Agent(
        name=name,
        description=_as_text(header.get("description")).strip(),
        instructions=sections.get("instructions", ""),
        skills=skills,
        defaults=defaults,
    )


# ----------------------------------------------------------------- stores


class _Store:
    kind = "item"

    def __init__(self, directory: Path):
        self.dir = Path(directory)
        self.errors: List[Tuple[str, str]] = []

    # subclasses
    def _parse(self, text: str, fallback: str):
        raise NotImplementedError

    def _dump(self, item) -> str:
        raise NotImplementedError

    # shared
    def _path(self, name: str) -> Path:
        if not valid_name(name):
            raise ValueError(
                f"'{name}' is not a valid name. Use lowercase letters, digits, - and _ (max 64)."
            )
        base = self.dir.resolve()
        path = (base / f"{name}.md").resolve()
        if path.parent != base:
            raise ValueError("Invalid name.")
        return path

    def list(self) -> list:
        self.errors = []
        items = []
        if not self.dir.exists():
            return items
        seen = set()
        for path in sorted(self.dir.glob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            try:
                item = self._parse(path.read_text(encoding="utf-8-sig"), path.stem)
            except (OSError, ValueError) as exc:
                self.errors.append((path.name, str(exc)))
                continue
            if item.name in seen:
                self.errors.append((path.name, f"Duplicate name '{item.name}' (ignored)."))
                continue
            seen.add(item.name)
            item.path = path
            items.append(item)
        return items

    def names(self) -> List[str]:
        return [i.name for i in self.list()]

    def get(self, name: str):
        for item in self.list():
            if item.name == name:
                return item
        return None

    def exists(self, name: str) -> bool:
        return self.get(name) is not None

    def save(self, item, overwrite: bool = False) -> Path:
        path = self._path(item.name)
        if path.exists() and not overwrite:
            raise FileExistsError(f"A {self.kind} named '{item.name}' already exists.")
        _atomic_write(path, self._dump(item))
        item.path = path
        return path

    def delete(self, name: str) -> bool:
        item = self.get(name)
        if item is None or item.path is None:
            return False
        item.path.unlink()
        return True


class SkillStore(_Store):
    kind = "skill"

    def _parse(self, text: str, fallback: str) -> Skill:
        return parse_skill(text, fallback)

    def _dump(self, item: Skill) -> str:
        if not one_line(item.jql):
            raise ValueError("A skill needs a JQL query.")
        item.sync_parameters()
        return dump_skill(item)


class AgentStore(_Store):
    kind = "agent"

    def _parse(self, text: str, fallback: str) -> Agent:
        return parse_agent(text, fallback)

    def _dump(self, item: Agent) -> str:
        return dump_agent(item)
