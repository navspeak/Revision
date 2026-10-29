"""End-to-end GUI smoke test. Run under a virtual display:

    xvfb-run -a -s "-screen 0 1400x900x24" python tests/gui_smoke.py [screenshot_dir]

Uses the fake copilot and acli from tests/fakes, so no network or real tools are needed.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import zipfile
from pathlib import Path

import helpers  # noqa: F401
from helpers import make_settings

import tkinter as tk
from tkinter import ttk

from jirabot.ui.common import AppContext
from jirabot.ui.main_window import MainWindow

SHOTS = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if SHOTS:
    SHOTS.mkdir(parents=True, exist_ok=True)

failures = []


def check(cond, label):
    print(("PASS  " if cond else "FAIL  ") + label, flush=True)
    if not cond:
        failures.append(label)


def pump(root, seconds=0.2):
    end = time.time() + seconds
    while time.time() < end:
        root.update()
        time.sleep(0.01)


def wait_for(root, cond, timeout=15, label=""):
    end = time.time() + timeout
    while time.time() < end:
        root.update()
        try:
            if cond():
                return True
        except tk.TclError:
            pass
        time.sleep(0.02)
    print(f"      (timed out waiting for {label})", flush=True)
    return False


def shot(root, name):
    if not SHOTS:
        return
    pump(root, 0.3)
    subprocess.run(["import", "-window", "root", str(SHOTS / f"{name}.png")], check=False)


def drive_modal(root, ctx, fn, delay=200):
    """Run fn(modal) as soon as a modal dialog is open."""
    def poll():
        m = ctx.modal
        if m is not None and m.winfo_exists():
            try:
                fn(m)
            except Exception:
                traceback.print_exc()
                failures.append("modal driver crashed")
                m.destroy()
        else:
            root.after(50, poll)
    root.after(delay, poll)


def transcript(chat):
    return chat.transcript.get("1.0", "end")


def send(root, chat, text):
    chat.input.delete("1.0", "end")
    chat.input.insert("1.0", text)
    chat.on_send()


def idle(root, chat, timeout=20):
    return wait_for(root, lambda: not chat.busy, timeout, "chat to finish")


def main():
    import faulthandler
    from tkinter import messagebox

    faulthandler.dump_traceback_later(150, exit=True)  # never hang forever
    dialogs_seen = []
    # Any unexpected message box is recorded and auto-answered so the test cannot block on it.
    messagebox.showerror = lambda title, msg, **kw: dialogs_seen.append(("error", title, msg))
    messagebox.showwarning = lambda title, msg, **kw: dialogs_seen.append(("warning", title, msg))
    messagebox.showinfo = lambda title, msg, **kw: dialogs_seen.append(("info", title, msg))
    messagebox.askyesno = lambda title, msg, **kw: (dialogs_seen.append(("askyesno", title, msg)), True)[1]

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
    chat, skills_tab, agents_tab, settings_tab = win.chat, win.skills, win.agents, win.settings
    pump(root, 0.5)

    # ---------------------------------------------------------------- A. blank state
    t = transcript(chat)
    check("not been taught any Jira skills" in t, "A1 blank-state welcome is shown")
    check("Teach me" in t and "import a skill document" in t, "A2 welcome mentions importing a document")
    check(chat.skill_list.size() == 0, "A3 skill list starts empty")
    shot(root, "01_blank_state")

    # ---------------------------------------------------------------- B/C. clarifying question, then JQL
    send(root, chat, "help me triage the bugs")
    idle(root, chat)
    check("Which project key" in transcript(chat), "B1 bot asks a clarifying question")
    check(not chat.proposal.winfo_ismapped(), "B2 no JQL proposed yet")

    send(root, chat, "ABC, last 14 days")
    idle(root, chat)
    pump(root, 0.3)
    jql = chat.jql_text.get("1.0", "end").strip()
    check("project = ABC" in jql and "created >= -14d" in jql, "C1 JQL proposal appears and is editable")
    check(chat.proposal.winfo_ismapped(), "C2 proposal panel is visible")
    shot(root, "02_proposal")

    # ---------------------------------------------------------------- D. run
    chat.run_query()
    idle(root, chat)
    pump(root, 0.3)
    rows = chat.tree.get_children()
    check(len(rows) == 3, "D1 results table has 3 rows")
    check(list(chat.tree["columns"])[0] == "key", "D2 key column comes first")
    first = chat.tree.item(rows[0], "values")
    check(first[0] == "ABC-101", "D3 first row is ABC-101")
    shot(root, "03_results")

    # ---------------------------------------------------------------- E. summarise
    chat.summarise()
    idle(root, chat)
    check("unassigned" in transcript(chat), "E1 summary is shown")

    # ---------------------------------------------------------------- F. save as skill from chat
    def fill_skill_editor(m):
        check(m.name_var.get() == "bug-triage-weekly", "F1 editor prefilled with the requested name")
        check("{project}" in m.jql_text.get("1.0", "end"), "F2 editor JQL uses a {project} placeholder")
        check("project" in m.params_text.get("1.0", "end"), "F3 editor lists the project parameter")
        shot(root, "04_skill_editor")
        m.save()

    drive_modal(root, ctx, fill_skill_editor)
    send(root, chat, "save this as a skill called bug-triage-weekly")
    idle(root, chat)
    wait_for(root, lambda: ctx.modal is None, 10, "editor to close")
    check((settings.skills_dir / "bug-triage-weekly.md").exists(), "F4 skill file written to skills/")
    check("bug-triage-weekly" in chat.skill_names, "F5 chat skill list refreshed")
    saved_text = (settings.skills_dir / "bug-triage-weekly.md").read_text()
    check(saved_text.startswith("---\nname: bug-triage-weekly"), "F6 saved file has readable header")

    # ---------------------------------------------------------------- G. examples -> skill -> suggested in chat
    def pick_example(m):
        m.listbox.selection_clear(0, "end")
        m.listbox.selection_set(0)  # open-bugs
        m.choose()

    def finish_example(m):
        check(m.name_var.get() == "open-bugs", "G1 example prefilled in editor")
        lines = m.params_text.get("1.0", "end").replace("project | Jira project key | ", "project | Jira project key | ABC")
        m.params_text.delete("1.0", "end")
        m.params_text.insert("1.0", lines.strip())
        m.save()

    drive_modal(root, ctx, pick_example)
    root.after(600, lambda: drive_modal(root, ctx, finish_example, delay=50))
    skills_tab.show_examples()
    wait_for(root, lambda: ctx.modal is None, 10, "example editor to close")
    check((settings.skills_dir / "open-bugs.md").exists(), "G2 example saved as a skill")
    check("project = {project}" in (settings.skills_dir / "open-bugs.md").read_text(), "G3 placeholder kept in file")

    chat.new_chat()
    pump(root, 0.3)
    check("Welcome back" in transcript(chat) and "open-bugs" in transcript(chat), "G4 welcome lists saved skills")
    shot(root, "05_welcome_back")
    send(root, chat, "show me the open bugs")
    idle(root, chat)
    pump(root, 0.3)
    check("skill called open-bugs" in transcript(chat), "G5 bot suggests the saved skill")
    jql = chat.jql_text.get("1.0", "end").strip()
    check(jql.startswith("project = ABC AND issuetype = Bug"), "G6 skill JQL rendered with project default")
    check(chat.pending_skill == "open-bugs", "G7 proposal remembers it came from a skill")

    # run skill from the list with the dialog
    chat.skill_list.selection_clear(0, "end")
    chat.skill_list.selection_set(chat.skill_names.index("open-bugs"))

    def fill_run(m):
        m.vars["project"].set("XYZ")
        m.ok()

    drive_modal(root, ctx, fill_run)
    chat.run_selected_skill()
    pump(root, 0.3)
    check("project = XYZ" in chat.jql_text.get("1.0", "end"), "G8 Run skill dialog fills parameters")

    # ---------------------------------------------------------------- H. import documents (file path + browse-less)
    tmp = Path(tempfile.mkdtemp(prefix="jirabot-docs-"))
    md = tmp / "My Triage Playbook.md"
    md.write_text(
        "# Triage playbook\n\nEvery Monday I run:\n\n```\nproject = ABC AND issuetype = Bug AND statusCategory != Done\n```\n\n"
        "And for old items: `project = ABC AND updated <= -30d`\n",
        encoding="utf-8",
    )
    docx = tmp / "release notes.docx"
    body = "".join(
        f"<w:p><w:r><w:t>{p}</w:t></w:r></w:p>"
        for p in ["Release checklist", "JQL: project = ABC AND fixVersion = 2.4 AND statusCategory != Done"]
    )
    with zipfile.ZipFile(docx, "w") as zf:
        zf.writestr(
            "word/document.xml",
            '<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f"<w:body>{body}</w:body></w:document>",
        )

    saved_names = []

    def import_dialog(m):
        check(True, "H1 import dialog opened")
        shot(root, "06_import_dialog")
        m.path_var.set(f'"{md}" "{docx}"')  # typed path(s), quotes as Windows "Copy as path" gives them
        m.do_import()

    def review_editor(m):
        saved_names.append(m.name_var.get())
        m.save()

    def next_editor(_=None):
        drive_modal(root, ctx, review_editor, delay=30)

    drive_modal(root, ctx, import_dialog)
    # after the dialog closes, 3 editors are expected (2 JQLs in the md, 1 in the docx)
    for i in range(3):
        root.after(800 + i * 900, next_editor)
    skills_tab.import_documents()
    wait_for(root, lambda: not skills_tab.importing, 40, "import to finish")
    pump(root, 0.5)
    check(len(saved_names) == 3, f"H2 three skills were offered for review (got {saved_names})")
    check(skills_tab.saved_count == 3, "H3 three skills saved from two documents")
    check("doc-skill-1" in ctx.skills.names(), "H4 imported skills are in the store")
    shot(root, "07_skills_tab")

    # H5: native skill file imports with no Copilot call at all
    native = tmp / "native.md"
    native.write_text(
        "---\nname: native-one\ndescription: Native skill\nparameters:\n  - project | Key | ABC\n---\n\n## JQL\n\nproject = {project} AND priority = High\n",
        encoding="utf-8",
    )
    calls_log = tmp / "calls.log"
    os.environ["FAKE_COPILOT_LOG"] = str(calls_log)

    def import_native(m):
        m.use_copilot.set(False)
        m.path_var.set(str(native))
        m.do_import()

    drive_modal(root, ctx, import_native)
    root.after(900, lambda: drive_modal(root, ctx, lambda m: m.save(), delay=30))
    skills_tab.import_documents()
    wait_for(root, lambda: not skills_tab.importing, 20, "native import")
    del os.environ["FAKE_COPILOT_LOG"]
    check("native-one" in ctx.skills.names(), "H5 ready-made skill file imported")
    check(not calls_log.exists(), "H6 no Copilot call was needed for a ready-made skill file")

    # H7: bad path gives a friendly error and keeps the dialog open
    def bad_path(m):
        m.path_var.set(str(tmp / "nope.md"))
        m.do_import()
        check(any(k == "error" and "cannot find" in msg for k, _t, msg in dialogs_seen),
              "H7 missing file path shows a friendly error")
        check(m.winfo_exists(), "H8 dialog stays open after an error")
        m.cancel()

    drive_modal(root, ctx, bad_path)
    skills_tab.import_documents()

    # ---------------------------------------------------------------- I. agents
    chat.new_chat()
    send(root, chat, "open bugs in ABC")
    idle(root, chat)

    def fill_agent(m):
        check(m.name_var.get() == "triage-assistant", "I1 agent drafted from the conversation")
        names = list(m.skill_names)
        m.skill_list.selection_clear(0, "end")
        m.skill_list.selection_set(names.index("open-bugs"))
        shot(root, "08_agent_editor")
        m.save()

    drive_modal(root, ctx, fill_agent)
    chat.save_as_agent()
    idle(root, chat)
    wait_for(root, lambda: ctx.modal is None, 10, "agent editor to close")
    check((settings.agents_dir / "triage-assistant.md").exists(), "I2 agent file written to agents/")
    chat.agent_var.set("triage-assistant")
    chat._agent_changed()
    check(chat.skill_names == ["open-bugs"], "I3 agent limits the skills shown in Chat")
    pump(root, 0.2)
    agents_tab.refresh()
    check("triage-assistant" in agents_tab.names, "I4 Agents tab lists it")

    # ---------------------------------------------------------------- J. settings tab
    settings_tab.test_copilot()
    wait_for(root, lambda: "OK" in settings_tab.output.get("1.0", "end"), 15, "copilot test")
    check("answered" in settings_tab.output.get("1.0", "end"), "J1 Test Copilot reports a reply")
    settings_tab.test_acli()
    wait_for(root, lambda: "Test search" in settings_tab.output.get("1.0", "end"), 15, "acli test")
    out = settings_tab.output.get("1.0", "end")
    check("Authenticated" in out and "Test search worked" in out, "J2 Check login runs status and a test search")
    settings_tab.token_var.set("super-secret-token")
    settings_tab.login()
    wait_for(root, lambda: "Logged in" in settings_tab.output.get("1.0", "end"), 15, "login")
    check("Logged in" in settings_tab.output.get("1.0", "end"), "J3 login succeeds")
    check(settings_tab.token_var.get() == "", "J4 token field is cleared after login")
    check("super-secret-token" not in settings.config_path.read_text(), "J5 token is not written to config")
    win.notebook.select(settings_tab)
    shot(root, "09_settings")

    # ---------------------------------------------------------------- K. error paths
    chat.agent_var.set("(no agent)")
    chat._agent_changed()
    os.environ["FAKE_COPILOT_FAIL"] = "1"
    send(root, chat, "bugs in ABC please")
    idle(root, chat)
    del os.environ["FAKE_COPILOT_FAIL"]
    check("simulated failure" in transcript(chat), "K1 Copilot failure is shown to the user")
    check(not chat.busy and str(chat.send_btn["state"]) == "normal", "K2 UI recovers after an error")

    send(root, chat, "bugs in ABC")
    idle(root, chat)
    os.environ["FAKE_ACLI_FAIL"] = "1"
    chat.run_query()
    idle(root, chat)
    del os.environ["FAKE_ACLI_FAIL"]
    check("unbounded" in transcript(chat).lower() and "Add a project" in transcript(chat), "K3 ACLI error shown with a hint")

    os.environ["FAKE_ACLI_EMPTY"] = "1"
    chat.run_query()
    idle(root, chat)
    del os.environ["FAKE_ACLI_EMPTY"]
    check("No results" in transcript(chat), "K4 empty result set is handled")

    # stop button: slow copilot cancelled
    settings.copilot_command = f'"{sys.executable}" -c "import time; time.sleep(30)"'
    send(root, chat, "bugs in ABC")
    pump(root, 0.6)
    check(chat.busy, "K5 busy while Copilot is thinking")
    chat.stop()
    ok = idle(root, chat, 10)
    check(ok and "Stopped." in transcript(chat), "K6 Stop cancels the running command")

    shot(root, "10_final_chat")
    unexpected = [d for d in dialogs_seen if d[0] in ("askyesno",) or (d[0] == "error" and "cannot find" not in d[2])]
    check(not unexpected, f"Z1 no unexpected message boxes ({unexpected})")
    root.destroy()
    print()
    if failures:
        print(f"{len(failures)} FAILED:")
        for f in failures:
            print("  -", f)
        return 1
    print("ALL GUI CHECKS PASSED")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
