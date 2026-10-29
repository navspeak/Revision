"""Calls GitHub Copilot CLI in non-interactive mode:  copilot -p "<prompt>"

Copilot is never given permission to use tools: the app only asks it for text.
"""
from __future__ import annotations

import threading
from typing import Optional

from .config import Settings
from .log import debug_enabled, log
from .proc import CommandError, resolve_argv, run, split_command, tail


class CopilotClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def build_argv(self, prompt: str) -> list:
        s = self.settings
        argv = split_command(s.copilot_command) + ["-p", prompt]
        if s.copilot_model.strip():
            argv += ["--model", s.copilot_model.strip()]
        if s.copilot_extra_args.strip():
            argv += split_command(s.copilot_extra_args)
        return argv

    def describe(self) -> str:
        """Explain which program will be started (used by the Settings test button)."""
        try:
            argv, note = resolve_argv(split_command(self.settings.copilot_command))
        except CommandError as exc:
            return str(exc)
        if note == "cmd-shim":
            return f"{argv[0]} (a .cmd launcher: long or multi-line prompts will be refused; see README)"
        if note:
            return f"{note}"
        return argv[0]

    def ask(self, prompt: str, cancel: Optional[threading.Event] = None) -> str:
        argv = self.build_argv(prompt)
        result = run(argv, timeout=self.settings.copilot_timeout, cancel=cancel)
        log.info(
            "copilot call: prompt=%d chars rc=%s %.1fs stdout=%d chars",
            len(prompt), result.returncode, result.seconds, len(result.stdout),
        )
        if debug_enabled():
            log.debug("PROMPT:\n%s\nREPLY:\n%s\nSTDERR:\n%s", prompt, result.stdout, result.stderr)
        if result.returncode != 0:
            detail = tail(result.stderr or result.stdout)
            raise CommandError(f"Copilot exited with code {result.returncode}.\n{detail}")
        text = result.stdout.strip()
        if not text:
            raise CommandError("Copilot returned no text." + (f"\n{tail(result.stderr)}" if result.stderr.strip() else ""))
        return text
