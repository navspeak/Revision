#!/usr/bin/env bash
# Starts the Jira Bot web edition (Streamlit) on macOS or Linux.
# The first run creates a private .venv next to this file and installs requirements-web.txt into it.
set -e
cd "$(dirname "$0")"
if [ ! -x .venv/bin/python ]; then
  echo "First run: creating .venv and installing the web packages (a few minutes)..."
  python3 -m venv .venv
  .venv/bin/python -m pip install --upgrade pip >/dev/null
  .venv/bin/python -m pip install -r requirements-web.txt
fi
echo "Jira Bot is starting. Your browser should open at http://localhost:8501  (Ctrl+C here to stop it)"
exec .venv/bin/python -m streamlit run web_app.py "$@"
