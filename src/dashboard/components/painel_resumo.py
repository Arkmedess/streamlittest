"""
src/dashboard/components/painel_resumo.py
──────────────────────────────────────────
Responsabilidade: renderizar o painel direito (resumo + gráfico de status).
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dashboard.components.shared import brl


STATUS_ORDER = ["Recente (<30d)", "Ativo (30-90d)", "Atenção (91-180d)", "Inativo (>180d)"]
STATUS_COLORS = ["#0f7d33", "#8dcf75", "#f0c330", "#d96b5f"]


def _classificar_status_recencia(dias: int) -> str:
    if dias < 30:
        return "Recente (<30d)"
    if dias <= 90:
        return "Ativo (30-90d)"
    if dias <= 180:
        return "Atenção (91-180d)"
    return "Inativo (>180d)"


def render_painel_resumo(df_filtrado: pd.DataFrame) -> None:
    """
    Renderiza o painel lateral direito com métricas e gráficos.

    Args:
        df_filtrado: dataframe base com filtros já aplicados.
    """
    if df_filtrado.empty:
        st.markdown(
            '<div class="right-panel">'
            '<div class="right-panel-title">Insights e Distribuição</div>'
            '<div style="color:#6b6b6b;">Sem dados para os filtros selecionados.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    consolidado_nf = (
        df_filtrado.groupby(
            ["nota_fiscal", "cliente_nome_fantasia", "data_faturamento"], as_index=False
        )
        .agg(vlr_total_nf=("vlr_total_nf", "max"))
        .sort_values("data_faturamento", ascending=False)
    )

    total_nfs = consolidado_nf["nota_fiscal"].nunique()
    volume_total = consolidado_nf["vlr_total_nf"].sum()
    ticket_medio = volume_total / total_nfs if total_nfs else 0.0

    st.markdown('<div class="right-panel"><div class="right-panel-title">Insights e Distribuição</div>', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="insight-grid">'
            f'<div class="insight-item"><div class="insight-label">Total de NFs</div><div class="insight-value">{total_nfs}</div></div>'
            f'<div class="insight-item"><div class="insight-label">Volume Total</div><div class="insight-value">{brl(float(volume_total))}</div></div>'
            f'<div class="insight-item"><div class="insight-label">Ticket Médio</div><div class="insight-value">{brl(float(ticket_medio))}</div></div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    top5 = (
        consolidado_nf.groupby("cliente_nome_fantasia", as_index=False)
        .agg(valor_total=("vlr_total_nf", "sum"))
        .sort_values("valor_total", ascending=False)
        .head(5)
    )

    st.markdown('<div class="right-panel"><div class="right-panel-title">Top 5 Clientes por Valor</div>', unsafe_allow_html=True)

    st.vega_lite_chart(
        top5,
        {
            "width": "container",
            "height": 260,
            "autosize": {"type": "fit", "contains": "padding"},
            "config": {
                "background": "#f8fbf8",
                "view": {"stroke": "transparent"},
                "axis": {
                    "labelFontSize": 12,
                    "titleFontSize": 12,
                    "labelColor": "#2c3f33",
                    "titleColor": "#2c3f33",
                    "gridColor": "#e1e9e2",
                },
            },
            "layer": [
                {
                    "mark": {"type": "bar", "cornerRadiusTopLeft": 6, "cornerRadiusTopRight": 6},
                    "encoding": {
                        "x": {
                            "field": "cliente_nome_fantasia",
                            "type": "nominal",
                            "sort": "-y",
                            "title": None,
                            "axis": {"labelAngle": -25},
                        },
                        "y": {"field": "valor_total", "type": "quantitative", "title": "Valor Total"},
                        "color": {"value": "#1a6b36"},
                        "tooltip": [
                            {"field": "cliente_nome_fantasia", "type": "nominal", "title": "Cliente"},
                            {"field": "valor_total", "type": "quantitative", "title": "Valor", "format": ",.2f"},
                        ],
                    },
                },
                {
                    "mark": {"type": "text", "dy": -10, "color": "#234a30", "fontSize": 12, "fontWeight": "bold"},
                    "encoding": {
                        "x": {"field": "cliente_nome_fantasia", "type": "nominal", "sort": "-y"},
                        "y": {"field": "valor_total", "type": "quantitative"},
                        "text": {"field": "valor_total", "type": "quantitative", "format": ",.0f"},
                    },
                },
            ],
        },
        width='stretch',
    )
    st.markdown('</div>', unsafe_allow_html=True)

    ultima_compra_cliente = (
        df_filtrado.groupby("cliente_nome_fantasia", as_index=False)
        .agg(ultima_data=("data_faturamento", "max"))
    )
    ultima_compra_cliente["dias_ult_compra"] = (
        pd.Timestamp.today().normalize() - ultima_compra_cliente["ultima_data"].dt.normalize()
    ).dt.days
    ultima_compra_cliente["status_conta"] = ultima_compra_cliente["dias_ult_compra"].apply(_classificar_status_recencia)

    distribuicao = (
        ultima_compra_cliente.groupby("status_conta", as_index=False)
        .agg(clientes=("cliente_nome_fantasia", "nunique"))
    )
    distribuicao["status_conta"] = pd.Categorical(distribuicao["status_conta"], categories=STATUS_ORDER, ordered=True)
    distribuicao = distribuicao.sort_values("status_conta")
    distribuicao["percentual"] = distribuicao["clientes"] / distribuicao["clientes"].sum()
    distribuicao["label"] = distribuicao.apply(
        lambda row: f"{row['status_conta']} {row['percentual']:.0%}", axis=1
    )

    st.markdown('<div class="right-panel"><div class="right-panel-title">Distribuição por Status de Conta</div>', unsafe_allow_html=True)

    st.vega_lite_chart(
        distribuicao,
        {
            "width": "container",
            "height": 320,
            "autosize": {"type": "fit", "contains": "padding"},
            "config": {
                "background": "#f8fbf8",
                "view": {"stroke": "transparent"},
                "legend": {
                    "labelFontSize": 12,
                    "titleFontSize": 12,
                    "labelColor": "#2c3f33",
                },
            },
            "layer": [
                {
                    "mark": {"type": "arc", "innerRadius": 90, "outerRadius": 145},
                    "encoding": {
                        "theta": {"field": "clientes", "type": "quantitative"},
                        "color": {
                            "field": "status_conta",
                            "type": "nominal",
                            "scale": {"domain": STATUS_ORDER, "range": STATUS_COLORS},
                            "legend": {"title": None, "orient": "bottom"},
                        },
                        "tooltip": [
                            {"field": "status_conta", "type": "nominal", "title": "Status"},
                            {"field": "clientes", "type": "quantitative", "title": "Clientes"},
                            {"field": "percentual", "type": "quantitative", "title": "%", "format": ".2%"},
                        ],
                    },
                },
                {
                    "mark": {
                        "type": "text",
                        "radius": 170,
                        "fontSize": 12,
                        "fontWeight": "bold",
                        "fill": "#2c3f33",
                    },
                    "encoding": {
                        "theta": {"field": "clientes", "type": "quantitative"},
                        "text": {"field": "label", "type": "nominal"},
                    },
                },
            ],
        },
        width='stretch',
    )

    legend_lines = "".join(
        f"<div><span style='color:{color};font-weight:900;'>●</span> {status}: {pct:.1%}</div>"
        for status, color, pct in zip(distribuicao['status_conta'].astype(str), STATUS_COLORS, distribuicao['percentual'])
    )
    st.markdown(f'<div class="status-legend">{legend_lines}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
