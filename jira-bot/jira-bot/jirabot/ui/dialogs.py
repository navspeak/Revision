"""Dialogs: skill editor, agent editor, run-a-skill, import a skill document, examples, text viewer."""
from __future__ import annotations

import copy
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Dict, List, Optional

from .. import importer
from ..examples import example_skills
from ..store import (
    Agent,
    Param,
    Skill,
    one_line,
    parse_param_line,
    valid_name,
    PLACEHOLDER_RE,
)
from .common import AppContext, Modal, mono_font

HINT_COLOR = "#5f6368"


def _text(parent, height: int, mono: bool = False) -> scrolledtext.ScrolledText:
    widget = scrolledtext.ScrolledText(parent, height=height, width=70, wrap="word", undo=True)
    if mono:
        widget.configure(font=mono_font())
    return widget


# ------------------------------------------------------------------ skill editor


class SkillEditor(Modal):
    """Review and edit a skill, then save it. result is the saved Skill, or None."""

    def __init__(self, parent, ctx: AppContext, skill: Skill, title: str = "Skill",
                 allow_skip: bool = False, note: str = ""):
        super().__init__(parent, title, ctx)
        self.original_name = skill.name if skill.path else ""
        body = ttk.Frame(self, padding=12)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        row = 0
        if note:
            ttk.Label(body, text=note, wraplength=640, foreground=HINT_COLOR, justify="left").grid(
                row=row, column=0, columnspan=2, sticky="w", pady=(0, 8))
            row += 1

        self.name_var = tk.StringVar(value=skill.name)
        self.desc_var = tk.StringVar(value=skill.description)
        self.fields_var = tk.StringVar(value=skill.fields)
        self.limit_var = tk.StringVar(value=str(skill.limit) if skill.limit else "")

        ttk.Label(body, text="Name").grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(body, textvariable=self.name_var).grid(row=row, column=1, sticky="ew", pady=3)
        row += 1
        ttk.Label(body, text="Description").grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(body, textvariable=self.desc_var).grid(row=row, column=1, sticky="ew", pady=3)
        row += 1

        ttk.Label(body, text="JQL").grid(row=row, column=0, sticky="nw", pady=3)
        self.jql_text = _text(body, 4, mono=True)
        self.jql_text.insert("1.0", skill.jql)
        self.jql_text.grid(row=row, column=1, sticky="ew", pady=3)
        row += 1
        ttk.Label(body, text="Use {name} for values that change, for example project = {project}",
                  foreground=HINT_COLOR).grid(row=row, column=1, sticky="w")
        row += 1

        ttk.Label(body, text="Parameters").grid(row=row, column=0, sticky="nw", pady=3)
        self.params_text = _text(body, 4, mono=True)
        self.params_text.insert("1.0", "\n".join(p.to_line() for p in skill.parameters))
        self.params_text.grid(row=row, column=1, sticky="ew", pady=3)
        row += 1
        hint = ttk.Frame(body)
        hint.grid(row=row, column=1, sticky="w")
        ttk.Label(hint, text="One per line:  name | description | default value",
                  foreground=HINT_COLOR).pack(side="left")
        ttk.Button(hint, text="Add from JQL", command=self._add_placeholders).pack(side="left", padx=8)
        row += 1

        ttk.Label(body, text="Fields").grid(row=row, column=0, sticky="w", pady=3)
        small = ttk.Frame(body)
        small.grid(row=row, column=1, sticky="ew", pady=3)
        small.columnconfigure(0, weight=1)
        ttk.Entry(small, textvariable=self.fields_var).grid(row=0, column=0, sticky="ew")
        ttk.Label(small, text="Limit").grid(row=0, column=1, padx=(10, 4))
        ttk.Entry(small, textvariable=self.limit_var, width=6).grid(row=0, column=2)
        row += 1
        ttk.Label(body, text="Optional. Example fields: key,summary,status,priority,assignee",
                  foreground=HINT_COLOR).grid(row=row, column=1, sticky="w")
        row += 1

        ttk.Label(body, text="Output").grid(row=row, column=0, sticky="nw", pady=3)
        self.output_text = _text(body, 3)
        self.output_text.insert("1.0", skill.output)
        self.output_text.grid(row=row, column=1, sticky="ew", pady=3)
        row += 1
        ttk.Label(body, text="Notes").grid(row=row, column=0, sticky="nw", pady=3)
        self.notes_text = _text(body, 3)
        self.notes_text.insert("1.0", skill.notes)
        self.notes_text.grid(row=row, column=1, sticky="ew", pady=3)
        row += 1

        buttons = ttk.Frame(body)
        buttons.grid(row=row, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(buttons, text="Save skill", command=self.save).pack(side="right")
        if allow_skip:
            ttk.Button(buttons, text="Skip this one", command=self.cancel).pack(side="right", padx=6)
        else:
            ttk.Button(buttons, text="Cancel", command=self.cancel).pack(side="right", padx=6)

    def _lines_to_params(self) -> List[Param]:
        params = []
        for line in self.params_text.get("1.0", "end").splitlines():
            param = parse_param_line(line)
            if param:
                params.append(param)
        return params

    def _add_placeholders(self) -> None:
        try:
            params = self._lines_to_params()
        except ValueError as exc:
            messagebox.showerror("Parameters", str(exc), parent=self)
            return
        known = {p.name for p in params}
        for name in PLACEHOLDER_RE.findall(self.jql_text.get("1.0", "end")):
            if name not in known:
                params.append(Param(name))
                known.add(name)
        self.params_text.delete("1.0", "end")
        self.params_text.insert("1.0", "\n".join(p.to_line() for p in params))

    def _collect(self) -> Skill:
        name = self.name_var.get().strip()
        if not valid_name(name):
            raise ValueError("The name must use lowercase letters, digits, - and _ (up to 64 characters).")
        jql = one_line(self.jql_text.get("1.0", "end"))
        if not jql:
            raise ValueError("The JQL box is empty.")
        limit_text = self.limit_var.get().strip()
        if limit_text and not limit_text.isdigit():
            raise ValueError("Limit must be a whole number.")
        skill = Skill(
            name=name,
            description=one_line(self.desc_var.get()),
            jql=jql,
            parameters=self._lines_to_params(),
            fields=one_line(self.fields_var.get()),
            limit=int(limit_text) if limit_text else None,
            output=self.output_text.get("1.0", "end").strip(),
            notes=self.notes_text.get("1.0", "end").strip(),
        )
        skill.sync_parameters()
        return skill

    def save(self) -> None:
        try:
            skill = self._collect()
        except ValueError as exc:
            messagebox.showerror("Cannot save", str(exc), parent=self)
            return
        editing_same = bool(self.original_name) and skill.name == self.original_name
        if self.ctx.skills.exists(skill.name) and not editing_same:
            if not messagebox.askyesno(
                "Replace skill?", f"A skill named '{skill.name}' already exists. Replace it?", parent=self
            ):
                return
        try:
            self.ctx.skills.save(skill, overwrite=True)
            if self.original_name and skill.name != self.original_name:
                self.ctx.skills.delete(self.original_name)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Cannot save", str(exc), parent=self)
            return
        self.result = skill
        self.destroy()


# ------------------------------------------------------------------ agent editor


class AgentEditor(Modal):
    def __init__(self, parent, ctx: AppContext, agent: Agent, title: str = "Agent", note: str = ""):
        super().__init__(parent, title, ctx)
        self.original_name = agent.name if agent.path else ""
        body = ttk.Frame(self, padding=12)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        row = 0
        if note:
            ttk.Label(body, text=note, wraplength=620, foreground=HINT_COLOR, justify="left").grid(
                row=row, column=0, columnspan=2, sticky="w", pady=(0, 8))
            row += 1

        self.name_var = tk.StringVar(value=agent.name)
        self.desc_var = tk.StringVar(value=agent.description)
        ttk.Label(body, text="Name").grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(body, textvariable=self.name_var).grid(row=row, column=1, sticky="ew", pady=3)
        row += 1
        ttk.Label(body, text="Description").grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(body, textvariable=self.desc_var).grid(row=row, column=1, sticky="ew", pady=3)
        row += 1
        ttk.Label(body, text="Instructions").grid(row=row, column=0, sticky="nw", pady=3)
        self.instr_text = _text(body, 7)
        self.instr_text.insert("1.0", agent.instructions)
        self.instr_text.grid(row=row, column=1, sticky="ew", pady=3)
        row += 1

        ttk.Label(body, text="Skills").grid(row=row, column=0, sticky="nw", pady=3)
        box = ttk.Frame(body)
        box.grid(row=row, column=1, sticky="ew", pady=3)
        box.columnconfigure(0, weight=1)
        self.skill_names = ctx.skills.names()
        self.skill_list = tk.Listbox(box, selectmode="multiple", height=5, exportselection=False)
        for name in self.skill_names:
            self.skill_list.insert("end", name)
        for index, name in enumerate(self.skill_names):
            if name in agent.skills:
                self.skill_list.selection_set(index)
        self.skill_list.grid(row=0, column=0, sticky="ew")
        row += 1
        ttk.Label(body, text="Leave all unselected to let the agent use every skill.",
                  foreground=HINT_COLOR).grid(row=row, column=1, sticky="w")
        row += 1

        ttk.Label(body, text="Defaults").grid(row=row, column=0, sticky="nw", pady=3)
        self.defaults_text = _text(body, 3, mono=True)
        self.defaults_text.insert("1.0", "\n".join(f"{k} | {v}" for k, v in agent.defaults.items()))
        self.defaults_text.grid(row=row, column=1, sticky="ew", pady=3)
        row += 1
        ttk.Label(body, text="One per line:  parameter | value   (for example: project | ABC)",
                  foreground=HINT_COLOR).grid(row=row, column=1, sticky="w")
        row += 1

        buttons = ttk.Frame(body)
        buttons.grid(row=row, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(buttons, text="Save agent", command=self.save).pack(side="right")
        ttk.Button(buttons, text="Cancel", command=self.cancel).pack(side="right", padx=6)

    def save(self) -> None:
        name = self.name_var.get().strip()
        if not valid_name(name):
            messagebox.showerror("Cannot save", "The name must use lowercase letters, digits, - and _.", parent=self)
            return
        defaults: Dict[str, str] = {}
        for line in self.defaults_text.get("1.0", "end").splitlines():
            if "|" in line:
                key, _, value = line.partition("|")
                if key.strip():
                    defaults[key.strip()] = value.strip()
        chosen = [self.skill_names[i] for i in self.skill_list.curselection()]
        agent = Agent(
            name=name,
            description=one_line(self.desc_var.get()),
            instructions=self.instr_text.get("1.0", "end").strip(),
            skills=chosen,
            defaults=defaults,
        )
        editing_same = bool(self.original_name) and name == self.original_name
        if self.ctx.agents.exists(name) and not editing_same:
            if not messagebox.askyesno("Replace agent?", f"An agent named '{name}' already exists. Replace it?", parent=self):
                return
        try:
            self.ctx.agents.save(agent, overwrite=True)
            if self.original_name and name != self.original_name:
                self.ctx.agents.delete(self.original_name)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Cannot save", str(exc), parent=self)
            return
        self.result = agent
        self.destroy()


# ------------------------------------------------------------------ run a skill


class RunSkillDialog(Modal):
    """Ask for a skill's parameter values. result is a dict of values, or None."""

    def __init__(self, parent, ctx: AppContext, skill: Skill, presets: Optional[Dict[str, str]] = None):
        super().__init__(parent, f"Run skill: {skill.name}", ctx)
        presets = presets or {}
        self.skill = skill
        body = ttk.Frame(self, padding=12)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        row = 0
        if skill.description:
            ttk.Label(body, text=skill.description, wraplength=480, justify="left").grid(
                row=row, column=0, columnspan=2, sticky="w", pady=(0, 6))
            row += 1
        ttk.Label(body, text=skill.jql, font=mono_font(), wraplength=480, foreground=HINT_COLOR,
                  justify="left").grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 10))
        row += 1

        self.vars: Dict[str, tk.StringVar] = {}
        first_entry = None
        for param in skill.parameters:
            label = param.name + (f"  ({param.description})" if param.description else "")
            ttk.Label(body, text=label).grid(row=row, column=0, sticky="w", pady=3, padx=(0, 10))
            var = tk.StringVar(value=presets.get(param.name) or param.default)
            entry = ttk.Entry(body, textvariable=var, width=34)
            entry.grid(row=row, column=1, sticky="ew", pady=3)
            first_entry = first_entry or entry
            self.vars[param.name] = var
            row += 1
        if not skill.parameters:
            ttk.Label(body, text="This skill has no parameters.", foreground=HINT_COLOR).grid(
                row=row, column=0, columnspan=2, sticky="w")
            row += 1

        self.error = ttk.Label(body, text="", foreground="#b00020")
        self.error.grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        buttons = ttk.Frame(body)
        buttons.grid(row=row, column=0, columnspan=2, sticky="e", pady=(8, 0))
        ttk.Button(buttons, text="Prepare query", command=self.ok).pack(side="right")
        ttk.Button(buttons, text="Cancel", command=self.cancel).pack(side="right", padx=6)
        self.bind("<Return>", lambda _e: self.ok())
        if first_entry is not None:
            first_entry.focus_set()

    def ok(self) -> None:
        values = {name: var.get().strip() for name, var in self.vars.items()}
        _, missing = self.skill.render(values)
        if missing:
            self.error.config(text="Please fill in: " + ", ".join(missing))
            return
        self.result = values
        self.destroy()


# ------------------------------------------------------------------ import dialog


class ImportDialog(Modal):
    """Choose skill documents by file picker or by typing a path, or paste text.

    result is {"docs": [Document, ...], "use_copilot": bool}, or None.
    """

    FILETYPES = [
        ("Skill documents", "*.md *.markdown *.txt *.jql *.json *.yaml *.yml *.csv *.docx"),
        ("All files", "*.*"),
    ]

    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, "Import skill document", ctx)
        body = ttk.Frame(self, padding=12)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)

        intro = (
            "Give me a document that describes how you query Jira: a playbook, notes, a saved list of JQL, "
            "or a ready-made skill file. I will turn it into skills for you to review before anything is saved.\n"
            "Supported: .md  .txt  .jql  .json  .yaml  .csv  .docx"
        )
        ttk.Label(body, text=intro, wraplength=560, justify="left").grid(row=0, column=0, sticky="w")

        ttk.Label(body, text="File path (type or paste it, or use Browse)").grid(row=1, column=0, sticky="w", pady=(12, 2))
        path_row = ttk.Frame(body)
        path_row.grid(row=2, column=0, sticky="ew")
        path_row.columnconfigure(0, weight=1)
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_row, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(path_row, text="Browse...", command=self.browse).grid(row=0, column=1, padx=(8, 0))
        ttk.Label(body, text="Several files? Pick them together in Browse, or put each path in quotes.",
                  foreground=HINT_COLOR).grid(row=3, column=0, sticky="w")

        ttk.Label(body, text="Or paste the document text here").grid(row=4, column=0, sticky="w", pady=(12, 2))
        self.paste = _text(body, 8)
        self.paste.grid(row=5, column=0, sticky="nsew")
        body.rowconfigure(5, weight=1)

        self.use_copilot = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            body,
            text="Use Copilot to turn the document into skills (recommended for free-form documents)",
            variable=self.use_copilot,
        ).grid(row=6, column=0, sticky="w", pady=(10, 0))
        ttk.Label(body, text="The document text is sent to Copilot. Untick this to use simple extraction only.",
                  foreground=HINT_COLOR).grid(row=7, column=0, sticky="w")

        buttons = ttk.Frame(body)
        buttons.grid(row=8, column=0, sticky="e", pady=(12, 0))
        ttk.Button(buttons, text="Import", command=self.do_import).pack(side="right")
        ttk.Button(buttons, text="Cancel", command=self.cancel).pack(side="right", padx=6)
        self.path_entry.focus_set()

    def browse(self) -> None:
        paths = filedialog.askopenfilenames(parent=self, title="Choose skill documents", filetypes=self.FILETYPES)
        if paths:
            self.path_var.set(" ".join(f'"{p}"' for p in paths))

    def do_import(self) -> None:
        docs = []
        problems: List[str] = []
        for raw in importer.parse_path_list(self.path_var.get()):
            try:
                docs.append(importer.read_document(raw))
            except importer.ImportProblem as exc:
                problems.append(str(exc))
        pasted = self.paste.get("1.0", "end").strip()
        if pasted:
            try:
                docs.append(importer.document_from_text(pasted))
            except importer.ImportProblem as exc:
                problems.append(str(exc))

        if problems:
            text = "\n\n".join(problems)
            if not docs:
                messagebox.showerror("Cannot import", text, parent=self)
                return
            if not messagebox.askyesno("Some files were skipped", text + "\n\nContinue with the others?", parent=self):
                return
        if not docs:
            messagebox.showinfo("Nothing to import", "Choose a file, type a path, or paste some text.", parent=self)
            return
        self.result = {"docs": docs, "use_copilot": bool(self.use_copilot.get())}
        self.destroy()


# ------------------------------------------------------------------ examples


class ExamplesDialog(Modal):
    """Browse example JQL patterns. result is a Skill copy to edit, or None."""

    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, "Example JQL patterns", ctx)
        self.examples = example_skills()
        body = ttk.Frame(self, padding=12)
        body.pack(fill="both", expand=True)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(1, weight=1)
        ttk.Label(
            body,
            text="Starting points only. Nothing is saved until you review it and press Save skill.",
            foreground=HINT_COLOR,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        self.listbox = tk.Listbox(body, width=26, height=12, exportselection=False)
        for ex in self.examples:
            self.listbox.insert("end", ex.name)
        self.listbox.grid(row=1, column=0, sticky="ns")
        self.preview = scrolledtext.ScrolledText(body, width=64, height=12, wrap="word", state="disabled")
        self.preview.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        buttons = ttk.Frame(body)
        buttons.grid(row=2, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(buttons, text="Create skill from selected...", command=self.choose).pack(side="right")
        ttk.Button(buttons, text="Close", command=self.cancel).pack(side="right", padx=6)
        self.listbox.bind("<<ListboxSelect>>", lambda _e: self.show())
        self.listbox.bind("<Double-Button-1>", lambda _e: self.choose())
        self.listbox.selection_set(0)
        self.show()

    def selected(self) -> Optional[Skill]:
        sel = self.listbox.curselection()
        return self.examples[sel[0]] if sel else None

    def show(self) -> None:
        skill = self.selected()
        self.preview.config(state="normal")
        self.preview.delete("1.0", "end")
        if skill:
            params = "\n".join("  " + p.to_line() for p in skill.parameters) or "  (none)"
            self.preview.insert(
                "1.0",
                f"{skill.description}\n\nJQL\n{skill.jql}\n\nParameters (name | description | default)\n{params}\n",
            )
        self.preview.config(state="disabled")

    def choose(self) -> None:
        skill = self.selected()
        if skill:
            self.result = copy.deepcopy(skill)
            self.destroy()


# ------------------------------------------------------------------ text viewer


class TextViewer(Modal):
    def __init__(self, parent, title: str, text: str):
        super().__init__(parent, title)
        body = ttk.Frame(self, padding=10)
        body.pack(fill="both", expand=True)
        box = scrolledtext.ScrolledText(body, width=100, height=26, wrap="none", font=mono_font())
        box.pack(fill="both", expand=True)
        box.insert("1.0", text)
        box.config(state="disabled")
        buttons = ttk.Frame(body)
        buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(buttons, text="Close", command=self.cancel).pack(side="right")
        ttk.Button(buttons, text="Copy", command=lambda: self._copy(text)).pack(side="right", padx=6)

    def _copy(self, text: str) -> None:
        self.clipboard_clear()
        self.clipboard_append(text)
