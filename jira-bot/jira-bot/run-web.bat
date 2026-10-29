@echo off
REM Starts the Jira Bot web edition (Streamlit).
REM The first run creates a private .venv next to this file and installs requirements-web.txt into it.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo First run: creating .venv and installing the web packages. This takes a few minutes...
  where py >nul 2>nul && (py -3 -m venv .venv) || (python -m venv .venv)
  if errorlevel 1 goto :fail
  ".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
  ".venv\Scripts\python.exe" -m pip install -r requirements-web.txt
  if errorlevel 1 goto :fail
)
echo Jira Bot is starting. Your browser should open at http://localhost:8501  (close this window to stop it)
".venv\Scripts\python.exe" -m streamlit run web_app.py %*
if errorlevel 1 goto :fail
goto :eof
:fail
echo.
echo Something went wrong. See the message above, or the Troubleshooting section of README.md.
pause
