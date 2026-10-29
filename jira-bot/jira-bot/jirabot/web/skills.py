"""Skills page: list, edit, import documents, examples. Also the shared draft reviewer."""
from __future__ import annotations

from typing import List, Optional

import streamlit as st

from .. import examples, skillgen
from ..importer import ImportProblem, document_from_text, parse_path_list, read_document, read_upload
from ..proc import CommandError
from ..store import Param, Skill, parse_param_line, slugify
from . import services

QUEUE = "skill_drafts"


def queue_drafts(drafts: List[Skill], note: str = "") -> None:
    st.session_state.setdefault(QUEUE, [])
    st.session_state[QUEUE].extend({"skill": d, "note": note} for d in drafts)


def skill_form(skill: Skill, key: str, title: str, note: str = "", allow_skip: bool = False,
               editing: bool = False) -> Optional[str]:
    """Edit a skill. Returns 'saved', 'skipped' or None."""
    ctx = services.context()
    st.subheader(title)
    if note:
        st.caption(note)
    with st.form(key):
        name = st.text_input("Name", skill.name, help="Lowercase letters, digits, - and _. Used as the file name.")
        description = st.text_input("What it is for", skill.description)
        jql = st.text_area("JQL", skill.jql, height=110, help="Use {placeholders} for values that change, for example {project}.")
        c1, c2 = st.columns([3, 1])
        fields = c1.text_input("Columns to fetch (optional, comma separated)", skill.fields)
        limit = c2.number_input("Max rows (0 = default)", 0, 100000, int(skill.limit or 0))
        params = st.text_area(
            "Parameters (one per line: name | description | default)",
            "\n".join(p.to_line() for p in skill.parameters), height=90,
        )
        output = st.text_area("How to present the results (optional)", skill.output, height=70)
        notes = st.text_area("Notes (optional)", skill.notes, height=70)
        replace = st.checkbox("Replace an existing skill with this name", value=editing)
        c_save, c_skip = st.columns([1, 1])
        save = c_save.form_submit_button("Save skill", type="primary")
        skip = c_skip.form_submit_button("Skip") if allow_skip else False
    if skip:
        return "skipped"
    if not save:
        return None
    try:
        parsed: List[Param] = []
        for line in params.splitlines():
            p = parse_param_line(line)
            if p:
                parsed.append(p)
        item = Skill(
            name=slugify(name), description=description.strip(), jql=jql.strip(), parameters=parsed,
            fields=fields.strip(), limit=int(limit) or None, output=output.strip(), notes=notes.strip(),
        )
        ctx.skills.save(item, overwrite=replace)
    except FileExistsError as exc:
        st.error(f"{exc} Tick 'Replace an existing skill' to overwrite it.")
        return None
    except ValueError as exc:
        st.error(str(exc))
        return None
    st.toast(f"Saved skill '{item.name}'.")
    return "saved"


def draft_review() -> bool:
    """Show the first queued draft. Returns True if one is on screen."""
    queue = st.session_state.get(QUEUE) or []
    if not queue:
        return False
    first = queue[0]
    total = len(queue)
    title = "Save as skill" if total == 1 else f"Save as skill ({total} waiting)"
    result = skill_form(first["skill"], f"draft_{id(first)}", title, first["note"], allow_skip=True)
    if result:
        queue.pop(0)
        st.rerun()
    return True


def _documents_from_inputs(uploads, paths_text: str, pasted: str):
    docs, problems = [], []
    for up in uploads or []:
        try:
            docs.append(read_upload(up.name, up.getvalue()))
        except ImportProblem as exc:
            problems.append(str(exc))
    for raw in parse_path_list(paths_text):
        try:
            docs.append(read_document(raw))
        except ImportProblem as exc:
            problems.append(str(exc))
    if pasted.strip():
        try:
            docs.append(document_from_text(pasted, "pasted-text"))
        except ImportProblem as exc:
            problems.append(str(exc))
    return docs, problems


def teach_tab() -> None:
    ctx = services.context()
    st.markdown(
        "Give me a skill document and I will turn the JQL in it into reusable skills. "
        "Upload a file, give its path on this computer, or paste text."
    )
    uploads = st.file_uploader(
        "Upload documents (.md .txt .jql .json .yaml .csv .docx)", accept_multiple_files=True,
        type=["md", "markdown", "txt", "text", "jql", "json", "yaml", "yml", "csv", "docx"],
    )
    paths = st.text_area(
        "...or file paths on this computer (one per line)", height=70,
        placeholder="~/Documents/triage-playbook.docx",
    )
    pasted = st.text_area("...or paste text", height=110)
    use_llm = st.checkbox("Use Copilot to read the documents (recommended)", value=True)
    if st.button("Read the documents", type="primary"):
        docs, problems = _documents_from_inputs(uploads, paths, pasted)
        for p in problems:
            st.error(p)
        for doc in docs:
            try:
                with st.spinner(f"Reading {doc.name}..."):
                    drafts, notes = skillgen.skills_from_document(
                        ctx.llm if use_llm else None, doc, ctx.skills.names()
                    )
                queue_drafts(drafts, f"From {doc.name}. " + " ".join(notes))
            except (ValueError, CommandError) as exc:
                st.error(f"{doc.name}: {exc}")
        if st.session_state.get(QUEUE):
            st.rerun()
    st.divider()
    st.markdown("**Or start from an example pattern**")
    for example in examples.example_skills():
        c1, c2 = st.columns([5, 1])
        c1.markdown(f"**{example.name}**  \n<span class='jb-muted'>{example.description}</span>", unsafe_allow_html=True)
        if c2.button("Use", key=f"ex_{example.name}"):
            queue_drafts([example], "Example pattern. Adjust it to fit your Jira.")
            st.rerun()


def list_tab() -> None:
    ctx = services.context()
    skills = ctx.skills.list()
    for name, why in ctx.skills.errors:
        st.warning(f"Could not read {name}: {why}")
    if not skills:
        st.info("No skills yet. Use the Teach me tab, or save one from a chat.")
        return
    editing = st.session_state.get("edit_skill")
    for skill in skills:
        if editing == skill.name:
            if skill_form(skill, f"edit_{skill.name}", f"Edit skill: {skill.name}", editing=True):
                st.session_state.pop("edit_skill")
                st.rerun()
            if st.button("Cancel editing", key=f"cancel_{skill.name}"):
                st.session_state.pop("edit_skill")
                st.rerun()
            continue
        with st.expander(f"**{skill.name}**  {('- ' + skill.description) if skill.description else ''}"):
            st.code(skill.jql, language="sql")
            if skill.parameters:
                st.caption("Parameters: " + ", ".join(
                    f"{p.name}" + (f" (default {p.default})" if p.default else "") for p in skill.parameters))
            c1, c2, _ = st.columns([1, 1, 6])
            if c1.button("Edit", key=f"e_{skill.name}"):
                st.session_state["edit_skill"] = skill.name
                st.rerun()
            if c2.button("Delete", key=f"d_{skill.name}"):
                st.session_state["confirm_delete_skill"] = skill.name
                st.rerun()
            if st.session_state.get("confirm_delete_skill") == skill.name:
                st.warning(f"Delete '{skill.name}'? This cannot be undone.")
                if st.button("Yes, delete it", key=f"yd_{skill.name}"):
                    ctx.skills.delete(skill.name)
                    st.session_state.pop("confirm_delete_skill")
                    st.rerun()


def page() -> None:
    st.title("Skills")
    if draft_review():
        st.divider()
    tab_list, tab_teach = st.tabs(["My skills", "Teach me"])
    with tab_list:
        list_tab()
    with tab_teach:
        teach_tab()
