"""Shared objects for the web app, created once per server process."""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from typing import List

import streamlit as st

from ..config import Settings
from ..jira import AcliClient
from ..llm import CopilotClient
from ..proc import split_command
from ..reviews import ReviewStore
from ..store import AgentStore, SkillStore


@dataclass
class Ctx:
    settings: Settings
    skills: SkillStore
    agents: AgentStore
    acli: AcliClient
    llm: CopilotClient
    reviews: ReviewStore


@st.cache_resource(show_spinner=False)
def context() -> Ctx:
    settings = Settings.load()
    return Ctx(
        settings=settings,
        skills=SkillStore(settings.skills_dir),
        agents=AgentStore(settings.agents_dir),
        acli=AcliClient(settings),
        llm=CopilotClient(settings),
        reviews=ReviewStore(settings.home / "data" / "reviews.sqlite3"),
    )


def setup_warnings(settings: Settings) -> List[str]:
    out: List[str] = []
    for label, command in (("Copilot CLI", settings.copilot_command), ("Atlassian CLI (acli)", settings.acli_command)):
        try:
            parts = split_command(command)
            found = bool(parts) and shutil.which(parts[0]) is not None
        except Exception:  # noqa: BLE001
            found = False
        if not found:
            out.append(f"{label} was not found. Open Settings to set its location.")
    if not settings.jira_site:
        out.append("Jira is not set up yet. Open Settings, enter your site and email, and log in.")
    return out


def default_review_name(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip().strip(".?!")
    return (text[:50].rstrip() or "My review")
