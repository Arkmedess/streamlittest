"""
main.py
───────
Ponto de entrada. Orquestra na ordem correta:

    1. Auth      → bloqueia se não logado
    2. Page      → set_page_config + CSS (deve vir antes de qualquer st.*)
    3. Logout    → injeta botão na sidebar
    4. Dados     → carrega DataFrames
    5. Layout    → monta sidebar, header, colunas e componentes

Execute:
    streamlit run main.py
"""

import streamlit as st

from src.auth import require_login, render_logout_button
from src.dashboard import setup_page
from src.dashboard.components import (
    render_sidebar,
    render_kpi_cards,
    render_tabela_nfs,
    render_tabela_historico,
    render_painel_resumo,
)
from src.data import carregar_nfs, carregar_historico

# ── 1. Auth ───────────────────────────────────────────────────────────────────
require_login()

# ── 2. Configuração da página + CSS global ────────────────────────────────────
setup_page()

# ── 3. Logout na sidebar ──────────────────────────────────────────────────────
render_logout_button()

# ── 4. Dados ──────────────────────────────────────────────────────────────────
df_nfs       = carregar_nfs()
df_historico = carregar_historico()

# ── 5. Layout ─────────────────────────────────────────────────────────────────
filtros = render_sidebar()

st.markdown(
    '<p class="main-header">📋 Histórico de Compra do Clientes</p>',
    unsafe_allow_html=True,
)

render_kpi_cards(df_nfs, df_historico)

col_esq, col_dir = st.columns([3, 1.1])

with col_esq:
    render_tabela_nfs(df_nfs, filtros)
    render_tabela_historico(df_historico, filtros)

with col_dir:
    render_painel_resumo(df_nfs, df_historico)