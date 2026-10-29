"""Turn conversations and documents into skills and agents (with Copilot, or without it)."""
from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from . import prompts, protocol
from .importer import Document, find_jql_candidates, looks_like_skill_file
from .llm import CopilotClient
from .proc import Cancelled, CommandError
from .session import Turn
from .store import Agent, Param, Skill, one_line, parse_skill, slugify

MAX_SKILLS_PER_DOCUMENT = 10


def skills_from_chat(
    llm: CopilotClient,
    turns: Sequence[Turn],
    last_jql: str,
    existing_names: Sequence[str],
    suggested_name: str = "",
    cancel: Optional[threading.Event] = None,
) -> List[Skill]:
    prompt = prompts.skill_from_chat_prompt(
        turns, last_jql, existing_names, slugify(suggested_name), llm.settings.max_prompt_chars
    )
    return protocol.parse_skill_drafts(llm.ask(prompt, cancel))


def agent_from_chat(
    llm: CopilotClient,
    turns: Sequence[Turn],
    skills: Sequence[Skill],
    suggested_name: str = "",
    cancel: Optional[threading.Event] = None,
) -> Optional[Agent]:
    prompt = prompts.agent_from_chat_prompt(
        turns, skills, slugify(suggested_name), llm.settings.max_prompt_chars
    )
    return protocol.parse_agent_draft(llm.ask(prompt, cancel))


def fallback_skill(jql: str, suggested_name: str = "") -> Skill:
    """A bare skill around a JQL query, used when Copilot cannot draft one."""
    return Skill(name=slugify(suggested_name) or "new-skill", jql=one_line(jql))


def skills_from_json(text: str) -> List[Skill]:
    try:
        data = json.loads(text)
    except ValueError:
        return []
    items = data if isinstance(data, list) else [data]
    skills: List[Skill] = []
    for item in items:
        if not isinstance(item, dict) or not item.get("jql"):
            continue
        params = []
        raw_params = item.get("parameters", [])
        if isinstance(raw_params, dict):
            raw_params = [{"name": k, "default": v} for k, v in raw_params.items()]
        for p in raw_params if isinstance(raw_params, list) else []:
            if isinstance(p, dict) and p.get("name"):
                params.append(Param(str(p["name"]), str(p.get("description", "")), str(p.get("default", ""))))
        skill = Skill(
            name=slugify(str(item.get("name", ""))) or "imported-skill",
            description=one_line(str(item.get("description", ""))),
            jql=one_line(str(item["jql"])),
            parameters=params,
            fields=str(item.get("fields", "")),
            output=str(item.get("output", "")),
            notes=str(item.get("notes", "")),
        )
        skill.sync_parameters()
        skills.append(skill)
    return skills[:MAX_SKILLS_PER_DOCUMENT]


def heuristic_skills(doc: Document) -> List[Skill]:
    """No-AI fallback: pick JQL-looking text out of the document."""
    stem = slugify(Path(doc.name).stem) or "imported-skill"
    first_line = next((ln.strip(" #*-\t") for ln in doc.text.splitlines() if ln.strip()), "")
    skills: List[Skill] = []
    for index, jql in enumerate(find_jql_candidates(doc.text), start=1):
        skill = Skill(
            name=stem if index == 1 else f"{stem}-{index}",
            description=first_line[:120],
            jql=jql,
            notes=f"Imported from {doc.name} using simple extraction. Review the JQL.",
        )
        skill.sync_parameters()
        skills.append(skill)
    return skills


def skills_from_document(
    llm: Optional[CopilotClient],
    doc: Document,
    existing_names: Sequence[str],
    cancel: Optional[threading.Event] = None,
) -> Tuple[List[Skill], List[str]]:
    """Returns (draft skills, notes to show the user). Raises ValueError if nothing usable is found."""
    notes: List[str] = []
    text = doc.text

    if looks_like_skill_file(text):
        try:
            return [parse_skill(text)], ["Read as a ready-made skill file."]
        except ValueError as exc:
            notes.append(f"This looks like a skill file but could not be read ({exc}).")

    if doc.name.lower().endswith(".json"):
        found = skills_from_json(text)
        if found:
            return found, ["Read from JSON."]

    if llm is not None:
        limit = max(2000, llm.settings.max_prompt_chars - 4500)
        excerpt = text[:limit]
        if len(text) > limit:
            notes.append(
                f"The document is long, so only the first {limit:,} characters were sent to Copilot."
            )
        try:
            raw = llm.ask(prompts.document_to_skills_prompt(excerpt, doc.name, list(existing_names)), cancel)
            drafts = protocol.parse_skill_drafts(raw)
            if drafts:
                return drafts[:MAX_SKILLS_PER_DOCUMENT], notes
            notes.append("Copilot's answer did not contain a usable skill, so simple extraction was used.")
        except Cancelled:
            raise
        except CommandError as exc:
            first = str(exc).strip().splitlines()[0] if str(exc).strip() else "unknown error"
            notes.append(f"Copilot could not be used ({first}). Simple extraction was used instead.")

    found = heuristic_skills(doc)
    if found:
        notes.append("Created with simple extraction. Please review the JQL and add parameters.")
        return found, notes
    raise ValueError(
        f"I could not find a JQL query in '{doc.name}'. Describe what you need in chat instead, "
        "or check that the file has JQL in it."
    )
