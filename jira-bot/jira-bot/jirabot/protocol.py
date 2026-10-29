"""Read Copilot's replies.

Copilot is asked to answer inside small XML-like tags. The parser is forgiving: it uses the
LAST <jirabot> block (in case the CLI echoes anything), ignores noise around it, and falls
back to treating the whole reply as a plain message.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .store import Agent, Param, Skill, one_line, slugify, strip_fence


def _blocks(text: str, tag: str) -> List[str]:
    return re.findall(rf"<{tag}\b[^>]*>(.*?)</{tag}>", text or "", re.S | re.I)


def _first(text: str, tag: str) -> Optional[str]:
    found = _blocks(text, tag)
    return found[0].strip() if found else None


def _clean_jql(text: Optional[str]) -> str:
    if not text:
        return ""
    jql = strip_fence(text.strip())
    jql = jql.strip("`").strip()
    jql = re.sub(r"^\s*jql\s*:\s*", "", jql, flags=re.I)
    return one_line(jql).rstrip(";").strip()


@dataclass
class Reply:
    message: str = ""
    jql: str = ""
    fields: str = ""
    skill: str = ""
    params: Dict[str, str] = field(default_factory=dict)
    structured: bool = False


def parse_reply(raw: str) -> Reply:
    raw = raw or ""
    blocks = _blocks(raw, "jirabot")
    body = blocks[-1] if blocks else raw
    reply = Reply(structured=bool(blocks))

    message = _first(body, "message")
    if message is None:
        stripped = re.sub(r"<[^>]+>.*?</[^>]+>", "", body, flags=re.S).strip()
        message = stripped if blocks else raw.strip()
    reply.message = message.strip()

    reply.jql = _clean_jql(_first(body, "jql"))
    reply.fields = one_line(_first(body, "fields") or "")
    reply.skill = slugify(_first(body, "use_skill") or "")
    for match in re.finditer(r'<param\s+name\s*=\s*"([^"]+)"\s*>(.*?)</param>', body, re.S | re.I):
        reply.params[match.group(1).strip()] = match.group(2).strip()
    return reply


def _parse_skill_block(block: str) -> Optional[Skill]:
    jql = _clean_jql(_first(block, "jql"))
    if not jql:
        return None
    name = slugify(_first(block, "name") or "") or "new-skill"
    params: List[Param] = []
    for match in re.finditer(r"<param\b([^>]*)>(.*?)</param>", block, re.S | re.I):
        attrs, desc = match.group(1), match.group(2)
        name_m = re.search(r'name\s*=\s*"([^"]+)"', attrs)
        if not name_m:
            continue
        default_m = re.search(r'default\s*=\s*"([^"]*)"', attrs)
        params.append(
            Param(name_m.group(1).strip(), one_line(desc), (default_m.group(1) if default_m else "").strip())
        )
    limit_text = (_first(block, "limit") or "").strip()
    skill = Skill(
        name=name,
        description=one_line(_first(block, "description") or ""),
        jql=jql,
        parameters=params,
        fields=one_line(_first(block, "fields") or ""),
        limit=int(limit_text) if limit_text.isdigit() else None,
        output=(_first(block, "output") or "").strip(),
        notes=(_first(block, "notes") or "").strip(),
    )
    skill.sync_parameters()
    return skill


def parse_skill_drafts(raw: str) -> List[Skill]:
    skills = []
    for block in _blocks(raw, "skill"):
        skill = _parse_skill_block(block)
        if skill:
            skills.append(skill)
    return skills


def parse_agent_draft(raw: str) -> Optional[Agent]:
    blocks = _blocks(raw, "agent")
    if not blocks:
        return None
    block = blocks[-1]
    name = slugify(_first(block, "name") or "")
    if not name:
        return None
    defaults: Dict[str, str] = {}
    for match in re.finditer(r'<default\s+name\s*=\s*"([^"]+)"\s*>(.*?)</default>', block, re.S | re.I):
        defaults[match.group(1).strip()] = one_line(match.group(2))
    skills = [slugify(s) for s in (_first(block, "skills") or "").split(",") if slugify(s)]
    return Agent(
        name=name,
        description=one_line(_first(block, "description") or ""),
        instructions=(_first(block, "instructions") or "").strip(),
        skills=skills,
        defaults=defaults,
    )
