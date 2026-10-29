"""Reviews: a saved set of Jira results plus your annotations, stored in SQLite.

A *review* is one working session over a list of issues (for example "Sprint 42 triage").
It remembers the JQL, a snapshot of the rows, which columns you hid, your colour-coded marks,
and your notes. Annotations are keyed by issue key, so re-running the query refreshes the rows
without losing what you wrote. No UI code lives here, so it can be tested.
"""
from __future__ import annotations

import json
import re
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

# name -> (emoji used inside dropdowns, solid hex, translucent tint used for row backgrounds)
PALETTE: Dict[str, Tuple[str, str, str]] = {
    "green": ("\U0001F7E9", "#2e9e5b", "rgba(46, 158, 91, 0.22)"),
    "blue": ("\U0001F7E6", "#3b82f6", "rgba(59, 130, 246, 0.22)"),
    "orange": ("\U0001F7E7", "#f59e0b", "rgba(245, 158, 11, 0.25)"),
    "red": ("\U0001F7E5", "#ef4444", "rgba(239, 68, 68, 0.22)"),
    "purple": ("\U0001F7EA", "#8b5cf6", "rgba(139, 92, 246, 0.22)"),
    "yellow": ("\U0001F7E8", "#eab308", "rgba(234, 179, 8, 0.28)"),
    "grey": ("⬜", "#6b7280", "rgba(107, 114, 128, 0.20)"),
}


@dataclass
class Mark:
    name: str
    color: str = "grey"

    @property
    def emoji(self) -> str:
        return PALETTE.get(self.color, PALETTE["grey"])[0]

    @property
    def hex(self) -> str:
        return PALETTE.get(self.color, PALETTE["grey"])[1]

    @property
    def tint(self) -> str:
        return PALETTE.get(self.color, PALETTE["grey"])[2]

    @property
    def label(self) -> str:
        """Text shown in the dropdown, with a colour square so colour is visible in the grid."""
        return f"{self.emoji} {self.name}"


DEFAULT_MARKS: List[Mark] = [
    Mark("Keep", "green"),
    Mark("Discuss", "blue"),
    Mark("Move out", "orange"),
    Mark("Not doing", "red"),
]


@dataclass
class Annotation:
    mark: str = ""
    note: str = ""
    updated_at: str = ""


@dataclass
class Review:
    name: str
    jql: str = ""
    columns: List[str] = field(default_factory=list)
    hidden: List[str] = field(default_factory=list)
    marks: List[Mark] = field(default_factory=lambda: [Mark(m.name, m.color) for m in DEFAULT_MARKS])
    fetched_at: str = ""
    row_count: int = 0

    def mark_by_name(self, name: str) -> Optional[Mark]:
        return next((m for m in self.marks if m.name == name), None)

    def label_for(self, name: str) -> str:
        mark = self.mark_by_name(name)
        if mark:
            return mark.label
        return f"⬜ {name}" if name else ""

    def name_for_label(self, label: str) -> str:
        label = (label or "").strip()
        for mark in self.marks:
            if label == mark.label or label == mark.name:
                return mark.name
        return label


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def clean_review_name(name: str) -> str:
    name = re.sub(r"\s+", " ", (name or "")).strip()
    return name[:80]


SCHEMA = """
CREATE TABLE IF NOT EXISTS reviews (
    name TEXT PRIMARY KEY,
    jql TEXT NOT NULL DEFAULT '',
    columns TEXT NOT NULL DEFAULT '[]',
    hidden TEXT NOT NULL DEFAULT '[]',
    marks TEXT NOT NULL DEFAULT '[]',
    fetched_at TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS issues (
    review TEXT NOT NULL,
    key TEXT NOT NULL,
    pos INTEGER NOT NULL,
    data TEXT NOT NULL,
    PRIMARY KEY (review, key)
);
CREATE TABLE IF NOT EXISTS annotations (
    review TEXT NOT NULL,
    key TEXT NOT NULL,
    mark TEXT NOT NULL DEFAULT '',
    note TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (review, key)
);
CREATE INDEX IF NOT EXISTS idx_issues_review ON issues(review, pos);
"""


class ReviewStore:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as conn:
            conn.executescript(SCHEMA)

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        # A short-lived connection per call keeps this safe when several people use the app at once.
        conn = sqlite3.connect(str(self.path), timeout=15)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=15000")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # --------------------------------------------------------------- reviews

    def list_reviews(self) -> List[Review]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT r.*, (SELECT COUNT(*) FROM issues i WHERE i.review = r.name) AS n "
                "FROM reviews r ORDER BY COALESCE(NULLIF(r.fetched_at, ''), r.created_at) DESC, r.name"
            ).fetchall()
        return [self._review_from_row(r, r["n"]) for r in rows]

    def get(self, name: str) -> Optional[Review]:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM reviews WHERE name = ?", (name,)).fetchone()
            if row is None:
                return None
            n = conn.execute("SELECT COUNT(*) FROM issues WHERE review = ?", (name,)).fetchone()[0]
        return self._review_from_row(row, n)

    def ensure(self, name: str) -> Review:
        name = clean_review_name(name)
        if not name:
            raise ValueError("A review needs a name.")
        existing = self.get(name)
        if existing:
            return existing
        marks = json.dumps([{"name": m.name, "color": m.color} for m in DEFAULT_MARKS])
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO reviews (name, marks, created_at) VALUES (?, ?, ?)", (name, marks, now())
            )
        return self.get(name)  # type: ignore[return-value]

    def delete(self, name: str) -> None:
        with self._conn() as conn:
            for table, col in (("issues", "review"), ("annotations", "review"), ("reviews", "name")):
                conn.execute(f"DELETE FROM {table} WHERE {col} = ?", (name,))

    @staticmethod
    def _review_from_row(row: sqlite3.Row, count: int) -> Review:
        try:
            marks_raw = json.loads(row["marks"] or "[]")
        except ValueError:
            marks_raw = []
        marks = [Mark(str(m.get("name", "")), str(m.get("color", "grey"))) for m in marks_raw if m.get("name")]
        return Review(
            name=row["name"],
            jql=row["jql"],
            columns=json.loads(row["columns"] or "[]"),
            hidden=json.loads(row["hidden"] or "[]"),
            marks=marks or [Mark(m.name, m.color) for m in DEFAULT_MARKS],
            fetched_at=row["fetched_at"],
            row_count=count,
        )

    # -------------------------------------------------------------- settings

    def set_hidden(self, name: str, hidden: Sequence[str]) -> None:
        with self._conn() as conn:
            conn.execute("UPDATE reviews SET hidden = ? WHERE name = ?", (json.dumps(list(hidden)), name))

    def set_marks(self, name: str, marks: Sequence[Mark]) -> None:
        cleaned: List[Mark] = []
        seen = set()
        for mark in marks:
            label = re.sub(r"\s+", " ", mark.name or "").strip()
            if label and label.lower() not in seen:
                seen.add(label.lower())
                cleaned.append(Mark(label, mark.color if mark.color in PALETTE else "grey"))
        if not cleaned:
            raise ValueError("Keep at least one mark.")
        with self._conn() as conn:
            conn.execute(
                "UPDATE reviews SET marks = ? WHERE name = ?",
                (json.dumps([{"name": m.name, "color": m.color} for m in cleaned]), name),
            )

    # ------------------------------------------------------------- snapshots

    def save_snapshot(self, name: str, jql: str, columns: Sequence[str], rows: Sequence[Dict[str, str]]) -> int:
        """Replace the saved rows with a fresh result set. Annotations are kept."""
        self.ensure(name)
        columns = list(columns)
        prepared: List[Tuple[str, int, str]] = []
        seen = set()
        for index, row in enumerate(rows):
            key = str(row.get("key") or f"row-{index + 1}")
            if key in seen:
                continue
            seen.add(key)
            data = dict(row)
            data["key"] = key
            prepared.append((key, index, json.dumps(data, ensure_ascii=False)))
        if prepared and "key" not in columns:
            columns.insert(0, "key")
        with self._conn() as conn:
            conn.execute("DELETE FROM issues WHERE review = ?", (name,))
            conn.executemany(
                "INSERT INTO issues (review, key, pos, data) VALUES (?, ?, ?, ?)",
                [(name, k, p, d) for k, p, d in prepared],
            )
            conn.execute(
                "UPDATE reviews SET jql = ?, columns = ?, fetched_at = ? WHERE name = ?",
                (jql, json.dumps(columns), now(), name),
            )
        return len(prepared)

    def load_rows(self, name: str) -> List[Dict[str, str]]:
        with self._conn() as conn:
            rows = conn.execute("SELECT data FROM issues WHERE review = ? ORDER BY pos", (name,)).fetchall()
        return [json.loads(r["data"]) for r in rows]

    # ----------------------------------------------------------- annotations

    def annotations(self, name: str) -> Dict[str, Annotation]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT key, mark, note, updated_at FROM annotations WHERE review = ?", (name,)
            ).fetchall()
        return {r["key"]: Annotation(r["mark"], r["note"], r["updated_at"]) for r in rows}

    def set_annotation(
        self, name: str, key: str, mark: Optional[str] = None, note: Optional[str] = None
    ) -> None:
        """Set a mark and/or a note. None leaves that field as it is; "" clears it."""
        self.set_annotations(name, [(key, mark, note)])

    def set_annotations(
        self, name: str, changes: Iterable[Tuple[str, Optional[str], Optional[str]]]
    ) -> int:
        count = 0
        stamp = now()
        with self._conn() as conn:
            for key, mark, note in changes:
                current = conn.execute(
                    "SELECT mark, note FROM annotations WHERE review = ? AND key = ?", (name, key)
                ).fetchone()
                new_mark = (current["mark"] if current else "") if mark is None else mark
                new_note = (current["note"] if current else "") if note is None else note
                if not new_mark and not new_note:
                    conn.execute("DELETE FROM annotations WHERE review = ? AND key = ?", (name, key))
                else:
                    conn.execute(
                        "INSERT INTO annotations (review, key, mark, note, updated_at) VALUES (?, ?, ?, ?, ?) "
                        "ON CONFLICT(review, key) DO UPDATE SET mark = excluded.mark, "
                        "note = excluded.note, updated_at = excluded.updated_at",
                        (name, key, new_mark, new_note, stamp),
                    )
                count += 1
        return count

    def apply_mark(self, name: str, keys: Iterable[str], mark: str) -> int:
        return self.set_annotations(name, [(k, mark, None) for k in keys])

    def mark_counts(self, name: str) -> Dict[str, int]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT a.mark AS mark, COUNT(*) AS n FROM annotations a "
                "JOIN issues i ON i.review = a.review AND i.key = a.key "
                "WHERE a.review = ? GROUP BY a.mark",
                (name,),
            ).fetchall()
        return {r["mark"]: r["n"] for r in rows}


def merge_rows(
    rows: Sequence[Dict[str, str]], notes: Dict[str, Annotation]
) -> List[Dict[str, str]]:
    """Rows with the annotation columns added (Mark and Note), in the saved order."""
    merged = []
    for row in rows:
        ann = notes.get(row.get("key", ""))
        item = dict(row)
        item["_mark"] = ann.mark if ann else ""
        item["_note"] = ann.note if ann else ""
        merged.append(item)
    return merged
