"""Pure helpers behind the review grid (no Streamlit calls, so they can be unit tested)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import pandas as pd

from ..reviews import Annotation, Review, merge_rows

PICK = "Pick"
MARK = "Mark"
NOTE = "Note"
UNMARKED = "(no mark)"
EDITOR_COLUMNS = (PICK, MARK, NOTE)


@dataclass
class Frame:
    df: "pd.DataFrame"
    keys: List[str]  # issue key for each row of df, in order
    total: int  # rows before the search / mark filter
    shown_columns: List[str]
    rows: List[Dict[str, str]]  # the matching rows with _mark / _note, for export


def pretty(column: str) -> str:
    return "Key" if column == "key" else column.replace("_", " ").title()


def visible_columns(review: Review) -> List[str]:
    hidden = set(review.hidden)
    cols = [c for c in review.columns if c not in hidden]
    if "key" in cols:
        cols.remove("key")
        cols.insert(0, "key")
    return cols


def issue_url(site: str, key: str) -> str:
    return f"https://{site}/browse/{key}" if site and key and not key.startswith("row-") else key


def row_matches(row: Dict[str, str], needle: str) -> bool:
    return any(needle in str(v).lower() for v in row.values())


def build_frame(
    review: Review,
    rows: Sequence[Dict[str, str]],
    annotations: Dict[str, Annotation],
    site: str = "",
    search: str = "",
    mark_filter: Optional[Sequence[str]] = None,
) -> Frame:
    """The table shown in the editor: Pick, Mark, Note, then the Jira columns."""
    merged = merge_rows(rows, annotations)
    needle = (search or "").strip().lower()
    wanted = set(mark_filter or [])
    cols = visible_columns(review)
    out_rows: List[Dict[str, object]] = []
    keys: List[str] = []
    kept: List[Dict[str, str]] = []
    for row in merged:
        mark = row["_mark"]
        if wanted and (mark or UNMARKED) not in wanted:
            continue
        if needle and not row_matches(row, needle):
            continue
        item: Dict[str, object] = {PICK: False, MARK: review.label_for(mark) or None, NOTE: row["_note"]}
        for c in cols:
            value = row.get(c, "")
            item[c] = issue_url(site, value) if c == "key" else value
        out_rows.append(item)
        keys.append(row.get("key", ""))
        kept.append(row)
    df = pd.DataFrame(out_rows, columns=[PICK, MARK, NOTE] + cols)
    df[PICK] = df[PICK].astype(bool)
    return Frame(df=df, keys=keys, total=len(merged), shown_columns=cols, rows=kept)


def tint_styler(df: "pd.DataFrame", review: Review):
    """Row tint by mark. Streamlit shows it on the read-only cells; editable cells keep the colour square.

    Vectorised, so a 20,000-row table is styled in a fraction of a second.
    """
    tints = {m.label: f"background-color: {m.tint}" for m in review.marks}

    def paint(frame):
        column = frame[MARK].map(tints).fillna("")
        return pd.DataFrame({name: column for name in frame.columns}, index=frame.index)

    return df.style.apply(paint, axis=None)


def parse_edits(
    state: Optional[dict], keys: Sequence[str], review: Review
) -> Tuple[Dict[str, Dict[str, str]], List[str]]:
    """Turn the data editor's change log into ({issue key: {mark/note}}, picked keys).

    Row numbers in the log refer to the table as it was drawn, even when the user has
    sorted the grid, so `keys` must be the key list from that same draw.
    """
    changes: Dict[str, Dict[str, str]] = {}
    picked: List[str] = []
    edited = (state or {}).get("edited_rows") or {}
    for raw_index, delta in edited.items():
        try:
            index = int(raw_index)
        except (TypeError, ValueError):
            continue
        if not 0 <= index < len(keys) or not isinstance(delta, dict):
            continue
        key = keys[index]
        if delta.get(PICK) is True:
            picked.append(key)
        change: Dict[str, str] = {}
        if MARK in delta:
            change["mark"] = review.name_for_label(delta[MARK] or "")
        if NOTE in delta:
            change["note"] = (delta[NOTE] or "").strip()
        if change:
            changes[key] = change
    return changes, picked


def column_summary(review: Review) -> str:
    cols = visible_columns(review)
    return f"{len(cols)} of {len(review.columns)} columns shown"
