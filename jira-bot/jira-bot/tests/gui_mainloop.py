"""GUI test under the real Tk mainloop (the way the app actually runs).

    xvfb-run -a -s "-screen 0 1400x900x24" python tests/gui_mainloop.py [screenshot_dir]

The scenario is a generator: each `yield` is a condition to wait for, checked from root.after().
"""
import faulthandler
import subprocess
import sys
import time
import traceback
from pathlib import Path
from tkinter import messagebox

import helpers  # noqa: F401
from helpers import make_settings

import tkinter as tk
from tkinter import ttk

from jirabot.ui.common import AppContext
from jirabot.ui.main_window import MainWindow

SHOTS = Path(sys.argv[1]) if len(sys.argv) > 1 else None
failures = []


def check(cond, label):
    print(("PASS  " if cond else "FAIL  ") + label, flush=True)
    if not cond:
        failures.append(label)


def main():
    faulthandler.dump_traceback_later(90, exit=True)
    seen = []
    messagebox.showerror = lambda t, m, **k: seen.append(("error", m))
    messagebox.showwarning = lambda t, m, **k: seen.append(("warning", m))
    messagebox.showinfo = lambda t, m, **k: seen.append(("info", m))
    messagebox.askyesno = lambda t, m, **k: (seen.append(("askyesno", m)), True)[1]

    settings = make_settings()
    settings.save()
    root = tk.Tk()
    root.geometry("1180x800+0+0")
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    ctx = AppContext(root, settings)
    win = MainWindow(root, ctx)
    win.pack(fill="both", expand=True)
    chat = win.chat

    def shot(name):
        if SHOTS:
            SHOTS.mkdir(parents=True, exist_ok=True)
            subprocess.run(["import", "-window", "root", str(SHOTS / f"{name}.png")], check=False)

    def send(text):
        chat.input.insert("1.0", text)
        chat.on_send()

    def drive_modal(fn):
        def poll():
            m = ctx.modal
            if m is not None and m.winfo_exists():
                fn(m)
            else:
                root.after(50, poll)
        root.after(100, poll)

    def scenario():
        yield lambda: True
        send("open bugs in ABC from the last 14 days")
        yield lambda: not chat.busy and chat.proposal.winfo_ismapped()
        check("created >= -14d" in chat.jql_text.get("1.0", "end"), "M1 proposal arrives through the real mainloop")
        chat.run_query()
        yield lambda: not chat.busy and len(chat.tree.get_children()) == 3
        check(len(chat.tree.get_children()) == 3, "M2 results arrive through the real mainloop")
        yield lambda: True
        time.sleep(0.2)
        root.update()
        tree_h = chat.tree.winfo_height()
        check(tree_h >= 70, f"M3 results table has room to show rows (height {tree_h}px)")
        check(chat.transcript.bbox("end-2c") is not None, "M3b latest message is visible in the transcript")
        shot("11_results_after_fix")

        drive_modal(lambda m: m.save())
        send("save this as a skill called weekly-bugs")
        yield lambda: not chat.busy and ctx.modal is None and "weekly-bugs" in ctx.skills.names()
        check("weekly-bugs" in ctx.skills.names(), "M4 save-as-skill works under mainloop")
        check(ctx.modal is None and not chat.busy, "M5 UI is idle afterwards")

        # type a path into the import dialog and import a ready-made skill file
        p = Path(settings.home) / "ready.md"
        p.write_text("---\nname: ready-made\ndescription: d\n---\n\n## JQL\n\nproject = ABC AND priority = High\n", encoding="utf-8")

        def imp(m):
            m.use_copilot.set(False)
            m.path_var.set(f'"{p}"')
            m.do_import()

        drive_modal(imp)
        win.skills.import_documents()
        yield lambda: ctx.modal is not None and hasattr(ctx.modal, "name_var")
        ctx.modal.save()
        yield lambda: not win.skills.importing
        check("ready-made" in ctx.skills.names(), "M6 file-path import works under mainloop")
        check(not [s for s in seen if s[0] in ("error", "askyesno")], f"M7 no unexpected dialogs {seen}")

    gen = scenario()
    state = {"cond": None}

    def tick():
        try:
            if state["cond"] is None or state["cond"]():
                state["cond"] = next(gen)
        except StopIteration:
            root.destroy()
            return
        except Exception:
            traceback.print_exc()
            failures.append("scenario crashed")
            root.destroy()
            return
        root.after(50, tick)

    root.after(300, tick)
    root.mainloop()
    print()
    if failures:
        print(f"{len(failures)} FAILED: {failures}")
        return 1
    print("ALL MAINLOOP CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
