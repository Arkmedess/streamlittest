"""
src/dashboard/components/tabela_historico.py
─────────────────────────────────────────────
Responsabilidade: renderizar a seção "Histórico de Compras" com filtros aplicados.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.components.shared import brl


def render_tabela_historico(df_filtrado: pd.DataFrame) -> None:
    """
    Renderiza a tabela de histórico de compras.

    Args:
        df_filtrado: dataframe base com filtros já aplicados.
    """
    st.markdown(
        '<div class="section-box">'
        '<span class="section-title">Histórico de Compras Consolidadas</span>',
        unsafe_allow_html=True,
    )

    if df_filtrado.empty:
        st.info("Sem dados para os filtros selecionados.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    view = (
        df_filtrado.groupby(
            [
                "nota_fiscal",
                "data_faturamento",
                "cliente_nome_fantasia",
                "tipo_operacao",
                "cidade",
                "uf",
            ],
            as_index=False,
        )
        .agg(vlr_total_nf=("vlr_total_nf", "max"))
        .sort_values("data_faturamento", ascending=False)
    )

    total_linhas = len(view)
    linhas_por_pagina = st.selectbox(
        "Linhas por página (Consolidado)",
        options=[10, 20, 50],
        index=1,
        key="hist_page_size",
    )

    page_key = "hist_page_current"
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
        f"<td>{r['cliente_nome_fantasia']}</td>"
        f"<td>{brl(float(r['vlr_total_nf']) if pd.notna(r['vlr_total_nf']) else 0.0)}</td>"
        f"<td>{r['tipo_operacao']}</td>"
        f"<td>{r['cidade']}</td>"
        f"<td>{r['uf']}</td>"
        f"</tr>"
        for _, r in page.iterrows()
    )

    st.markdown(
        f"""
        <div class="table-scroll">
          <table class="styled-table">
            <thead>
              <tr>
                <th>NF</th><th>Data Faturamento</th><th>Cliente</th>
                <th>Valor Total NF</th><th>Operação</th><th>Cidade</th><th>Estado</th>
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
        if st.button("◀", key="hist_prev", disabled=pagina <= 1, width='stretch'):
            st.session_state[page_key] = max(1, pagina - 1)
            st.rerun()
    with p2:
        st.markdown(
            f'<div class="pager-text">Página {pagina} de {paginas} • Mostrando {inicio + 1} a {min(fim, total_linhas)} de {total_linhas} linhas</div>',
            unsafe_allow_html=True,
        )
    with p3:
        if st.button("▶", key="hist_next", disabled=pagina >= paginas, width='stretch'):
            st.session_state[page_key] = min(paginas, pagina + 1)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
