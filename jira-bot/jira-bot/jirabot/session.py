"""Conversation state (no UI code, so it can be tested)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Turn:
    role: str  # "user", "assistant" or "note"
    text: str

    def render(self, limit: int = 3000) -> str:
        text = self.text if len(self.text) <= limit else self.text[:limit] + " ..."
        if self.role == "user":
            return f"User: {text}"
        if self.role == "assistant":
            return f"Assistant: {text}"
        return f"[App] {text}"


@dataclass
class ChatSession:
    turns: List[Turn] = field(default_factory=list)
    last_jql: str = ""
    last_question: str = ""

    def reset(self) -> None:
        self.turns.clear()
        self.last_jql = ""
        self.last_question = ""

    def add_user(self, text: str) -> None:
        self.turns.append(Turn("user", text))
        self.last_question = text

    def add_assistant(self, text: str) -> None:
        self.turns.append(Turn("assistant", text))

    def add_note(self, text: str) -> None:
        self.turns.append(Turn("note", text))

    def has_user_turn(self) -> bool:
        return any(t.role == "user" for t in self.turns)

    def latest_user_text(self) -> Optional[str]:
        for turn in reversed(self.turns):
            if turn.role == "user":
                return turn.text
        return None
