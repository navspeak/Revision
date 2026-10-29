"""Ask page: chat in plain English, check the JQL, run it, open the issues in the Review grid."""
from __future__ import annotations

import re
from typing import Dict, List, Optional

import streamlit as st

from .. import jira, prompts, protocol, skillgen
from ..proc import CommandError
from ..session import ChatSession
from ..store import Agent, Skill
from . import services, skills as skills_page
from .agents import DRAFT as AGENT_DRAFT

SAVE_SKILL_RE = re.compile(
    r"^\s*(?:please\s+)?save\s+(?:this|that|it)?\s*(?:as\s+)?(?:a\s+)?skill(?:\s+(?:called|named))?\s*[:\-]?\s*(?P<name>.*)$",
    re.I,
)


def _state() -> None:
    ss = st.session_state
    ss.setdefault("chat", ChatSession())
    ss.setdefault("msgs", [])
    ss.setdefault("proposal", None)
    ss.setdefault("result", None)
    ss.setdefault("pid", 0)


def say(kind: str, text: str) -> None:
    st.session_state["msgs"].append({"kind": kind, "text": text})


def new_chat() -> None:
    st.session_state["chat"].reset()
    st.session_state["msgs"] = []
    st.session_state["proposal"] = None
    st.session_state["result"] = None
    st.session_state.pop("skill_run", None)


def current_agent(ctx) -> Optional[Agent]:
    name = st.session_state.get("agent_name")
    return ctx.agents.get(name) if name and name != "(no agent)" else None


def available_skills(ctx) -> List[Skill]:
    agent = current_agent(ctx)
    skills = ctx.skills.list()
    if agent and agent.skills:
        subset = [s for s in skills if s.name in agent.skills]
        return subset or skills
    return skills


def propose(jql: str, fields: str = "", limit: Optional[int] = None, skill: str = "") -> None:
    st.session_state["pid"] += 1
    st.session_state["proposal"] = {"jql": jql, "fields": fields, "limit": limit, "skill": skill}
    st.session_state["result"] = None


def ask_model(ctx) -> None:
    chat: ChatSession = st.session_state["chat"]
    prompt = prompts.chat_prompt(chat.turns, available_skills(ctx), current_agent(ctx), ctx.settings.max_prompt_chars)
    try:
        with st.spinner("Asking Copilot..."):
            raw = ctx.llm.ask(prompt)
    except CommandError as exc:
        message = str(exc)
        hint = _hint(message)
        say("error", "That did not work.\n" + message + (f"\n\n{hint}" if hint else ""))
        return
    reply = protocol.parse_reply(raw)
    message = reply.message or "(Copilot sent no message.)"
    chat.add_assistant(message + (f"\nJQL: {reply.jql}" if reply.jql else ""))
    say("bot", message)
    skill = next((s for s in available_skills(ctx) if s.name == reply.skill), None) if reply.skill else None
    if skill is not None:
        agent = current_agent(ctx)
        values = dict(agent.defaults) if agent else {}
        values.update(reply.params)
        jql, missing = skill.render(values)
        if missing:
            say("note", f"The skill '{skill.name}' still needs: {', '.join(missing)}.")
            st.session_state["skill_run"] = {"name": skill.name, "presets": values}
            return
        propose(jql, skill.fields or reply.fields, skill.limit, skill.name)
    elif reply.jql:
        propose(reply.jql, reply.fields)
    elif not reply.structured:
        say("note", "Copilot did not use the expected format, so its reply is shown as plain text.")


def _hint(message: str) -> str:
    low = message.lower()
    if "could not find" in low or "could not start" in low:
        return "Open Settings and check the command path, then use the Test button."
    if any(w in low for w in ("auth", "login", "unauthorized", "401", "403", "credentials", "not logged")):
        return "This looks like a sign-in problem. Open Settings and log in to Jira."
    if "unbounded" in low:
        return "Jira rejected the query because it has no restriction. Add a project, date range or assignee."
    if "longer than" in low:
        return "The command timed out. You can raise the timeout in Settings."
    return ""


def on_user_text(ctx, text: str) -> None:
    chat: ChatSession = st.session_state["chat"]
    say("user", text)
    match = SAVE_SKILL_RE.match(text)
    if match:
        draft_skill(ctx, match.group("name").strip())
        return
    chat.add_user(text)
    st.session_state["proposal"] = None
    ask_model(ctx)


def draft_skill(ctx, suggested: str = "") -> None:
    chat: ChatSession = st.session_state["chat"]
    if not chat.has_user_turn() and not chat.last_jql:
        say("note", "Have a short conversation first, then save what worked.")
        return
    note = "Drafted from your conversation. Check the JQL and parameters, then save."
    try:
        with st.spinner("Drafting a skill from this conversation..."):
            drafts = skillgen.skills_from_chat(ctx.llm, chat.turns, chat.last_jql, ctx.skills.names(), suggested)
    except CommandError as exc:
        drafts = []
        first = (str(exc).strip().splitlines() or ["unknown error"])[0]
        note = f"Copilot could not draft this ({first}), so this is a plain starting point from the last query."
    if not drafts and chat.last_jql:
        drafts = [skillgen.fallback_skill(chat.last_jql, suggested)]
        if "plain starting point" not in note:
            note = "Copilot did not return a skill, so this is a plain starting point from the last query."
    if not drafts:
        say("error", "I could not draft a skill. Run a query first, then try again.")
        return
    skills_page.queue_drafts(drafts, note)
    say("note", "A skill draft is ready. Scroll to the top of the page to check and save it.")


def draft_agent(ctx, suggested: str = "") -> None:
    chat: ChatSession = st.session_state["chat"]
    if not chat.has_user_turn():
        say("note", "Have a short conversation first, then save an agent.")
        return
    try:
        with st.spinner("Drafting an agent..."):
            agent = skillgen.agent_from_chat(ctx.llm, chat.turns, ctx.skills.list(), suggested)
    except CommandError as exc:
        say("error", str(exc))
        return
    st.session_state[AGENT_DRAFT] = agent or Agent(name=suggested or "new-agent")
    pages = st.session_state.get("_pages", {})
    if "agents" in pages:
        st.switch_page(pages["agents"])


# ------------------------------------------------------------------ panels


def skill_run_panel(ctx) -> None:
    run = st.session_state.get("skill_run")
    if not run:
        return
    skill = ctx.skills.get(run["name"])
    if skill is None:
        st.session_state.pop("skill_run")
        return
    agent = current_agent(ctx)
    values = dict(agent.defaults) if agent else {}
    values.update(run.get("presets") or {})
    with st.form(f"run_{skill.name}"):
        st.markdown(f"**Run skill: {skill.name}**")
        entered: Dict[str, str] = {}
        for p in skill.parameters:
            entered[p.name] = st.text_input(f"{p.name}" + (f"  ({p.description})" if p.description else ""),
                                            values.get(p.name, p.default))
        go = st.form_submit_button("Prepare query", type="primary")
    if go:
        jql, missing = skill.render(entered)
        if missing:
            st.error("Still needed: " + ", ".join(missing))
            return
        chat: ChatSession = st.session_state["chat"]
        say("user", f"Run skill: {skill.name}")
        chat.add_user(f"Run the saved skill '{skill.name}'.")
        chat.add_assistant(f"Using skill {skill.name}.\nJQL: {jql}")
        st.session_state.pop("skill_run")
        propose(jql, skill.fields, skill.limit, skill.name)
        st.rerun()


def proposal_panel(ctx) -> None:
    prop = st.session_state.get("proposal")
    if not prop:
        return
    pid = st.session_state["pid"]
    with st.container(border=True):
        label = f"Using skill '{prop['skill']}'. " if prop["skill"] else ""
        st.markdown(f"**Query to run.** {label}Check it, edit it if you like, then run it.")
        jql = st.text_area("JQL", prop["jql"], key=f"jql_{pid}", height=100, label_visibility="collapsed")
        c1, c2, c3 = st.columns([3, 1.2, 2])
        fields = c1.text_input("Columns (optional)", prop["fields"], key=f"fields_{pid}")
        limit = c2.number_input("Max rows", 1, 100000, int(prop["limit"] or ctx.settings.default_limit), key=f"limit_{pid}")
        everything = c3.checkbox("Fetch every page", key=f"all_{pid}",
                                 help="Ask ACLI for all matching issues instead of stopping at Max rows. Best for big reviews.")
        b1, b2, _ = st.columns([1, 1, 5])
        run = b1.button("Run query", type="primary", key=f"run_{pid}")
        if b2.button("Discard", key=f"discard_{pid}"):
            st.session_state["proposal"] = None
            st.rerun()
    if not run:
        return
    chat: ChatSession = st.session_state["chat"]
    try:
        clean = jira.clean_jql(jql)
    except ValueError as exc:
        st.error(str(exc))
        return
    chat.last_jql = clean
    prop.update(jql=clean, fields=fields)
    try:
        with st.spinner("Running in Jira..."):
            res = ctx.acli.search(clean, fields, int(limit), paginate=everything)
    except CommandError as exc:
        say("error", "That did not work.\n" + str(exc) + (("\n\n" + _hint(str(exc))) if _hint(str(exc)) else ""))
        st.rerun()
    st.session_state["result"] = res
    n = len(res.rows)
    say("note", f"Ran: {res.jql}\n{n} result{'s' if n != 1 else ''}.")
    if ctx.settings.share_results:
        table = prompts.rows_to_text(res.columns, res.rows, max_rows=25, max_chars=3500)
        chat.add_note(f"The app ran this JQL: {res.jql}\nIt returned {n} rows. First rows:\n{table}")
    else:
        chat.add_note(f"The app ran this JQL: {res.jql}\nIt returned {n} rows. "
                      "The row contents are not shared with you (the user turned that off).")
    if n == 0:
        say("bot", "No results. Tell me if I should widen the query (for example a longer time window, or fewer filters).")
        if res.raw.strip() and res.raw.strip() not in ("[]", "{}"):
            say("note", "The output could not be read as a table. Check the raw output below.")
    st.rerun()


def result_panel(ctx) -> None:
    res = st.session_state.get("result")
    if res is None:
        return
    chat: ChatSession = st.session_state["chat"]
    n = len(res.rows)
    with st.container(border=True):
        st.markdown(f"**{n} issue{'s' if n != 1 else ''} found.**")
        if n:
            st.dataframe(res.rows[:8], hide_index=True, width="stretch")
            if n > 8:
                st.caption(f"Previewing 8 of {n}. Open the Review grid to see them all.")
            default = services.default_review_name(chat.last_question or "My review")
            name = st.text_input("Review name", default, key=f"rname_{st.session_state['pid']}",
                                 help="Re-using a name refreshes that review and keeps its marks and notes.")
            c1, c2, _ = st.columns([1.4, 1, 4])
            if c1.button("Open in Review", type="primary", key="open_review"):
                try:
                    ctx.reviews.save_snapshot(name, res.jql, res.columns, res.rows)
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.session_state["review_name"] = name.strip()
                    pages = st.session_state.get("_pages", {})
                    if "review" in pages:
                        st.switch_page(pages["review"])
            summarise = c2.button("Summarise", key="summarise")
            if summarise:
                allowed = ctx.settings.share_results or st.session_state.get("share_once")
                if not allowed:
                    st.session_state["ask_share"] = True
                else:
                    _summarise(ctx, res)
            if st.session_state.get("ask_share") and not ctx.settings.share_results:
                if st.checkbox("Allow Copilot to see the first rows of these results (this time only)", key="share_once"):
                    st.session_state.pop("ask_share")
                    _summarise(ctx, res)
        if res.raw and n == 0:
            with st.expander("Raw ACLI output"):
                st.code(res.raw[:5000])


def _summarise(ctx, res) -> None:
    chat: ChatSession = st.session_state["chat"]
    prompt = prompts.summary_prompt(
        chat.last_question, res.jql, res.columns, res.rows, current_agent(ctx), ctx.settings.max_prompt_chars)
    try:
        with st.spinner("Summarising..."):
            raw = ctx.llm.ask(prompt)
    except CommandError as exc:
        say("error", str(exc))
        st.rerun()
    text = protocol.parse_reply(raw).message or raw
    chat.add_assistant(text)
    say("bot", text)
    st.rerun()


def welcome(ctx) -> None:
    skills = ctx.skills.list()
    pages = st.session_state.get("_pages", {})
    with st.chat_message("assistant"):
        if not skills:
            st.markdown(
                "Hi. I am your Jira bot, and I have not been taught any Jira skills yet, so I start from a blank slate.\n\n"
                "1. **Ask in plain English**, for example *open bugs in project ABC from the last 2 weeks*. "
                "I will work out the JQL, ask you questions if I need to, and show you the query before anything runs.\n"
                "2. **Teach me** with a skill document (upload it or give its path), or start from example JQL patterns.\n"
                "3. When a session goes well, **save it as a skill** and I will remember it."
            )
            if "skills" in pages:
                st.page_link(pages["skills"], label="Teach me", icon="📚")
        else:
            st.markdown(f"Welcome back. I know **{len(skills)} skill{'s' if len(skills) != 1 else ''}**. "
                        "Run one, or just describe what you need and I will suggest one if it fits.")
            cols = st.columns(min(3, len(skills)))
            for i, skill in enumerate(skills[:9]):
                if cols[i % len(cols)].button(f"▶ {skill.name}", key=f"quick_{skill.name}", help=skill.description or None):
                    st.session_state["skill_run"] = {"name": skill.name, "presets": {}}
                    st.rerun()
    for w in services.setup_warnings(ctx.settings):
        st.warning(w)


def page() -> None:
    ctx = services.context()
    _state()
    st.title("Ask Jira")
    top2, top3, top4, _ = st.columns([2.2, 1.2, 1.4, 3])
    agents = ["(no agent)"] + ctx.agents.names()
    top2.selectbox("Agent", agents, key="agent_name", label_visibility="collapsed",
                   help="Agents add instructions, skills and default values.")
    if top3.button("New chat", use_container_width=True):
        new_chat()
        st.rerun()
    with top4.popover("Save what worked", use_container_width=True):
        name = st.text_input("Name (optional)", key="save_name")
        if st.button("Save as skill", use_container_width=True):
            draft_skill(ctx, name)
            st.rerun()
        if st.button("Save as agent", use_container_width=True):
            draft_agent(ctx, name)
            st.rerun()

    if skills_page.draft_review():
        st.divider()

    msgs = st.session_state["msgs"]
    if not msgs:
        welcome(ctx)
    for m in msgs:
        if m["kind"] == "user":
            with st.chat_message("user"):
                st.markdown(m["text"])
        elif m["kind"] == "bot":
            with st.chat_message("assistant"):
                st.markdown(m["text"])
        elif m["kind"] == "error":
            with st.chat_message("assistant"):
                st.error(m["text"])
        else:
            st.caption(m["text"])

    skill_run_panel(ctx)
    proposal_panel(ctx)
    result_panel(ctx)

    text = st.chat_input("Describe what you need, for example: open bugs in ABC from the last 2 weeks")
    if text:
        on_user_text(ctx, text.strip())
        st.rerun()
