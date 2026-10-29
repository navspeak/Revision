"""The main window: Chat, Skills, Agents and Settings tabs."""
from __future__ import annotations

import tkinter as tk
import traceback
from tkinter import messagebox, ttk

from ..log import log
from .agents_tab import AgentsTab
from .chat_tab import ChatTab
from .common import AppContext
from .settings_tab import SettingsTab
from .skills_tab import SkillsTab


class MainWindow(ttk.Frame):
    def __init__(self, root: tk.Tk, ctx: AppContext):
        super().__init__(root)
        self.root = root
        self.ctx = ctx
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.chat = ChatTab(self.notebook, ctx)
        self.skills = SkillsTab(self.notebook, ctx)
        self.agents = AgentsTab(self.notebook, ctx)
        self.settings = SettingsTab(self.notebook, ctx)
        self.notebook.add(self.chat, text="Chat")
        self.notebook.add(self.skills, text="Skills")
        self.notebook.add(self.agents, text="Agents")
        self.notebook.add(self.settings, text="Settings")

        ctx.actions["import"] = self._import_from_chat
        ctx.actions["examples"] = self._examples_from_chat

        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.report_callback_exception = self._report_exception

    def _import_from_chat(self) -> None:
        self.notebook.select(self.skills)
        self.skills.import_documents()

    def _examples_from_chat(self) -> None:
        self.notebook.select(self.skills)
        self.skills.show_examples()

    def _report_exception(self, exc_type, exc, tb) -> None:
        detail = "".join(traceback.format_exception(exc_type, exc, tb))
        log.error("Unhandled error in the UI:\n%s", detail)
        try:
            messagebox.showerror(
                "Something went wrong",
                f"{exc_type.__name__}: {exc}\n\nDetails were written to jirabot.log.",
            )
        except tk.TclError:
            pass

    def on_close(self) -> None:
        self.chat.cancel_event.set()
        self.skills.cancel_event.set()
        self.root.destroy()
