"""
src/dashboard/components/tabela_nfs.py
───────────────────────────────────────
Responsabilidade: renderizar a seção "Itens da NF" com filtros aplicados.
"""

import pandas as pd
import streamlit as st

from src.dashboard.components.shared import render_badge


def render_tabela_nfs(df: pd.DataFrame, filtros: dict) -> None:
    """
    Renderiza a tabela de itens da NF.

    Args:
        df:      DataFrame retornado por carregar_nfs()
        filtros: dict retornado por render_sidebar()
    """
    st.markdown(
        '<div class="section-box">'
        '<span class="section-title">Itens da NF</span>',
        unsafe_allow_html=True,
    )

    # ── Filtros ───────────────────────────────────────────────────────────────
    view = df.copy()
    if filtros["produto"]:
        view = view[view["Produto"].str.contains(filtros["produto"], case=False)]
    if filtros["status"]:
        view = view[view["Status"].isin(filtros["status"])]

    # ── HTML da tabela ────────────────────────────────────────────────────────
    rows = "".join(
        f"<tr>"
        f"<td>{r['NF']}</td>"
        f"<td>{r['Data']}</td>"
        f"<td>{r['Produto']}</td>"
        f"<td>{r['Qtd']}</td>"
        f"<td>R$ {r['Valor (R$)']}</td>"
        f"<td>{render_badge(r['Status'])}</td>"
        f"</tr>"
        for _, r in view.iterrows()
    )

    st.markdown(
        f"""
        <table class="styled-table">
          <thead>
            <tr>
              <th>NF</th><th>Data</th><th>Produto</th>
              <th>Qtd</th><th>Valor</th><th>Status</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )