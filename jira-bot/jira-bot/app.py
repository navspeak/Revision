"""Jira Bot: start with  python app.py"""
import sys


def main() -> int:
    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        print(
            "Tkinter is not available in this Python.\n"
            "  Windows/macOS: reinstall Python from python.org and keep 'tcl/tk' ticked.\n"
            "  Ubuntu/Debian: sudo apt install python3-tk",
            file=sys.stderr,
        )
        return 1

    from jirabot.config import Settings, default_home
    from jirabot.log import log, setup_logging
    from jirabot.ui.common import AppContext
    from jirabot.ui.main_window import MainWindow

    if sys.platform.startswith("win"):
        try:  # crisp text on high-DPI screens
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:  # noqa: BLE001
            pass

    home = default_home()
    setup_logging(home)
    settings = Settings.load(home)

    root = tk.Tk()
    root.title("Jira Bot")
    root.geometry("1120x780")
    root.minsize(860, 600)
    style = ttk.Style(root)
    if sys.platform.startswith("win") and "vista" in style.theme_names():
        style.theme_use("vista")
    elif "clam" in style.theme_names() and sys.platform.startswith("linux"):
        style.theme_use("clam")

    ctx = AppContext(root, settings)
    MainWindow(root, ctx).pack(fill="both", expand=True)
    log.info("Jira Bot started (home=%s)", home)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
