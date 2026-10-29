"""The Settings tab: Jira site and login (through ACLI), Copilot and ACLI commands."""
from __future__ import annotations

import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from ..config import normalize_site
from ..proc import tail
from .common import AppContext, mono_font


class SettingsTab(ttk.Frame):
    def __init__(self, parent, ctx: AppContext):
        super().__init__(parent, padding=14)
        self.ctx = ctx
        self._build()

    def _build(self) -> None:
        s = self.ctx.settings
        self.columnconfigure(1, weight=1)
        self.rowconfigure(99, weight=1)
        self.vars = {
            "jira_site": tk.StringVar(value=s.jira_site),
            "jira_email": tk.StringVar(value=s.jira_email),
            "copilot_command": tk.StringVar(value=s.copilot_command),
            "copilot_model": tk.StringVar(value=s.copilot_model),
            "copilot_extra_args": tk.StringVar(value=s.copilot_extra_args),
            "copilot_timeout": tk.StringVar(value=str(s.copilot_timeout)),
            "max_prompt_chars": tk.StringVar(value=str(s.max_prompt_chars)),
            "acli_command": tk.StringVar(value=s.acli_command),
            "acli_timeout": tk.StringVar(value=str(s.acli_timeout)),
            "default_limit": tk.StringVar(value=str(s.default_limit)),
            "default_fields": tk.StringVar(value=s.default_fields),
        }
        self.token_var = tk.StringVar()
        self.share_var = tk.BooleanVar(value=s.share_results)

        row = 0

        def heading(text: str) -> None:
            nonlocal row
            ttk.Label(self, text=text, font=("TkDefaultFont", 10, "bold")).grid(
                row=row, column=0, columnspan=3, sticky="w", pady=(10 if row else 0, 4))
            row += 1

        def field(label: str, key: str, hint: str = "", show: str = "", var=None) -> None:
            nonlocal row
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", pady=2, padx=(0, 12))
            entry = ttk.Entry(self, textvariable=var or self.vars[key], show=show)
            entry.grid(row=row, column=1, sticky="ew", pady=2)
            if hint:
                ttk.Label(self, text=hint, foreground="#5f6368").grid(row=row, column=2, sticky="w", padx=(10, 0))
            row += 1

        heading("Jira (through the Atlassian CLI)")
        field("Site", "jira_site", "for example  mycompany.atlassian.net")
        field("Email", "jira_email")
        field("API token", "", "used once to log in; this app never saves it (leave empty to use JIRABOT_JIRA_API_TOKEN from .env)", show="*", var=self.token_var)
        buttons = ttk.Frame(self)
        buttons.grid(row=row, column=1, sticky="w", pady=(4, 0))
        ttk.Button(buttons, text="Log in to Jira", command=self.login).pack(side="left")
        ttk.Button(buttons, text="Check login", command=self.test_acli).pack(side="left", padx=6)
        row += 1

        heading("Atlassian CLI")
        field("ACLI command", "acli_command", "name on your PATH, or a full path")
        field("Timeout (seconds)", "acli_timeout")
        field("Default max rows", "default_limit")
        field("Default fields", "default_fields", "optional, for example  key,summary,status,assignee")

        heading("Copilot CLI")
        field("Copilot command", "copilot_command", "name on your PATH, a full path, or  node path\\to\\loader.js")
        field("Model", "copilot_model", "optional, passed as --model")
        field("Extra arguments", "copilot_extra_args", "optional, added to every call")
        field("Timeout (seconds)", "copilot_timeout")
        field("Max prompt size", "max_prompt_chars", "characters; lower it if long chats fail on Windows")
        ttk.Checkbutton(
            self,
            text="Send the first rows of query results to Copilot, so follow-up questions and summaries can use them",
            variable=self.share_var,
        ).grid(row=row, column=1, columnspan=2, sticky="w", pady=(4, 0))
        row += 1
        buttons2 = ttk.Frame(self)
        buttons2.grid(row=row, column=1, sticky="w", pady=(4, 0))
        ttk.Button(buttons2, text="Test Copilot", command=self.test_copilot).pack(side="left")
        row += 1

        bar = ttk.Frame(self)
        bar.grid(row=row, column=0, columnspan=3, sticky="w", pady=(14, 4))
        ttk.Button(bar, text="Save settings", command=self.save).pack(side="left")
        self.saved_label = ttk.Label(bar, text="", foreground="#1e7e34")
        self.saved_label.pack(side="left", padx=10)
        row += 1

        self.output = scrolledtext.ScrolledText(self, height=9, wrap="word", font=mono_font(), state="disabled")
        self.output.grid(row=99, column=0, columnspan=3, sticky="nsew", pady=(6, 0))

    # ----------------------------------------------------------------- helpers

    def log(self, text: str, clear: bool = False) -> None:
        self.output.config(state="normal")
        if clear:
            self.output.delete("1.0", "end")
        self.output.insert("end", text.rstrip() + "\n")
        self.output.see("end")
        self.output.config(state="disabled")

    def _int(self, key: str, minimum: int, label: str) -> int:
        text = self.vars[key].get().strip()
        if not text.isdigit() or int(text) < minimum:
            raise ValueError(f"{label} must be a whole number of at least {minimum}.")
        return int(text)

    def save(self, quiet: bool = False) -> bool:
        s = self.ctx.settings
        try:
            timeout_c = self._int("copilot_timeout", 5, "Copilot timeout")
            timeout_a = self._int("acli_timeout", 5, "ACLI timeout")
            limit = self._int("default_limit", 1, "Default max rows")
            max_prompt = self._int("max_prompt_chars", 2000, "Max prompt size")
        except ValueError as exc:
            messagebox.showerror("Settings", str(exc), parent=self)
            return False
        if not self.vars["copilot_command"].get().strip() or not self.vars["acli_command"].get().strip():
            messagebox.showerror("Settings", "The Copilot and ACLI commands cannot be empty.", parent=self)
            return False
        s.jira_site = normalize_site(self.vars["jira_site"].get())
        self.vars["jira_site"].set(s.jira_site)
        s.jira_email = self.vars["jira_email"].get().strip()
        s.copilot_command = self.vars["copilot_command"].get().strip()
        s.copilot_model = self.vars["copilot_model"].get().strip()
        s.copilot_extra_args = self.vars["copilot_extra_args"].get().strip()
        s.copilot_timeout = timeout_c
        s.max_prompt_chars = max_prompt
        s.acli_command = self.vars["acli_command"].get().strip()
        s.acli_timeout = timeout_a
        s.default_limit = limit
        s.default_fields = self.vars["default_fields"].get().strip()
        s.share_results = bool(self.share_var.get())
        try:
            s.save()
        except OSError as exc:
            messagebox.showerror("Settings", f"Could not save: {exc}", parent=self)
            return False
        if not quiet:
            self.saved_label.config(text="Saved.")
            self.after(2500, lambda: self.saved_label.config(text=""))
        self.ctx.changed()
        return True

    # ------------------------------------------------------------------- tests

    def test_copilot(self) -> None:
        if not self.save(quiet=True):
            return
        self.log("Testing Copilot...", clear=True)
        self.log("Program: " + self.ctx.llm.describe())

        def work():
            started = time.monotonic()
            text = self.ctx.llm.ask("Reply with the single word OK.")
            return text, time.monotonic() - started

        def ok(result) -> None:
            text, secs = result
            self.log(f"Copilot answered in {secs:.1f}s:\n{tail(text, 800)}")
            self.log("If the answer above is clean text, the bot can use it. If it contains extra lines, that is fine too.")

        self.ctx.asyncer.run(work, ok, lambda exc: self.log(f"Failed:\n{exc}"))

    def test_acli(self) -> None:
        if not self.save(quiet=True):
            return
        self.log("Checking ACLI...", clear=True)

        def work():
            status = self.ctx.acli.auth_status()
            lines = [f"auth status (exit {status.returncode}):", tail(status.stdout or status.stderr, 800)]
            try:
                res = self.ctx.acli.search("created >= -30d ORDER BY created DESC", limit=1)
                lines.append(f"Test search worked: {len(res.rows)} row(s) returned.")
            except Exception as exc:  # noqa: BLE001
                lines.append(f"Test search failed:\n{exc}")
            return "\n".join(lines)

        self.ctx.asyncer.run(work, lambda text: self.log(str(text)), lambda exc: self.log(f"Failed:\n{exc}"))

    def login(self) -> None:
        if not self.save(quiet=True):
            return
        s = self.ctx.settings
        token = self.token_var.get() or s.env_token
        if not s.site_host or not s.jira_email or not token.strip():
            messagebox.showinfo("Log in", "Enter the site, your email and an API token first.", parent=self)
            return
        self.log("Logging in...", clear=True)
        self.token_var.set("")  # never keep the token around

        def work():
            return self.ctx.acli.login(s.site_host, s.jira_email, token)

        def ok(result) -> None:
            body = tail(result.stdout or result.stderr, 800)
            if result.ok:
                self.log(f"Logged in.\n{body}")
            else:
                self.log(f"Login failed (exit {result.returncode}):\n{body}")

        self.ctx.asyncer.run(work, ok, lambda exc: self.log(f"Failed:\n{exc}"))
