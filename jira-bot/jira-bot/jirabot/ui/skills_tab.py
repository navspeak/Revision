"""The Skills tab: list, edit, delete, import documents, browse examples."""
from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from typing import List, Optional

from .. import skillgen
from ..importer import Document
from ..proc import Cancelled
from ..store import Skill, dump_skill
from .common import AppContext, mono_font, open_folder
from .dialogs import ExamplesDialog, ImportDialog, SkillEditor


class SkillsTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, padding=10)
        self.ctx = ctx
        self.names: List[str] = []
        self.doc_queue: List[Document] = []
        self.use_copilot = True
        self.saved_count = 0
        self.total_docs = 0
        self.importing = False
        self.cancel_event = threading.Event()
        self._build()
        ctx.on_change(self.refresh)
        self.refresh()

    def _build(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        intro = ttk.Label(
            self,
            text=(
                "Skills are saved JQL recipes. Teach the bot a new one by importing a document, "
                "browsing examples, or saving a good chat session."
            ),
            foreground="#5f6368",
        )
        intro.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        left = ttk.Frame(self)
        left.grid(row=1, column=0, sticky="ns")
        left.rowconfigure(0, weight=1)
        self.listbox = tk.Listbox(left, width=28, exportselection=False, activestyle="none")
        self.listbox.grid(row=0, column=0, sticky="ns")
        sb = ttk.Scrollbar(left, orient="vertical", command=self.listbox.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=sb.set)
        self.listbox.bind("<<ListboxSelect>>", lambda _e: self.show_selected())
        self.listbox.bind("<Double-Button-1>", lambda _e: self.edit_skill())

        self.preview = scrolledtext.ScrolledText(self, wrap="word", state="disabled", font=mono_font())
        self.preview.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        buttons = ttk.Frame(self)
        buttons.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(buttons, text="Import document...", command=self.import_documents).pack(side="left")
        ttk.Button(buttons, text="Examples...", command=self.show_examples).pack(side="left", padx=6)
        ttk.Button(buttons, text="New skill", command=self.new_skill).pack(side="left")
        ttk.Button(buttons, text="Edit", command=self.edit_skill).pack(side="left", padx=6)
        ttk.Button(buttons, text="Delete", command=self.delete_skill).pack(side="left")
        ttk.Button(buttons, text="Open folder", command=lambda: open_folder(self.ctx.settings.skills_dir)).pack(
            side="right")
        self.stop_btn = ttk.Button(buttons, text="Stop", command=self.stop_import, state="disabled")
        self.stop_btn.pack(side="right", padx=6)

        self.status = ttk.Label(self, text="", foreground="#5f6368", wraplength=900, justify="left")
        self.status.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))

    # ------------------------------------------------------------------- list

    def refresh(self) -> None:
        keep = self.selected_name()
        skills = self.ctx.skills.list()
        self.names = [s.name for s in skills]
        self.listbox.delete(0, "end")
        for name in self.names:
            self.listbox.insert("end", name)
        if keep in self.names:
            self.listbox.selection_set(self.names.index(keep))
        elif self.names:
            self.listbox.selection_set(0)
        self.show_selected()
        if self.ctx.skills.errors and not self.importing:
            bad = "; ".join(f"{n} ({why})" for n, why in self.ctx.skills.errors)
            self.status.config(text=f"Some skill files could not be read: {bad}")
        elif not self.importing:
            self.status.config(text=f"{len(self.names)} skill{'s' if len(self.names) != 1 else ''} in {self.ctx.settings.skills_dir}")

    def selected_name(self) -> Optional[str]:
        sel = self.listbox.curselection()
        return self.names[sel[0]] if sel and sel[0] < len(self.names) else None

    def selected_skill(self) -> Optional[Skill]:
        name = self.selected_name()
        return self.ctx.skills.get(name) if name else None

    def show_selected(self) -> None:
        skill = self.selected_skill()
        text = dump_skill(skill) if skill else (
            "No skills yet.\n\nStart with Import document... (upload a file or enter its path), "
            "Examples..., or ask a question in the Chat tab and press Save as skill..."
        )
        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", text)
        self.preview.config(state="disabled")

    # ---------------------------------------------------------- simple actions

    def new_skill(self) -> None:
        result = SkillEditor(self, self.ctx, Skill(name="", jql=""), title="New skill").present()
        if result:
            self.ctx.changed()

    def edit_skill(self) -> None:
        skill = self.selected_skill()
        if skill is None:
            return
        if SkillEditor(self, self.ctx, skill, title=f"Edit skill: {skill.name}").present():
            self.ctx.changed()

    def delete_skill(self) -> None:
        name = self.selected_name()
        if not name:
            return
        if messagebox.askyesno("Delete skill", f"Delete the skill '{name}'? This cannot be undone.", parent=self):
            self.ctx.skills.delete(name)
            self.ctx.changed()

    def show_examples(self) -> None:
        draft = ExamplesDialog(self, self.ctx).present()
        if draft is not None:
            result = SkillEditor(
                self, self.ctx, draft, title="New skill from example",
                note="Adjust the JQL, parameters and defaults to match how your team works.",
            ).present()
            if result:
                self.ctx.changed()

    # ----------------------------------------------------------------- import

    def import_documents(self) -> None:
        if self.importing:
            messagebox.showinfo("Import", "An import is already running.", parent=self)
            return
        choice = ImportDialog(self, self.ctx).present()
        if choice:
            self.process_documents(choice["docs"], choice["use_copilot"])

    def process_documents(self, docs: List[Document], use_copilot: bool) -> None:
        self.doc_queue = list(docs)
        self.use_copilot = use_copilot
        self.saved_count = 0
        self.total_docs = len(docs)
        self.importing = True
        self._next_document()

    def _next_document(self) -> None:
        if not self.doc_queue:
            self.importing = False
            self.stop_btn.config(state="disabled")
            self.ctx.changed()
            self.status.config(
                text=f"Import finished: {self.saved_count} skill{'s' if self.saved_count != 1 else ''} saved "
                     f"from {self.total_docs} document{'s' if self.total_docs != 1 else ''}."
            )
            return
        doc = self.doc_queue.pop(0)
        position = self.total_docs - len(self.doc_queue)
        self.status.config(text=f"Reading {doc.name} ({position} of {self.total_docs})...")
        self.stop_btn.config(state="normal")
        existing = self.ctx.skills.names()
        llm = self.ctx.llm if self.use_copilot else None
        self.cancel_event = threading.Event()
        cancel = self.cancel_event
        self.ctx.asyncer.run(
            lambda: skillgen.skills_from_document(llm, doc, existing, cancel),
            lambda result: self._review(doc, result),
            lambda exc: self._failed(doc, exc),
        )

    def _review(self, doc: Document, result) -> None:
        drafts, notes = result
        self.stop_btn.config(state="disabled")
        total = len(drafts)
        for index, draft in enumerate(drafts, start=1):
            note = f"From {doc.name} (skill {index} of {total}). " + " ".join(notes)
            saved = SkillEditor(
                self, self.ctx, draft, title=f"Review skill: {doc.name}", allow_skip=True, note=note
            ).present()
            if saved is not None:
                self.saved_count += 1
                self.ctx.changed()
        self.after(50, self._next_document)

    def _failed(self, doc: Document, exc: Exception) -> None:
        self.stop_btn.config(state="disabled")
        if isinstance(exc, Cancelled):
            self.doc_queue.clear()
            self.status.config(text="Import stopped.")
            self.importing = False
            return
        messagebox.showwarning(f"Could not import {doc.name}", str(exc), parent=self)
        self.after(50, self._next_document)

    def stop_import(self) -> None:
        self.cancel_event.set()
        self.doc_queue.clear()
