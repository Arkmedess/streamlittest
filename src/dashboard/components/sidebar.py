"""
src/dashboard/components/sidebar.py
────────────────────────────────────
Responsabilidade: renderizar a sidebar com logo e filtros.
Retorna um dict com os valores selecionados pelo usuário.
"""

import streamlit as st
from src.data.loader import STATUS


def render_sidebar() -> dict:
    """
    Renderiza logo + filtros na sidebar.

    Retorna:
        {
            "cliente":  str,
            "produto":  str,
            "status":   list[str],
        }
    """
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo"><span>⚙ TPI</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown("**Cliente**")
        cliente = st.text_input(
            "", placeholder="Buscar cliente…",
            label_visibility="collapsed",
            key="filtro_cliente",
        )

        st.markdown("---")
        st.markdown("**Produto**")
        produto = st.text_input(
            "", placeholder="Buscar produto…",
            label_visibility="collapsed",
            key="filtro_produto",
        )

        st.markdown("---")
        st.markdown("**Status**")
        status = st.multiselect(
            "", options=STATUS, default=[],
            label_visibility="collapsed",
            key="filtro_status",
        )

    return {"cliente": cliente, "produto": produto, "status": status}