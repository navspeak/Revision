"""A little CSS to make the Streamlit defaults feel sleeker."""
import streamlit as st

CSS = """
<style>
.block-container {padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1500px;}
h1 {font-weight: 650; letter-spacing: -0.01em;}
div[data-testid="stMetric"] {background: rgba(127,127,127,0.07); border-radius: 12px; padding: 10px 14px;}
button[kind="primary"] {border-radius: 10px;}
.jb-pill {display:inline-block; padding:2px 10px; margin:0 6px 6px 0; border-radius:999px;
  font-size:0.82rem; border:1px solid rgba(127,127,127,0.35);}
.jb-muted {color: rgba(127,127,127,0.95); font-size: 0.9rem;}
</style>
"""


def apply() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
