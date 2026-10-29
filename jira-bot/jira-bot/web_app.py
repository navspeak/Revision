"""Jira Bot, web edition. Start it with run-web.sh / run-web.bat, or: streamlit run web_app.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st  # noqa: E402

st.set_page_config(page_title="Jira Bot", page_icon="🧭", layout="wide", initial_sidebar_state="expanded")

from jirabot.web import agents, ask, review, settings, skills, style  # noqa: E402

style.apply()
PAGES = {
    "ask": st.Page(ask.page, title="Ask", icon="💬", url_path="ask", default=True),
    "review": st.Page(review.page, title="Review", icon="🗂️", url_path="review"),
    "skills": st.Page(skills.page, title="Skills", icon="📚", url_path="skills"),
    "agents": st.Page(agents.page, title="Agents", icon="🤖", url_path="agents"),
    "settings": st.Page(settings.page, title="Settings", icon="⚙️", url_path="settings"),
}
st.session_state["_pages"] = PAGES
st.navigation(list(PAGES.values())).run()
