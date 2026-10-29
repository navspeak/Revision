"""Agents page: a named set of instructions, skills and default parameter values."""
from __future__ import annotations

from typing import Dict, Optional

import streamlit as st

from ..store import Agent, slugify
from . import services

DRAFT = "agent_draft"


def parse_defaults(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip().lstrip("-").strip()
        if not line:
            continue
        if "=" in line:
            k, v = line.split("=", 1)
        elif "|" in line:
            k, v = line.split("|", 1)
        else:
            raise ValueError(f"Defaults need the form name = value (got '{line}').")
        k = k.strip()
        if not k.replace("_", "").isalnum():
            raise ValueError(f"'{k}' is not a valid parameter name.")
        out[k] = v.strip()
    return out


def agent_form(agent: Agent, key: str, title: str, editing: bool = False, note: str = "") -> Optional[str]:
    ctx = services.context()
    st.subheader(title)
    if note:
        st.caption(note)
    skill_names = ctx.skills.names()
    with st.form(key):
        name = st.text_input("Name", agent.name)
        description = st.text_input("What it is for", agent.description)
        instructions = st.text_area("Instructions (how it should behave)", agent.instructions, height=140)
        chosen = st.multiselect("Skills it uses", skill_names, default=[s for s in agent.skills if s in skill_names])
        defaults = st.text_area(
            "Default values for parameters (name = value, one per line)",
            "\n".join(f"{k} = {v}" for k, v in agent.defaults.items()), height=80,
        )
        replace = st.checkbox("Replace an existing agent with this name", value=editing)
        save = st.form_submit_button("Save agent", type="primary")
    if not save:
        return None
    try:
        item = Agent(name=slugify(name), description=description.strip(), instructions=instructions.strip(),
                     skills=chosen, defaults=parse_defaults(defaults))
        ctx.agents.save(item, overwrite=replace)
    except FileExistsError as exc:
        st.error(f"{exc} Tick 'Replace an existing agent' to overwrite it.")
        return None
    except ValueError as exc:
        st.error(str(exc))
        return None
    st.toast(f"Saved agent '{item.name}'.")
    return "saved"


def page() -> None:
    ctx = services.context()
    st.title("Agents")
    st.caption("An agent bundles instructions, skills and default values (like your project key) so you can pick it in Ask.")
    draft = st.session_state.get(DRAFT)
    if draft is not None:
        if agent_form(draft, "agent_draft_form", "Save as agent", note="Drafted from your chat. Check it, then save."):
            st.session_state.pop(DRAFT)
            st.rerun()
        if st.button("Discard draft"):
            st.session_state.pop(DRAFT)
            st.rerun()
        st.divider()
    editing = st.session_state.get("edit_agent")
    agents = ctx.agents.list()
    for n, why in ctx.agents.errors:
        st.warning(f"Could not read {n}: {why}")
    if not agents and draft is None:
        st.info("No agents yet. Chat for a while in Ask, then use 'Save as agent' there, or create one below.")
    for agent in agents:
        if editing == agent.name:
            if agent_form(agent, f"ea_{agent.name}", f"Edit agent: {agent.name}", editing=True):
                st.session_state.pop("edit_agent")
                st.rerun()
            if st.button("Cancel", key=f"ca_{agent.name}"):
                st.session_state.pop("edit_agent")
                st.rerun()
            continue
        with st.expander(f"**{agent.name}**  {('- ' + agent.description) if agent.description else ''}"):
            if agent.instructions:
                st.write(agent.instructions)
            if agent.skills:
                st.caption("Skills: " + ", ".join(agent.skills))
            if agent.defaults:
                st.caption("Defaults: " + ", ".join(f"{k}={v}" for k, v in agent.defaults.items()))
            c1, c2, _ = st.columns([1, 1, 6])
            if c1.button("Edit", key=f"ea_btn_{agent.name}"):
                st.session_state["edit_agent"] = agent.name
                st.rerun()
            if c2.button("Delete", key=f"da_{agent.name}"):
                st.session_state["confirm_delete_agent"] = agent.name
                st.rerun()
            if st.session_state.get("confirm_delete_agent") == agent.name:
                st.warning(f"Delete '{agent.name}'?")
                if st.button("Yes, delete it", key=f"yda_{agent.name}"):
                    ctx.agents.delete(agent.name)
                    st.session_state.pop("confirm_delete_agent")
                    st.rerun()
    with st.expander("Create an agent from scratch"):
        if agent_form(Agent(name=""), "new_agent", "New agent"):
            st.rerun()
