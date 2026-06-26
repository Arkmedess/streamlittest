"""Render a simple view of recent application logs inside Streamlit.

This allows front-end users (admins) to inspect recent backend events without
accessing the server filesystem directly.
"""
from __future__ import annotations

import streamlit as st
from src.logging import tail_lines


def render_logs(lines: int = 200) -> None:
    """Render the last `lines` of the application log inside an expander."""
    log_lines = tail_lines(lines)
    if not log_lines:
        st.info("Nenhum log disponível ainda.")
        return

    with st.expander("Logs recentes (backend)", expanded=False):
        st.text_area("", value="\n".join(log_lines[-lines:]), height=260, key="app_logs", disabled=True)
