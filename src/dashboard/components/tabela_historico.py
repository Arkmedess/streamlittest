"""
src/dashboard/components/tabela_historico.py
─────────────────────────────────────────────
Responsabilidade: renderizar a seção "Histórico de Compras" com filtros aplicados.
"""

import pandas as pd
import streamlit as st

from src.dashboard.components.shared import render_badge


def render_tabela_historico(df: pd.DataFrame, filtros: dict) -> None:
    """
    Renderiza a tabela de histórico de compras.

    Args:
        df:      DataFrame retornado por carregar_historico()
        filtros: dict retornado por render_sidebar()
    """
    st.markdown(
        '<div class="section-box">'
        '<span class="section-title">Histórico de Compras</span>',
        unsafe_allow_html=True,
    )

    # ── Filtros ───────────────────────────────────────────────────────────────
    view = df.copy()
    if filtros["cliente"]:
        view = view[view["Cliente"].str.contains(filtros["cliente"], case=False)]
    if filtros["status"]:
        view = view[view["Status"].isin(filtros["status"])]

    # ── HTML da tabela ────────────────────────────────────────────────────────
    rows = "".join(
        f"<tr>"
        f"<td>{r['NF']}</td>"
        f"<td>{r['Data']}</td>"
        f"<td>{r['Cliente']}</td>"
        f"<td>R$ {r['Valor Total (R$)']}</td>"
        f"<td>{r['Itens']}</td>"
        f"<td>{render_badge(r['Status'])}</td>"
        f"</tr>"
        for _, r in view.iterrows()
    )

    st.markdown(
        f"""
        <table class="styled-table">
          <thead>
            <tr>
              <th>NF</th><th>Data</th><th>Cliente</th>
              <th>Valor Total</th><th>Itens</th><th>Status</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )