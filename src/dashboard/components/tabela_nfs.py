"""
src/dashboard/components/tabela_nfs.py
───────────────────────────────────────
Responsabilidade: renderizar a seção "Itens da NF" com filtros aplicados.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.components.shared import brl, render_badge


def render_tabela_nfs(df_filtrado: pd.DataFrame) -> None:
    """
    Renderiza a tabela de itens da NF.

    Args:
        df_filtrado: dataframe base com filtros já aplicados.
    """
    st.markdown(
        '<div class="section-box">'
        '<span class="section-title">Itens da Nota Fiscal</span>',
        unsafe_allow_html=True,
    )

    if df_filtrado.empty:
        st.info("Sem dados para os filtros selecionados.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    view = df_filtrado.copy()
    view["valor_unitario"] = view["vlr_total_mercadoria"] / view["qtd"].replace(0, pd.NA)

    total_linhas = len(view)
    linhas_por_pagina = st.selectbox(
        "Linhas por página (Itens)",
        options=[10, 20, 50],
        index=1,
        key="nfs_page_size",
    )

    page_key = "nfs_page_current"
    if page_key not in st.session_state:
        st.session_state[page_key] = 1

    paginas = max((total_linhas - 1) // linhas_por_pagina + 1, 1)
    st.session_state[page_key] = min(max(int(st.session_state[page_key]), 1), paginas)
    pagina = int(st.session_state[page_key])

    inicio = (int(pagina) - 1) * linhas_por_pagina
    fim = inicio + linhas_por_pagina
    page = view.iloc[inicio:fim]

    rows = "".join(
        f"<tr>"
        f"<td>{r['nota_fiscal']}</td>"
        f"<td>{r['data_faturamento'].strftime('%d/%m/%Y')}</td>"
        f"<td>{r['prd']}</td>"
        f"<td>{r['descricao_produto']}</td>"
        f"<td>{int(r['qtd']) if pd.notna(r['qtd']) else 0}</td>"
        f"<td>{brl(float(r['valor_unitario']) if pd.notna(r['valor_unitario']) else 0.0)}</td>"
        f"<td>{brl(float(r['vlr_total_mercadoria']) if pd.notna(r['vlr_total_mercadoria']) else 0.0)}</td>"
        f"<td>{render_badge(str(r['status']))}</td>"
        f"<td>{r['pedido_venda']}</td>"
        f"</tr>"
        for _, r in page.iterrows()
    )

    st.markdown(
        f"""
        <div class="table-scroll">
          <table class="styled-table">
            <thead>
              <tr>
                <th>NF</th><th>Data</th><th>Cód. Produto</th><th>Descrição de Produto</th>
                <th>Qtd</th><th>Valor Unitário</th><th>Total Mercadoria</th><th>Status Item</th><th>Pedido de Venda</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    p1, p2, p3 = st.columns([1, 3, 1])
    with p1:
        if st.button("◀", key="nfs_prev", disabled=pagina <= 1, width='stretch'):
            st.session_state[page_key] = max(1, pagina - 1)
            st.rerun()
    with p2:
        st.markdown(
            f'<div class="pager-text">Página {pagina} de {paginas} • Mostrando {inicio + 1} a {min(fim, total_linhas)} de {total_linhas} linhas</div>',
            unsafe_allow_html=True,
        )
    with p3:
        if st.button("▶", key="nfs_next", disabled=pagina >= paginas, width='stretch'):
            st.session_state[page_key] = min(paginas, pagina + 1)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
