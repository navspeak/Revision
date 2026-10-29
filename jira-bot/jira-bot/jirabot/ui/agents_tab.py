"""The Agents tab: saved personas that bundle instructions, skills and defaults."""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import List, Optional

from ..importer import ImportProblem, read_document
from ..store import Agent, dump_agent, parse_agent
from .common import AppContext, mono_font, open_folder
from .dialogs import AgentEditor


class AgentsTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, padding=10)
        self.ctx = ctx
        self.names: List[str] = []
        self._build()
        ctx.on_change(self.refresh)
        self.refresh()

    def _build(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        ttk.Label(
            self,
            text=(
                "An agent is a saved persona: instructions for how to triage and report, the skills it uses, "
                "and default values such as your project key. Pick one in the Chat tab."
            ),
            foreground="#5f6368",
            wraplength=900,
            justify="left",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        left = ttk.Frame(self)
        left.grid(row=1, column=0, sticky="ns")
        left.rowconfigure(0, weight=1)
        self.listbox = tk.Listbox(left, width=28, exportselection=False, activestyle="none")
        self.listbox.grid(row=0, column=0, sticky="ns")
        sb = ttk.Scrollbar(left, orient="vertical", command=self.listbox.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=sb.set)
        self.listbox.bind("<<ListboxSelect>>", lambda _e: self.show_selected())
        self.listbox.bind("<Double-Button-1>", lambda _e: self.edit_agent())

        self.preview = scrolledtext.ScrolledText(self, wrap="word", state="disabled", font=mono_font())
        self.preview.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        buttons = ttk.Frame(self)
        buttons.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(buttons, text="New agent", command=self.new_agent).pack(side="left")
        ttk.Button(buttons, text="Edit", command=self.edit_agent).pack(side="left", padx=6)
        ttk.Button(buttons, text="Delete", command=self.delete_agent).pack(side="left")
        ttk.Button(buttons, text="Import agent file...", command=self.import_agent).pack(side="left", padx=6)
        ttk.Button(buttons, text="Open folder", command=lambda: open_folder(self.ctx.settings.agents_dir)).pack(
            side="right")
        self.status = ttk.Label(self, text="", foreground="#5f6368", wraplength=900, justify="left")
        self.status.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))

    def refresh(self) -> None:
        keep = self.selected_name()
        agents = self.ctx.agents.list()
        self.names = [a.name for a in agents]
        self.listbox.delete(0, "end")
        for name in self.names:
            self.listbox.insert("end", name)
        if keep in self.names:
            self.listbox.selection_set(self.names.index(keep))
        elif self.names:
            self.listbox.selection_set(0)
        self.show_selected()
        if self.ctx.agents.errors:
            bad = "; ".join(f"{n} ({why})" for n, why in self.ctx.agents.errors)
            self.status.config(text=f"Some agent files could not be read: {bad}")
        else:
            self.status.config(text=f"{len(self.names)} agent{'s' if len(self.names) != 1 else ''} in {self.ctx.settings.agents_dir}")

    def selected_name(self) -> Optional[str]:
        sel = self.listbox.curselection()
        return self.names[sel[0]] if sel and sel[0] < len(self.names) else None

    def selected_agent(self) -> Optional[Agent]:
        name = self.selected_name()
        return self.ctx.agents.get(name) if name else None

    def show_selected(self) -> None:
        agent = self.selected_agent()
        text = dump_agent(agent) if agent else (
            "No agents yet.\n\nAfter a good triage session, press Save as agent... in the Chat tab, "
            "or create one here with New agent."
        )
        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", text)
        self.preview.config(state="disabled")

    def new_agent(self) -> None:
        if AgentEditor(self, self.ctx, Agent(name="", description="", instructions=""), title="New agent").present():
            self.ctx.changed()

    def edit_agent(self) -> None:
        agent = self.selected_agent()
        if agent and AgentEditor(self, self.ctx, agent, title=f"Edit agent: {agent.name}").present():
            self.ctx.changed()

    def delete_agent(self) -> None:
        name = self.selected_name()
        if name and messagebox.askyesno("Delete agent", f"Delete the agent '{name}'? This cannot be undone.", parent=self):
            self.ctx.agents.delete(name)
            self.ctx.changed()

    def import_agent(self) -> None:
        path = filedialog.askopenfilename(
            parent=self, title="Choose an agent file",
            filetypes=[("Agent files", "*.md *.markdown *.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            doc = read_document(path)
            agent = parse_agent(doc.text, fallback_name="")
        except (ImportProblem, ValueError) as exc:
            messagebox.showerror("Cannot import", str(exc), parent=self)
            return
        agent.path = None
        if AgentEditor(self, self.ctx, agent, title="Import agent", note=f"Imported from {doc.name}. Review and save.").present():
            self.ctx.changed()
