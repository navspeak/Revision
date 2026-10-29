"""The Chat tab: ask in plain English, review the JQL, run it, save what worked."""
from __future__ import annotations

import csv
import re
import shutil
import threading
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Dict, List, Optional

from .. import jira, prompts, protocol, skillgen
from ..jira import SearchResult
from ..proc import Cancelled, split_command
from ..session import ChatSession
from ..store import Agent, Skill
from .common import AppContext, hint_for_error, mono_font
from .dialogs import AgentEditor, RunSkillDialog, SkillEditor, TextViewer

NO_AGENT = "(no agent)"
SAVE_SKILL_RE = re.compile(
    r"^\s*(?:please\s+)?save\s+(?:this|that|it)?\s*(?:as\s+)?(?:a\s+)?skill(?:\s+(?:called|named))?\s*[:\-]?\s*(?P<name>.*)$",
    re.I,
)


class ChatTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent)
        self.ctx = ctx
        self.session = ChatSession()
        self.busy = False
        self.cancel_event = threading.Event()
        self.result: Optional[SearchResult] = None
        self.pending_fields = ""
        self.pending_skill = ""
        self.skill_names: List[str] = []
        self.work_visible = False
        self._sized_for: Optional[str] = None
        self._build()
        ctx.on_change(self.refresh_lists)
        self.refresh_lists()
        self.show_welcome()

    # ------------------------------------------------------------------ layout

    def _build(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        bar = ttk.Frame(self, padding=(8, 6))
        bar.grid(row=0, column=0, sticky="ew")
        ttk.Button(bar, text="New chat", command=self.new_chat).pack(side="left")
        ttk.Button(bar, text="Save as skill...", command=self.save_as_skill).pack(side="left", padx=(6, 0))
        ttk.Button(bar, text="Save as agent...", command=self.save_as_agent).pack(side="left", padx=(6, 0))
        self.stop_btn = ttk.Button(bar, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=(6, 0))
        self.status = ttk.Label(bar, text="", foreground="#5f6368")
        self.status.pack(side="left", padx=12)
        self.agent_var = tk.StringVar(value=NO_AGENT)
        self.agent_box = ttk.Combobox(bar, textvariable=self.agent_var, state="readonly", width=24)
        self.agent_box.pack(side="right")
        ttk.Label(bar, text="Agent:").pack(side="right", padx=(0, 6))
        self.agent_box.bind("<<ComboboxSelected>>", self._agent_changed)

        panes = ttk.PanedWindow(self, orient="horizontal")
        panes.grid(row=1, column=0, sticky="nsew", padx=8)

        # ---- left: skills
        left = ttk.Frame(panes, padding=(0, 0, 8, 0))
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)
        ttk.Label(left, text="Skills").grid(row=0, column=0, sticky="w")
        self.skill_list = tk.Listbox(left, width=26, exportselection=False, activestyle="none")
        self.skill_list.grid(row=1, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(left, orient="vertical", command=self.skill_list.yview)
        scroll.grid(row=1, column=1, sticky="ns")
        self.skill_list.config(yscrollcommand=scroll.set)
        self.skill_list.bind("<Double-Button-1>", lambda _e: self.run_selected_skill())
        ttk.Button(left, text="Run selected skill...", command=self.run_selected_skill).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        teach = ttk.Menubutton(left, text="Teach me...")
        menu = tk.Menu(teach, tearoff=False)
        menu.add_command(label="Import skill document...", command=lambda: self.ctx.actions.get("import", lambda: None)())
        menu.add_command(label="Browse example JQL...", command=lambda: self.ctx.actions.get("examples", lambda: None)())
        teach["menu"] = menu
        teach.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        panes.add(left, weight=0)

        # ---- right: transcript above, work area below
        self.right = ttk.PanedWindow(panes, orient="vertical")
        panes.add(self.right, weight=1)

        tframe = ttk.Frame(self.right)
        tframe.rowconfigure(0, weight=1)
        tframe.columnconfigure(0, weight=1)
        self.transcript = tk.Text(tframe, wrap="word", state="disabled", padx=10, pady=8, height=12,
                                  borderwidth=1, relief="solid", highlightthickness=0, cursor="arrow")
        tscroll = ttk.Scrollbar(tframe, orient="vertical", command=self.transcript.yview)
        self.transcript.config(yscrollcommand=tscroll.set)
        self.transcript.grid(row=0, column=0, sticky="nsew")
        tscroll.grid(row=0, column=1, sticky="ns")
        self._configure_tags()
        self.right.add(tframe, weight=2)

        self.work = ttk.Frame(self.right)
        self.work.columnconfigure(0, weight=1)
        self.work.rowconfigure(1, weight=1)
        self._build_work_area()

        # ---- input
        entry = ttk.Frame(self, padding=(8, 6))
        entry.grid(row=2, column=0, sticky="ew")
        entry.columnconfigure(0, weight=1)
        self.input = tk.Text(entry, height=3, wrap="word", undo=True)
        self.input.grid(row=0, column=0, sticky="ew")
        self.input.bind("<Return>", self._on_return)
        self.send_btn = ttk.Button(entry, text="Send", command=self.on_send)
        self.send_btn.grid(row=0, column=1, sticky="ns", padx=(8, 0))
        ttk.Label(entry, text="Enter to send, Shift+Enter for a new line", foreground="#5f6368").grid(
            row=1, column=0, sticky="w")
        self.input.focus_set()

    def _configure_tags(self) -> None:
        t = self.transcript
        t.tag_configure("who", font=("TkDefaultFont", 9, "bold"), foreground="#3c4043", spacing1=4)
        t.tag_configure("user", background="#e8f0fe", lmargin1=6, lmargin2=6, rmargin=6)
        t.tag_configure("bot", background="#f6f6f6", lmargin1=6, lmargin2=6, rmargin=6)
        t.tag_configure("note", foreground="#5f6368", font=("TkDefaultFont", 9, "italic"))
        t.tag_configure("error", foreground="#b00020", lmargin1=6, lmargin2=6)
        t.tag_configure("code", font=mono_font(), background="#fff8e1", lmargin1=14, lmargin2=14)

    def _build_work_area(self) -> None:
        self.proposal = ttk.LabelFrame(self.work, text="Proposed JQL (edit it if you like, then run)", padding=6)
        self.proposal.columnconfigure(0, weight=1)
        self.jql_text = tk.Text(self.proposal, height=2, wrap="word", font=mono_font())
        self.jql_text.grid(row=0, column=0, columnspan=6, sticky="ew")
        self.run_btn = ttk.Button(self.proposal, text="Run query", command=self.run_query)
        self.run_btn.grid(row=1, column=1, pady=(6, 0), padx=(0, 6))
        ttk.Button(self.proposal, text="Dismiss", command=self.hide_proposal).grid(row=1, column=2, pady=(6, 0))
        ttk.Label(self.proposal, text="Max rows").grid(row=1, column=3, pady=(6, 0), padx=(14, 4))
        self.limit_var = tk.StringVar(value=str(self.ctx.settings.default_limit))
        ttk.Entry(self.proposal, textvariable=self.limit_var, width=6).grid(row=1, column=4, pady=(6, 0))
        self.proposal.grid(row=0, column=0, sticky="ew")
        self.proposal.grid_remove()

        self.results = ttk.LabelFrame(self.work, text="Results", padding=6)
        self.results.columnconfigure(0, weight=1)
        self.results.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(self.results, show="headings", height=5)
        ys = ttk.Scrollbar(self.results, orient="vertical", command=self.tree.yview)
        xs = ttk.Scrollbar(self.results, orient="horizontal", command=self.tree.xview)
        self.tree.config(yscrollcommand=ys.set, xscrollcommand=xs.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        ys.grid(row=0, column=1, sticky="ns")
        xs.grid(row=1, column=0, sticky="ew")
        self.tree.bind("<Double-Button-1>", self._open_issue)
        actions = ttk.Frame(self.results)
        actions.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))
        self.count_label = ttk.Label(actions, text="")
        self.count_label.pack(side="left")
        self.summ_btn = ttk.Button(actions, text="Summarise results", command=self.summarise)
        self.summ_btn.pack(side="right")
        ttk.Button(actions, text="Export CSV...", command=self.export_csv).pack(side="right", padx=6)
        ttk.Button(actions, text="Raw output...", command=self.show_raw).pack(side="right")
        self.results.grid(row=1, column=0, sticky="nsew", pady=(6, 0))
        self.results.grid_remove()

    def _show_work(self) -> None:
        if not self.work_visible:
            self.right.add(self.work, weight=3)
            self.work_visible = True
            self._sized_for = None

    def _hide_work(self) -> None:
        if self.work_visible:
            self.right.forget(self.work)
            self.work_visible = False
            self._sized_for = None

    def _size_work(self, for_results: bool) -> None:
        """Give the work area enough room: a little for a proposal, most of the pane for results."""
        wanted = "results" if for_results else "proposal"
        if self._sized_for == wanted or (wanted == "proposal" and self._sized_for == "results"):
            return
        self._sized_for = wanted
        fraction = 0.32 if for_results else 0.60

        def apply() -> None:
            try:
                self.right.update_idletasks()
                total = self.right.winfo_height()
                if total > 250:
                    self.right.sashpos(0, int(total * fraction))
                self.update_idletasks()  # let the transcript take its new size first
                self.transcript.yview_moveto(1.0)
            except tk.TclError:
                pass

        self.after(60, apply)

    # --------------------------------------------------------------- transcript

    def append(self, who: str, text: str, tag: str) -> None:
        t = self.transcript
        t.config(state="normal")
        t.insert("end", who + "\n", ("who", tag))
        t.insert("end", text.strip() + "\n\n", (tag,))
        t.config(state="disabled")
        t.see("end")

    def append_note(self, text: str) -> None:
        t = self.transcript
        t.config(state="normal")
        t.insert("end", text.strip() + "\n\n", ("note",))
        t.config(state="disabled")
        t.see("end")

    def append_code(self, text: str) -> None:
        t = self.transcript
        t.config(state="normal")
        t.insert("end", text.strip() + "\n\n", ("code",))
        t.config(state="disabled")
        t.see("end")

    def clear_transcript(self) -> None:
        self.transcript.config(state="normal")
        self.transcript.delete("1.0", "end")
        self.transcript.config(state="disabled")

    # ------------------------------------------------------------------ welcome

    def setup_warnings(self) -> List[str]:
        s = self.ctx.settings
        warnings: List[str] = []
        for label, command in (("Copilot CLI", s.copilot_command), ("Atlassian CLI (acli)", s.acli_command)):
            try:
                parts = split_command(command)
                found = bool(parts) and shutil.which(parts[0]) is not None
            except Exception:  # noqa: BLE001
                found = False
            if not found:
                warnings.append(f"{label} was not found. Open the Settings tab to set its location.")
        if not s.jira_site:
            warnings.append("Jira is not set up yet. Open the Settings tab, enter your site and email, and log in.")
        return warnings

    def show_welcome(self) -> None:
        skills = self.available_skills()
        if not skills:
            text = (
                "Hi. I am your Jira bot, and I have not been taught any Jira skills yet, so I start from a blank slate.\n\n"
                "Ways to start:\n"
                "  1. Ask in plain English, for example: open bugs in project ABC from the last 2 weeks. "
                "I will work out the JQL, ask you questions if I need to, and show you the query before anything runs.\n"
                "  2. Use Teach me... (left) to import a skill document: upload a file or give me its path.\n"
                "  3. Use Teach me... to browse example JQL patterns and turn the ones you like into skills.\n\n"
                "When a session goes well, press Save as skill... and I will remember it next time."
            )
        else:
            lines = "\n".join(f"  - {s.name}: {s.description or '(no description)'}" for s in skills[:12])
            more = f"\n  ...and {len(skills) - 12} more" if len(skills) > 12 else ""
            text = (
                f"Welcome back. I know {len(skills)} skill{'s' if len(skills) != 1 else ''}:\n{lines}{more}\n\n"
                "Double-click a skill on the left to run it, or just describe what you need and I will suggest one if it fits."
            )
        self.append("Jira Bot", text, "bot")
        for warning in self.setup_warnings():
            self.append_note(warning)

    # ------------------------------------------------------------------- lists

    def current_agent(self) -> Optional[Agent]:
        name = self.agent_var.get()
        if not name or name == NO_AGENT:
            return None
        return self.ctx.agents.get(name)

    def available_skills(self) -> List[Skill]:
        skills = self.ctx.skills.list()
        agent = self.current_agent()
        if agent and agent.skills:
            skills = [s for s in skills if s.name in agent.skills]
        return skills

    def refresh_lists(self) -> None:
        agents = self.ctx.agents.names()
        self.agent_box.config(values=[NO_AGENT] + agents)
        if self.agent_var.get() not in [NO_AGENT] + agents:
            self.agent_var.set(NO_AGENT)
        self.skill_names = [s.name for s in self.available_skills()]
        self.skill_list.delete(0, "end")
        for name in self.skill_names:
            self.skill_list.insert("end", name)
        self.limit_var.set(str(self.ctx.settings.default_limit))

    def _agent_changed(self, _event=None) -> None:
        self.refresh_lists()
        agent = self.current_agent()
        self.append_note(f"Agent '{agent.name}' is active." if agent else "No agent selected.")

    # ------------------------------------------------------------------- state

    def set_busy(self, busy: bool, text: str = "") -> None:
        self.busy = busy
        state = "disabled" if busy else "normal"
        self.send_btn.config(state=state)
        self.run_btn.config(state=state)
        self.summ_btn.config(state=state)
        self.stop_btn.config(state="normal" if busy else "disabled")
        self.status.config(text=text)

    def stop(self) -> None:
        self.cancel_event.set()
        self.status.config(text="Stopping...")

    def _new_cancel(self) -> threading.Event:
        self.cancel_event = threading.Event()
        return self.cancel_event

    def new_chat(self) -> None:
        if self.busy:
            self.stop()
        self.session.reset()
        self.result = None
        self.clear_transcript()
        self.hide_proposal()
        self.results.grid_remove()
        self._hide_work()
        self.show_welcome()

    # -------------------------------------------------------------------- send

    def _on_return(self, event) -> Optional[str]:
        if event.state & 0x0001:  # Shift+Enter inserts a newline
            return None
        self.on_send()
        return "break"

    def on_send(self) -> None:
        if self.busy:
            return
        text = self.input.get("1.0", "end").strip()
        if not text:
            return
        self.input.delete("1.0", "end")
        self.append("You", text, "user")
        intent = SAVE_SKILL_RE.match(text)
        if intent:
            self.save_as_skill(intent.group("name").strip())
            return
        self.session.add_user(text)
        self.hide_proposal()
        self.ask_model()

    def ask_model(self) -> None:
        prompt = prompts.chat_prompt(
            self.session.turns, self.available_skills(), self.current_agent(), self.ctx.settings.max_prompt_chars
        )
        cancel = self._new_cancel()
        self.set_busy(True, "Asking Copilot...")
        self.ctx.asyncer.run(lambda: self.ctx.llm.ask(prompt, cancel), self._on_reply, self._on_error)

    def _on_reply(self, raw) -> None:
        self.set_busy(False)
        reply = protocol.parse_reply(str(raw))
        message = reply.message or "(Copilot sent no message.)"
        self.session.add_assistant(message + (f"\nJQL: {reply.jql}" if reply.jql else ""))
        self.append("Jira Bot", message, "bot")

        skill = None
        if reply.skill:
            skill = next((s for s in self.available_skills() if s.name == reply.skill), None)
        if skill is not None:
            agent = self.current_agent()
            values = dict(agent.defaults) if agent else {}
            values.update(reply.params)
            jql, missing = skill.render(values)
            if missing:
                self.append_note(f"The skill '{skill.name}' still needs: {', '.join(missing)}.")
                self.run_skill_dialog(skill.name, presets=values)
                return
            self.show_proposal(jql, skill.fields or reply.fields, skill.limit, skill.name)
            return
        if reply.jql:
            self.show_proposal(reply.jql, reply.fields, None, "")
        elif not reply.structured:
            self.append_note("Copilot did not use the expected format, so its reply is shown as plain text.")

    def _on_error(self, exc: Exception) -> None:
        self.set_busy(False)
        if isinstance(exc, Cancelled):
            self.append_note("Stopped.")
            return
        message = str(exc) or exc.__class__.__name__
        hint = hint_for_error(message)
        self.append("Jira Bot", "That did not work.\n" + message + (f"\n\n{hint}" if hint else ""), "error")

    # ---------------------------------------------------------------- proposal

    def show_proposal(self, jql: str, fields: str, limit: Optional[int], skill_name: str) -> None:
        self.pending_fields = fields or ""
        self.pending_skill = skill_name
        self._show_work()
        self._size_work(for_results=self.results.winfo_manager() != "")
        self.proposal.grid()
        self.jql_text.delete("1.0", "end")
        self.jql_text.insert("1.0", jql)
        self.limit_var.set(str(limit or self.ctx.settings.default_limit))
        label = f"Using skill '{skill_name}'. " if skill_name else ""
        self.status.config(text=label + "Review the JQL, then press Run query.")

    def hide_proposal(self) -> None:
        self.proposal.grid_remove()
        if not self.results.winfo_ismapped() and not self.result:
            self._hide_work()

    def run_query(self) -> None:
        if self.busy:
            return
        try:
            jql = jira.clean_jql(self.jql_text.get("1.0", "end"))
        except ValueError as exc:
            messagebox.showwarning("Cannot run", str(exc), parent=self)
            return
        limit_text = self.limit_var.get().strip()
        limit = int(limit_text) if limit_text.isdigit() and int(limit_text) > 0 else self.ctx.settings.default_limit
        fields = self.pending_fields
        self.session.last_jql = jql
        cancel = self._new_cancel()
        self.set_busy(True, "Running in Jira...")
        self.ctx.asyncer.run(
            lambda: self.ctx.acli.search(jql, fields, limit, cancel), self._on_results, self._on_error
        )

    def _on_results(self, result) -> None:
        self.set_busy(False)
        res: SearchResult = result  # type: ignore[assignment]
        self.result = res
        self._fill_tree(res)
        self._show_work()
        self.results.grid()
        self._size_work(for_results=True)
        count = len(res.rows)
        self.count_label.config(text=f"{count} result{'s' if count != 1 else ''}. Double-click a row to open it in Jira.")
        self.append_note(f"Ran: {res.jql}\n{count} result{'s' if count != 1 else ''}.")
        if self.ctx.settings.share_results:
            table = prompts.rows_to_text(res.columns, res.rows, max_rows=25, max_chars=3500)
            self.session.add_note(
                f"The app ran this JQL: {res.jql}\nIt returned {count} rows. First rows:\n{table}"
            )
        else:
            self.session.add_note(
                f"The app ran this JQL: {res.jql}\nIt returned {count} rows. "
                "The row contents are not shared with you (the user turned that off)."
            )
        if count == 0:
            self.append(
                "Jira Bot",
                "No results. Tell me if I should widen the query (for example a longer time window, or fewer filters).",
                "bot",
            )
            if res.raw.strip() and res.raw.strip() not in ("[]", "{}"):
                self.append_note("The output could not be read as a table. Use Raw output... to see what ACLI returned.")

    def _fill_tree(self, res: SearchResult) -> None:
        self.tree.delete(*self.tree.get_children())
        columns = res.columns or ["(no columns)"]
        self.tree.config(columns=columns)
        for name in columns:
            width = 90 if name == "key" else 380 if name == "summary" else 120
            self.tree.heading(name, text=name.title() if name != "key" else "Key")
            self.tree.column(name, width=width, minwidth=60, stretch=name == "summary")
        for row in res.rows:
            self.tree.insert("", "end", values=[row.get(c, "") for c in columns])

    def _open_issue(self, _event) -> None:
        site = self.ctx.settings.site_host
        if not (site and self.result and "key" in self.result.columns):
            return
        item = self.tree.focus()
        if not item:
            return
        index = self.result.columns.index("key")
        key = self.tree.item(item, "values")[index]
        if key:
            webbrowser.open(f"https://{site}/browse/{key}")

    def show_raw(self) -> None:
        if self.result:
            TextViewer(self, "Raw ACLI output", self.result.raw or "(empty)").present()

    def export_csv(self) -> None:
        if not self.result or not self.result.rows:
            messagebox.showinfo("Export", "There are no results to export.", parent=self)
            return
        path = filedialog.asksaveasfilename(
            parent=self, defaultextension=".csv", filetypes=[("CSV", "*.csv")], initialfile="jira-results.csv"
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as fh:
                writer = csv.writer(fh)
                writer.writerow(self.result.columns)
                for row in self.result.rows:
                    writer.writerow([row.get(c, "") for c in self.result.columns])
        except OSError as exc:
            messagebox.showerror("Export", str(exc), parent=self)
            return
        self.append_note(f"Saved {len(self.result.rows)} rows to {path}")

    def summarise(self) -> None:
        if self.busy or not self.result:
            return
        if not self.result.rows:
            messagebox.showinfo("Summarise", "There are no rows to summarise.", parent=self)
            return
        if not self.ctx.settings.share_results and not messagebox.askyesno(
            "Send results to Copilot?",
            "Sharing result rows with Copilot is turned off in Settings.\n\n"
            "Summarising needs to send the first rows of these results to Copilot, just this once. Continue?",
            parent=self,
        ):
            return
        res = self.result
        prompt = prompts.summary_prompt(
            self.session.latest_user_text() or "", res.jql, res.columns, res.rows,
            self.current_agent(), self.ctx.settings.max_prompt_chars,
        )
        cancel = self._new_cancel()
        self.set_busy(True, "Summarising...")

        def done(raw) -> None:
            self.set_busy(False)
            message = protocol.parse_reply(str(raw)).message
            self.session.add_assistant(message)
            self.append("Jira Bot", message, "bot")

        self.ctx.asyncer.run(lambda: self.ctx.llm.ask(prompt, cancel), done, self._on_error)

    # ---------------------------------------------------------- run a saved skill

    def run_selected_skill(self) -> None:
        selection = self.skill_list.curselection()
        if not selection:
            messagebox.showinfo("Run skill", "Pick a skill in the list first.", parent=self)
            return
        self.run_skill_dialog(self.skill_names[selection[0]])

    def run_skill_dialog(self, name: str, presets: Optional[Dict[str, str]] = None) -> None:
        skill = self.ctx.skills.get(name)
        if skill is None:
            messagebox.showwarning("Run skill", f"The skill '{name}' no longer exists.", parent=self)
            return
        values: Dict[str, str] = {}
        agent = self.current_agent()
        if agent:
            values.update(agent.defaults)
        values.update(presets or {})
        chosen = RunSkillDialog(self, self.ctx, skill, values).present()
        if chosen is None:
            return
        jql, missing = skill.render(chosen)
        if missing:
            return
        self.append("You", f"Run skill: {skill.name}", "user")
        self.session.add_user(f"Run the saved skill '{skill.name}'.")
        self.session.add_assistant(f"Using skill {skill.name}.\nJQL: {jql}")
        self.show_proposal(jql, skill.fields, skill.limit, skill.name)

    # ------------------------------------------------------ save as skill / agent

    def save_as_skill(self, suggested_name: str = "") -> None:
        if self.busy:
            return
        if not self.session.has_user_turn() and not self.session.last_jql:
            messagebox.showinfo("Save as skill", "Have a short conversation first, then save what worked.", parent=self)
            return
        turns = list(self.session.turns)
        last_jql = self.session.last_jql
        existing = self.ctx.skills.names()
        cancel = self._new_cancel()
        self.set_busy(True, "Drafting a skill from this conversation...")

        def work():
            return skillgen.skills_from_chat(self.ctx.llm, turns, last_jql, existing, suggested_name, cancel)

        def ok(drafts) -> None:
            self.set_busy(False)
            drafts = list(drafts)  # type: ignore[arg-type]
            note = "Drafted from your conversation. Check the JQL and parameters, then save."
            if not drafts and last_jql:
                drafts = [skillgen.fallback_skill(last_jql, suggested_name)]
                note = "Copilot did not return a skill, so this is a plain starting point from the last query."
            if not drafts:
                self.append("Jira Bot", "I could not draft a skill. Run a query first, then try again.", "error")
                return
            self._review_skills(drafts, note)

        def err(exc: Exception) -> None:
            self.set_busy(False)
            if isinstance(exc, Cancelled):
                self.append_note("Stopped.")
                return
            if last_jql:
                first = (str(exc).strip().splitlines() or ["unknown error"])[0]
                self._review_skills(
                    [skillgen.fallback_skill(last_jql, suggested_name)],
                    f"Copilot could not draft this ({first}), so here is a plain starting point from the last query.",
                )
            else:
                self._on_error(exc)

        self.ctx.asyncer.run(work, ok, err)

    def _review_skills(self, drafts: List[Skill], note: str) -> None:
        saved = 0
        for index, draft in enumerate(drafts, start=1):
            title = "Save as skill" if len(drafts) == 1 else f"Save as skill ({index} of {len(drafts)})"
            result = SkillEditor(self, self.ctx, draft, title=title, allow_skip=len(drafts) > 1, note=note).present()
            if result is not None:
                saved += 1
                self.append_note(f"Saved skill '{result.name}'.")
        if saved:
            self.ctx.changed()

    def save_as_agent(self) -> None:
        if self.busy:
            return
        if not self.session.has_user_turn():
            messagebox.showinfo("Save as agent", "Have a short conversation first, then save what worked.", parent=self)
            return
        turns = list(self.session.turns)
        skills = self.ctx.skills.list()
        cancel = self._new_cancel()
        self.set_busy(True, "Drafting an agent from this conversation...")

        def ok(agent) -> None:
            self.set_busy(False)
            note = "Drafted from your conversation. Check the instructions and skills, then save."
            if agent is None:
                agent = Agent(name="", description="", instructions="")
                note = "Copilot did not return an agent, so fill in the details yourself."
            self._review_agent(agent, note)

        def err(exc: Exception) -> None:
            self.set_busy(False)
            if isinstance(exc, Cancelled):
                self.append_note("Stopped.")
                return
            first = (str(exc).strip().splitlines() or ["unknown error"])[0]
            self._review_agent(Agent(name="", description="", instructions=""),
                               f"Copilot could not draft this ({first}). Fill in the details yourself.")

        self.ctx.asyncer.run(lambda: skillgen.agent_from_chat(self.ctx.llm, turns, skills, "", cancel), ok, err)

    def _review_agent(self, agent: Agent, note: str) -> None:
        result = AgentEditor(self, self.ctx, agent, title="Save as agent", note=note).present()
        if result is not None:
            self.append_note(f"Saved agent '{result.name}'. Pick it from the Agent list at the top right.")
            self.ctx.changed()
