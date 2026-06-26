"""
src/dashboard/components/painel_resumo.py
──────────────────────────────────────────
Responsabilidade: renderizar o painel direito (resumo + gráfico de status).
"""

import pandas as pd
import streamlit as st

from src.dashboard.components.shared import brl


def render_painel_resumo(df_nfs: pd.DataFrame, df_historico: pd.DataFrame) -> None:
    """
    Renderiza o painel lateral direito com resumo e gráfico.

    Args:
        df_nfs:       DataFrame retornado por carregar_nfs()
        df_historico: DataFrame retornado por carregar_historico()
    """
    # ── Métricas ──────────────────────────────────────────────────────────────
    total_compras = len(df_historico)
    total_valor   = df_historico["Valor Total (R$)"].astype(float).sum()
    cliente_top   = df_historico["Cliente"].value_counts().idxmax()
    ticket_medio  = total_valor / max(total_compras, 1)

    resumo = [
        ("🧾 Total de NFs",      str(total_compras)),
        ("💰 Volume total",       brl(total_valor)),
        ("🎯 Ticket médio",       brl(ticket_medio)),
        ("👑 Cliente mais ativo", cliente_top),
        ("📦 Produtos distintos", str(df_nfs["Produto"].nunique())),
        ("📅 Período analisado",  "Últimos 24 meses"),
    ]

    # ── Resumo ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="right-panel">'
        '<div class="right-panel-title">📊 Resumo do Cliente</div>',
        unsafe_allow_html=True,
    )

    for label, val in resumo:
        st.markdown(
            f"""
            <div style="padding:10px 0;border-bottom:1px solid #e8f0e8;">
              <div style="font-size:0.72rem;color:#888;text-transform:uppercase;
                          letter-spacing:0.5px;">{label}</div>
              <div style="font-size:1rem;font-weight:700;color:#1a5c2a;">{val}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Gráfico ───────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="right-panel">'
        '<div class="right-panel-title">📈 Compras por Status</div>',
        unsafe_allow_html=True,
    )

    status_counts = df_historico["Status"].value_counts()
    st.bar_chart(pd.DataFrame({"Quantidade": status_counts}), color="#1a5c2a", height=200)

    st.markdown("</div>", unsafe_allow_html=True)