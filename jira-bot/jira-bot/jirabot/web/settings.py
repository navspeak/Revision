"""Settings page: Jira login (via ACLI), Copilot, limits."""
from __future__ import annotations

import streamlit as st

from ..config import normalize_site
from ..proc import CommandError, tail
from . import services


def page() -> None:
    ctx = services.context()
    s = ctx.settings
    st.title("Settings")
    st.caption(f"Saved in {s.config_path}. Your API token is never saved by this app.")
    if s.env_locked:
        st.info("Set by .env or environment variables (edit that file to change them): "
                + ", ".join(sorted("JIRABOT_" + k.upper() for k in s.env_locked)))

    with st.form("settings"):
        st.subheader("Jira")
        c1, c2 = st.columns(2)
        site = c1.text_input("Jira site", s.jira_site, placeholder="mycompany.atlassian.net")
        email = c2.text_input("Email", s.jira_email)
        c1, c2 = st.columns(2)
        acli_cmd = c1.text_input("ACLI command", s.acli_command)
        acli_timeout = c2.number_input("ACLI timeout (seconds)", 10, 3600, int(s.acli_timeout))
        c1, c2 = st.columns(2)
        limit = c1.number_input("Default max rows", 1, 100000, int(s.default_limit))
        fields = c2.text_input("Default columns (optional, comma separated)", s.default_fields)
        st.subheader("Copilot")
        c1, c2 = st.columns(2)
        cop_cmd = c1.text_input("Copilot command", s.copilot_command)
        model = c2.text_input("Model (optional)", s.copilot_model)
        extra = st.text_input("Extra Copilot arguments (optional)", s.copilot_extra_args,
                              help="Never put --allow-all-tools here unless you understand what it allows.")
        c1, c2 = st.columns(2)
        cop_timeout = c1.number_input("Copilot timeout (seconds)", 10, 3600, int(s.copilot_timeout))
        budget = c2.number_input("Max prompt size (characters)", 2000, 200000, int(s.max_prompt_chars))
        share = st.checkbox(
            "Let Copilot see the first 25 result rows (for follow-up questions and summaries)",
            value=s.share_results,
        )
        saved = st.form_submit_button("Save settings", type="primary")
    if saved:
        s.jira_site = normalize_site(site)
        s.jira_email = email.strip()
        s.acli_command = acli_cmd.strip() or "acli"
        s.acli_timeout = int(acli_timeout)
        s.default_limit = int(limit)
        s.default_fields = fields.strip()
        s.copilot_command = cop_cmd.strip() or "copilot"
        s.copilot_model = model.strip()
        s.copilot_extra_args = extra.strip()
        s.copilot_timeout = int(cop_timeout)
        s.max_prompt_chars = int(budget)
        s.share_results = bool(share)
        s.save()
        st.success("Settings saved.")

    st.subheader("Check the connections")
    c1, c2 = st.columns(2)
    if c1.button("Test Copilot"):
        try:
            with st.spinner("Asking Copilot..."):
                reply = ctx.llm.ask("Reply with the single word OK.")
            st.success(f"Copilot answered: {reply[:200]}")
            st.caption("Command used: " + ctx.llm.describe())
        except CommandError as exc:
            st.error(str(exc))
    if c2.button("Check Jira login"):
        try:
            with st.spinner("Asking ACLI..."):
                status = ctx.acli.auth_status()
            st.code(tail(status.stdout or status.stderr, 800) or "(no output)")
            if status.ok:
                with st.spinner("Running a one-row test search..."):
                    res = ctx.acli.search("created >= -30d ORDER BY created DESC", limit=1)
                st.success(f"Search works ({len(res.rows)} row returned).")
        except (CommandError, ValueError) as exc:
            st.error(str(exc))

    st.subheader("Log in to Jira")
    st.caption("Create an API token at id.atlassian.com (Security, API tokens). It goes straight to ACLI and is not stored here.")
    from_env = s.env_token
    if from_env:
        st.info("An API token was found in your environment or .env file, so you can leave the box empty.")
    with st.form("login", clear_on_submit=True):
        token = st.text_input("API token", type="password", placeholder="(use the token from .env)" if from_env else "")
        go = st.form_submit_button("Log in")
    if go:
        token = token or from_env
        if not (s.site_host and s.jira_email and token.strip()):
            st.warning("Save your site and email above, then enter the token.")
        else:
            try:
                with st.spinner("Logging in..."):
                    result = ctx.acli.login(s.site_host, s.jira_email, token)
                body = tail(result.stdout or result.stderr, 800)
                (st.success if result.ok else st.error)(("Logged in.\n" if result.ok else f"Login failed (exit {result.returncode}):\n") + body)
            except (CommandError, ValueError) as exc:
                st.error(str(exc))
