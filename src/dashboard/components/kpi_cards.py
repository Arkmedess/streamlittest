"""
src/dashboard/components/kpi_cards.py
──────────────────────────────────────
Responsabilidade: renderizar os 4 KPI cards do topo.
Recebe os DataFrames já carregados, calcula as métricas e renderiza.
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st


def _ultima_nf(df_base: pd.DataFrame) -> str:
    if df_base.empty:
        return "-"

    ult_data = df_base["data_faturamento"].max()
    candidatas = df_base[df_base["data_faturamento"] == ult_data]["nota_fiscal"].astype(str)
    numericas = pd.to_numeric(candidatas, errors="coerce")
    if numericas.notna().any():
        return str(int(numericas.max()))
    return candidatas.max()


def _media_dias_entre_compras(df_base: pd.DataFrame) -> int:
    if df_base.empty:
        return 0

    base_unica = (
        df_base[["cliente_nome_fantasia", "data_faturamento"]]
        .drop_duplicates()
        .sort_values(["cliente_nome_fantasia", "data_faturamento"])
    )
    base_unica["delta"] = base_unica.groupby("cliente_nome_fantasia")["data_faturamento"].diff().dt.days
    media = base_unica["delta"].dropna()
    if media.empty:
        return 0
    return int(round(media.mean()))


def render_kpi_cards(df_base: pd.DataFrame) -> None:
    """Renderiza a linha dos 4 KPI cards."""
    if df_base.empty:
        ultima_nf = "-"
        ultima_data = "-"
        dias_ult = 0
        media_dias = 0
    else:
        ultima_nf = _ultima_nf(df_base)
        dt_ultima_compra = df_base["data_faturamento"].max()
        ultima_data = dt_ultima_compra.strftime("%d/%m/%Y")
        dias_ult = (datetime.today().date() - dt_ultima_compra.date()).days
        media_dias = _media_dias_entre_compras(df_base)

    icons = {
        "nf": (
            "<svg viewBox='0 0 24 24' aria-hidden='true' focusable='false'>"
            "<path d='M7 4h7l3 3v13H7z' />"
            "<path d='M14 4v3h3' />"
            "<path d='M9 12h6' />"
            "<path d='M9 16h4' />"
            "</svg>"
        ),
        "date": (
            "<svg viewBox='0 0 24 24' aria-hidden='true' focusable='false'>"
            "<path d='M7 4v3' /><path d='M17 4v3' />"
            "<rect x='4' y='6' width='16' height='14' rx='2' />"
            "<path d='M4 10h16' />"
            "</svg>"
        ),
        "days": (
            "<svg viewBox='0 0 24 24' aria-hidden='true' focusable='false'>"
            "<circle cx='12' cy='12' r='8' />"
            "<path d='M12 8v5l3 2' />"
            "</svg>"
        ),
        "avg": (
            "<svg viewBox='0 0 24 24' aria-hidden='true' focusable='false'>"
            "<path d='M6 12a6 6 0 0 1 10.4-3.9' />"
            "<path d='M18 6v4h-4' />"
            "<path d='M18 12a6 6 0 0 1-10.4 3.9' />"
            "<path d='M6 18v-4h4' />"
            "</svg>"
        ),
    }

    cards = [
        (icons["nf"], "Última NF", ultima_nf),
        (icons["date"], "Última Data", ultima_data),
        (icons["days"], "Dias últ. compra", f"{dias_ult} dias"),
        (icons["avg"], "Média dias entre compras", f"{media_dias} dias"),
    ]

    items = "".join(
        f"""
        <div class='metric-card'>
            <div class='metric-icon'>{icon}</div>
            <div>
                <div class='metric-label'>{label}</div>
                <div class='metric-value'>{value}</div>
            </div>
        </div>
        """
        for icon, label, value in cards
    )

    # Render using native Streamlit columns to avoid any escaping issues
    # and keep behavior consistent across Streamlit versions.
    cols = st.columns(4)
    for col, (icon, label, value) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class='metric-card'>
                  <div class='metric-icon'>{icon}</div>
                  <div>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
