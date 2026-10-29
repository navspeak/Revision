"""Safe subprocess helpers.

- Never uses a shell: arguments are passed as a list, so model output cannot inject commands.
- Supports timeouts and a cancel event so the UI can stop a running command.
- Handles Windows npm launchers (copilot.cmd) by calling node directly, because cmd.exe
  mangles multi-line arguments and characters such as & | < > ^ % and quotes.
"""
from __future__ import annotations

import os
import re
import shlex
import shutil
import signal
import subprocess
import threading
import time
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


class CommandError(Exception):
    """A command could not be run, or it failed."""


class Cancelled(CommandError):
    """The user stopped the command."""


@dataclass
class RunResult:
    argv: list
    returncode: int
    stdout: str
    stderr: str
    note: str = ""
    seconds: float = 0.0

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text or "")


def tail(text: str, limit: int = 1500) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else "..." + text[-limit:]


def split_command(text: str, windows: Optional[bool] = None) -> List[str]:
    """Split a command line from Settings, keeping Windows backslashes intact."""
    windows = (os.name == "nt") if windows is None else windows
    text = (text or "").strip()
    if not text:
        return []
    try:
        parts = shlex.split(text, posix=not windows)
    except ValueError as exc:
        raise CommandError(f"Could not read the command '{text}': {exc}") from exc
    if windows:
        parts = [
            p[1:-1] if len(p) >= 2 and p[0] == p[-1] and p[0] in "\"'" else p for p in parts
        ]
    return parts


# --- Windows launcher handling -------------------------------------------------

_SHIM_RE = re.compile(r'"%~?dp0%?\\(?P<rest>[^"]+?\.(?:cjs|mjs|js))"', re.IGNORECASE)


def _shim_script(shim_path: str) -> Optional[str]:
    """Find the node script that an npm .cmd launcher runs."""
    try:
        with open(shim_path, "r", encoding="utf-8", errors="replace") as fh:
            body = fh.read(20000)
    except OSError:
        return None
    match = _SHIM_RE.search(body)
    if not match:
        return None
    rel = match.group("rest").replace("\\", os.sep)
    script = os.path.join(os.path.dirname(os.path.abspath(shim_path)), rel)
    return script if os.path.exists(script) else None


def resolve_argv(
    argv: Sequence[str],
    windows: Optional[bool] = None,
    which: Callable[[str], Optional[str]] = shutil.which,
) -> Tuple[List[str], str]:
    """Return (argv to execute, note). note is "" normally, "cmd-shim" if we must use a .cmd."""
    windows = (os.name == "nt") if windows is None else windows
    if not argv:
        raise CommandError("No command is configured.")
    exe = argv[0]
    found = which(exe)
    if not found:
        raise CommandError(
            f"Could not find '{exe}'. Check that it is installed and on your PATH, "
            f"or enter its full path in Settings."
        )
    if windows and found.lower().endswith((".cmd", ".bat")):
        script = _shim_script(found)
        if script:
            node = os.path.join(os.path.dirname(found), "node.exe")
            if not os.path.exists(node):
                node = which("node") or ""
            if node:
                return [node, script] + list(argv[1:]), f"{found} -> node {script}"
        return [found] + list(argv[1:]), "cmd-shim"
    return [found] + list(argv[1:]), ""


_CMD_UNSAFE_RE = re.compile(r"[\r\n&|<>^%\"]")


def _kill(proc: subprocess.Popen) -> None:
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                capture_output=True,
                timeout=10,
                creationflags=CREATE_NO_WINDOW,
            )
        else:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def run(
    argv: Sequence[str],
    *,
    input_text: Optional[str] = None,
    timeout: float = 120,
    cancel: Optional[threading.Event] = None,
    env: Optional[dict] = None,
    cwd: Optional[str] = None,
    windows: Optional[bool] = None,
) -> RunResult:
    """Run a command without a shell and return its output.

    input_text is sent to stdin and is never logged or echoed (it may be a token).
    """
    resolved, note = resolve_argv(argv, windows=windows)
    if note == "cmd-shim":
        for arg in resolved[1:]:
            if _CMD_UNSAFE_RE.search(arg):
                raise CommandError(
                    f"'{argv[0]}' is a Windows .cmd launcher, which cannot safely receive text with "
                    "line breaks, quotes or symbols such as & | < > ^ %.\n"
                    "Fix: in Settings, set the command to the real program, for example the full path to "
                    "an .exe, or:  node C:\\path\\to\\npm-loader.js  (the script that your .cmd file runs)."
                )

    full_env = dict(os.environ)
    full_env.update({"NO_COLOR": "1", "TERM": "dumb"})
    if env:
        full_env.update(env)

    kwargs = dict(
        stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        env=full_env,
        cwd=cwd,
    )
    if os.name == "nt":
        kwargs["creationflags"] = CREATE_NO_WINDOW
    else:
        kwargs["start_new_session"] = True

    started = time.monotonic()
    try:
        proc = subprocess.Popen(resolved, **kwargs)
    except FileNotFoundError as exc:
        raise CommandError(f"Could not start '{resolved[0]}': {exc}") from exc
    except OSError as exc:
        raise CommandError(f"Could not start '{resolved[0]}': {exc}") from exc

    deadline = started + timeout
    first = True
    while True:
        try:
            out, err = proc.communicate(input=input_text if first else None, timeout=0.25)
            break
        except subprocess.TimeoutExpired:
            first = False
            if cancel is not None and cancel.is_set():
                _kill(proc)
                proc.communicate()
                raise Cancelled("Stopped.")
            if time.monotonic() > deadline:
                _kill(proc)
                proc.communicate()
                raise CommandError(f"The command took longer than {int(timeout)} seconds and was stopped.")

    return RunResult(
        argv=list(resolved),
        returncode=proc.returncode,
        stdout=strip_ansi(out or ""),
        stderr=strip_ansi(err or ""),
        note=note,
        seconds=time.monotonic() - started,
    )
