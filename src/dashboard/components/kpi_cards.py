"""
src/dashboard/components/kpi_cards.py
──────────────────────────────────────
Responsabilidade: renderizar os 4 KPI cards do topo.
Recebe os DataFrames já carregados, calcula as métricas e renderiza.
"""

from datetime import datetime

import pandas as pd
import streamlit as st


def render_kpi_cards(df_nfs: pd.DataFrame, df_historico: pd.DataFrame) -> None:
    """Renderiza a linha dos 4 KPI cards."""

    ultima_nf   = df_nfs["NF"].iloc[0]
    ultima_data = df_nfs["Data"].iloc[0]

    datas_dt   = pd.to_datetime(df_historico["Data"], dayfirst=True)
    dias_ult   = (datetime.today() - datas_dt.max()).days
    media_dias = round(
        (datas_dt.max() - datas_dt.min()).days / max(len(df_historico) - 1, 1)
    )

    cards = [
        ("🧾", "Última NF",        ultima_nf),
        ("📅", "Última Data",       ultima_data),
        ("🗓️", "Dias últ. compra",  f"{dias_ult} dias"),
        ("📈", "Média de dias",      f"{media_dias} dias"),
    ]

    cols = st.columns(4)
    for col, (icon, label, value) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                  <div class="metric-icon">{icon}</div>
                  <div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)