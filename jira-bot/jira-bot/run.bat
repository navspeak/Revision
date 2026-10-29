@echo off
REM Starts Jira Bot. Double-click this file, or run it from a terminal.
cd /d "%~dp0"
where py >nul 2>nul && (py -3 app.py) || (python app.py)
if errorlevel 1 pause
