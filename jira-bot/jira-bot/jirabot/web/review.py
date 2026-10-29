"""Review page: an Excel-like grid with sorting, hidden columns, colour marks and notes that are saved."""
from __future__ import annotations

from typing import List

import pandas as pd
import streamlit as st

from .. import export
from ..jira import clean_jql
from ..proc import CommandError
from ..reviews import PALETTE, Mark
from . import grid, services


def _persist(name: str, keys: List[str], review, state_key: str) -> None:
    """Runs when the grid is edited: save the Mark and Note changes straight away."""
    ctx = services.context()
    changes, _ = grid.parse_edits(st.session_state.get(state_key), keys, review)
    if changes:
        ctx.reviews.set_annotations(
            name, [(k, c.get("mark"), c.get("note")) for k, c in changes.items()]
        )
        st.session_state["saved_flash"] = f"Saved {len(changes)} change{'s' if len(changes) != 1 else ''}."


def _epoch(name: str) -> int:
    return st.session_state.setdefault("grid_epoch", {}).setdefault(name, 0)


def _bump(name: str) -> None:
    st.session_state.setdefault("grid_epoch", {})[name] = _epoch(name) + 1


def _marks_editor(ctx, review) -> None:
    with st.expander("Marks and colours"):
        st.caption("Rename, recolour, add or remove the marks you use in meetings (for example Move out, Not doing).")
        df = pd.DataFrame([{"Mark": m.name, "Colour": m.color} for m in review.marks])
        edited = st.data_editor(
            df, num_rows="dynamic", hide_index=True, key=f"marks_{review.name}",
            column_config={
                "Mark": st.column_config.TextColumn("Mark", required=True, max_chars=40),
                "Colour": st.column_config.SelectboxColumn("Colour", options=list(PALETTE), required=True),
            },
        )
        if st.button("Save marks", key=f"save_marks_{review.name}"):
            try:
                marks = [Mark(str(r["Mark"]).strip(), str(r["Colour"])) for _, r in edited.iterrows()
                         if str(r["Mark"]).strip() and str(r["Mark"]) != "nan"]
                ctx.reviews.set_marks(review.name, marks)
                _bump(review.name)
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))


def _refresh(ctx, review) -> None:
    fields = ",".join(c for c in review.columns if c != "key")
    try:
        with st.spinner("Fetching from Jira..."):
            res = ctx.acli.search(clean_jql(review.jql), fields, paginate=True)
        count = ctx.reviews.save_snapshot(review.name, review.jql, res.columns or review.columns, res.rows)
        _bump(review.name)
        st.session_state["saved_flash"] = f"Refreshed: {count} issues. Your marks and notes were kept."
        st.rerun()
    except (CommandError, ValueError) as exc:
        st.error(str(exc))


def page() -> None:
    ctx = services.context()
    st.title("Review")
    reviews = ctx.reviews.list_reviews()
    if not reviews:
        st.info("Nothing to review yet. Ask for some issues first, then press 'Open in Review'.")
        pages = st.session_state.get("_pages", {})
        if "ask" in pages:
            st.page_link(pages["ask"], label="Go to Ask", icon="💬")
        return

    names = [r.name for r in reviews]
    wanted = st.session_state.get("review_name")
    index = names.index(wanted) if wanted in names else 0
    head1, head2 = st.columns([3, 1])
    name = head1.selectbox("Review", names, index=index, label_visibility="collapsed")
    st.session_state["review_name"] = name
    review = ctx.reviews.get(name)
    if review is None:
        st.stop()
    with head2.popover("Review actions", use_container_width=True):
        if st.button("Refresh from Jira", key="refresh"):
            _refresh(ctx, review)
        if st.checkbox("I want to delete this review", key=f"delask_{name}"):
            if st.button("Delete review", key=f"del_{name}"):
                ctx.reviews.delete(name)
                st.session_state.pop("review_name", None)
                st.rerun()

    rows = ctx.reviews.load_rows(name)
    annotations = ctx.reviews.annotations(name)
    counts = ctx.reviews.mark_counts(name)

    pills = "".join(
        f"<span class='jb-pill'>{m.emoji} {m.name}: <b>{counts.get(m.name, 0)}</b></span>" for m in review.marks
    )
    st.markdown(f"<span class='jb-pill'>{len(rows)} issues</span>{pills}", unsafe_allow_html=True)
    st.caption(f"JQL: `{review.jql}`  |  fetched {review.fetched_at} UTC")

    flash = st.session_state.pop("saved_flash", None)
    if flash:
        st.toast(flash)

    f1, f2, f3 = st.columns([2, 2, 3])
    search = f1.text_input("Search", placeholder="Search keys, text and notes", label_visibility="collapsed",
                           key=f"search_{name}")
    mark_options = [m.name for m in review.marks] + [grid.UNMARKED]
    mark_filter = f2.multiselect("Marks", mark_options, placeholder="Filter by mark", label_visibility="collapsed",
                                 key=f"mf_{name}")
    all_cols = [c for c in review.columns]
    shown = f3.multiselect(
        "Columns", all_cols, default=[c for c in all_cols if c not in set(review.hidden)],
        placeholder="Columns to show", label_visibility="collapsed", key=f"cols_{name}_{_epoch(name)}",
        format_func=grid.pretty,
    )
    new_hidden = [c for c in all_cols if c not in shown]
    if new_hidden != review.hidden and shown:
        ctx.reviews.set_hidden(name, new_hidden)
        review = ctx.reviews.get(name)

    frame = grid.build_frame(review, rows, annotations, ctx.settings.site_host, search, mark_filter)
    st.caption(f"Showing {len(frame.keys)} of {frame.total}. Click a column header to sort; use the toolbar above the grid "
               "to search, download or go full screen. Pick a Mark from the dropdown or type a Note: both save automatically.")

    cfg = {
        grid.PICK: st.column_config.CheckboxColumn("Pick", width=60, help="Tick rows to mark several at once"),
        grid.MARK: st.column_config.SelectboxColumn(
            "Mark", options=[m.label for m in review.marks], width=150, required=False),
        grid.NOTE: st.column_config.TextColumn("Note", width=260, max_chars=1000),
    }
    for c in frame.shown_columns:
        if c == "key":
            if ctx.settings.site_host:
                cfg[c] = st.column_config.LinkColumn("Key", display_text=r"browse/(.*)$", width=90, pinned=True)
            else:
                cfg[c] = st.column_config.TextColumn("Key", width=90, pinned=True)
        else:
            cfg[c] = st.column_config.TextColumn(grid.pretty(c))

    sig = hash(tuple(frame.keys)) & 0xFFFFFFFF
    state_key = f"grid_{name}_{_epoch(name)}_{sig}_{len(review.marks)}"
    _, picked = grid.parse_edits(st.session_state.get(state_key), frame.keys, review)
    b1, b2, b3, b4 = st.columns([2, 1.5, 1.7, 2])
    choice = b1.selectbox("Mark to apply", [m.label for m in review.marks] + ["(clear mark)"],
                          label_visibility="collapsed", key=f"bulk_{name}")
    target = "" if choice.startswith("(") else review.name_for_label(choice)
    if b2.button(f"Apply to {len(picked)} picked", disabled=not picked, key=f"ap_{name}"):
        ctx.reviews.apply_mark(name, picked, target)
        _bump(name)
        st.session_state["saved_flash"] = f"Marked {len(picked)} issues."
        st.rerun()
    if b3.button(f"Apply to all {len(frame.keys)} shown", disabled=not frame.keys, key=f"aa_{name}"):
        ctx.reviews.apply_mark(name, frame.keys, target)
        _bump(name)
        st.session_state["saved_flash"] = f"Marked {len(frame.keys)} issues."
        st.rerun()

    e1, e2 = b4.columns(2)
    safe = "".join(ch if ch.isalnum() or ch in "-_ " else "_" for ch in name).strip() or "review"
    e1.download_button("CSV", export.to_csv(review.columns, review.hidden, frame.rows),
                       file_name=f"{safe}.csv", mime="text/csv", on_click="ignore")
    if export.xlsx_available():
        if e2.button("Excel", help="Build an .xlsx with the colours, a frozen header and filters"):
            with st.spinner("Building the workbook..."):
                data = export.to_xlsx(review.columns, review.hidden, frame.rows, review.marks, name)
            st.download_button(
                "Download .xlsx", data, file_name=f"{safe}.xlsx", on_click="ignore", type="primary",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    else:
        e2.caption("pip install openpyxl for Excel")

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)  # room for the grid's floating toolbar
    st.data_editor(
        grid.tint_styler(frame.df, review), key=state_key, hide_index=True, num_rows="fixed",
        width="stretch", height=min(600, 38 + 35 * max(len(frame.keys), 3)),
        column_config=cfg, disabled=frame.shown_columns,
        on_change=_persist, args=(name, list(frame.keys), review, state_key),
    )


    _marks_editor(ctx, review)
