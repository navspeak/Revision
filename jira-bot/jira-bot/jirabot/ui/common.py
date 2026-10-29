"""Shared UI plumbing: app context, background work, modal dialogs."""
from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from typing import Callable, Dict, List, Optional

from ..config import Settings
from ..jira import AcliClient
from ..llm import CopilotClient
from ..store import AgentStore, SkillStore


class Asyncer:
    """Run slow work (Copilot, ACLI) on a thread and deliver the result on the Tk thread."""

    def __init__(self, root: tk.Misc):
        self.root = root
        self.q: "queue.Queue" = queue.Queue()
        self._poll()

    def run(
        self,
        work: Callable[[], object],
        on_ok: Optional[Callable[[object], None]] = None,
        on_err: Optional[Callable[[Exception], None]] = None,
    ) -> None:
        def target() -> None:
            try:
                result = work()
            except Exception as exc:  # noqa: BLE001 - delivered to the UI
                self.q.put((on_err, exc))
                return
            self.q.put((on_ok, result))

        threading.Thread(target=target, daemon=True).start()

    def _poll(self) -> None:
        try:
            while True:
                callback, value = self.q.get_nowait()
                if callback is not None:
                    callback(value)
        except queue.Empty:
            pass
        try:
            self.root.after(60, self._poll)
        except tk.TclError:
            pass


class AppContext:
    def __init__(self, root: tk.Misc, settings: Settings):
        self.root = root
        self.settings = settings
        self.skills = SkillStore(settings.skills_dir)
        self.agents = AgentStore(settings.agents_dir)
        self.llm = CopilotClient(settings)
        self.acli = AcliClient(settings)
        self.asyncer = Asyncer(root)
        self.actions: Dict[str, Callable[[], None]] = {}
        self.modal: Optional["Modal"] = None
        self._listeners: List[Callable[[], None]] = []

    def on_change(self, callback: Callable[[], None]) -> None:
        self._listeners.append(callback)

    def changed(self) -> None:
        """Call after skills, agents or settings changed so every tab refreshes."""
        for callback in list(self._listeners):
            callback()


def mono_font() -> tkfont.Font:
    return tkfont.nametofont("TkFixedFont")


def open_folder(path) -> None:
    path = str(path)
    os.makedirs(path, exist_ok=True)
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except OSError:
        pass


def hint_for_error(message: str) -> str:
    low = message.lower()
    if "could not find" in low or "could not start" in low:
        return "Open the Settings tab and check the command path, then use the Test button."
    if any(w in low for w in ("auth", "login", "unauthorized", "401", "403", "credentials", "not logged")):
        return "This looks like a sign-in problem. Open the Settings tab and log in to Jira."
    if "unbounded" in low:
        return "Jira rejected the query because it has no restriction. Add a project, date range or assignee."
    if "longer than" in low:
        return "The command timed out. You can raise the timeout in Settings."
    return ""


class Modal(tk.Toplevel):
    """A dialog that blocks until closed. present() returns self.result."""

    def __init__(self, parent: tk.Misc, title: str, ctx: Optional[AppContext] = None):
        super().__init__(parent)
        self.ctx = ctx
        self.result = None
        self.title(title)
        self.transient(parent.winfo_toplevel())
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind("<Escape>", lambda _e: self.cancel())

    def present(self):
        self.update_idletasks()
        parent = self.master.winfo_toplevel()
        try:
            x = parent.winfo_rootx() + max(0, (parent.winfo_width() - self.winfo_reqwidth()) // 2)
            y = parent.winfo_rooty() + max(0, (parent.winfo_height() - self.winfo_reqheight()) // 3)
            self.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass
        try:
            self.wait_visibility()
            self.grab_set()
        except tk.TclError:
            pass
        if self.ctx is not None:
            self.ctx.modal = self
        self.focus_set()
        self.wait_window(self)
        if self.ctx is not None and self.ctx.modal is self:
            self.ctx.modal = None
        return self.result

    def cancel(self) -> None:
        self.result = None
        self.destroy()
