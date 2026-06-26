"""
src/dashboard/components/sidebar.py
────────────────────────────────────
Responsabilidade: renderizar a sidebar com logo e filtros.
Retorna um dict com os valores selecionados pelo usuário.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st


def _options(series: pd.Series) -> list[str]:
    return ["Todos", *sorted(series.dropna().astype(str).unique().tolist())]


def render_sidebar(df_base: pd.DataFrame) -> dict:
    """
    Renderiza logo + filtros na sidebar.

    Retorna:
        {
            "cliente": str,
            "cidade": str,
            "estado": str,
            "codigo_produto": str,
            "descricao_produto": str,
            "pedido_venda": str,
            "data_intervalo": tuple[date, date],
        }
    """
    logo_html = (
        '<div class="sidebar-logo">'
        '<div class="sidebar-logo-symbol">'
        '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<path d="M14 3l7 7-3 3-2-2-5 5 2 2-3 3-7-7 3-3 2 2 5-5-2-2z" />'
        '</svg>'
        '</div>'
        '<div class="sidebar-logo-text">TPI</div>'
        '</div>'
    )

    if df_base.empty:
        with st.sidebar:
            st.markdown(logo_html, unsafe_allow_html=True)
            st.info("Sem dados disponíveis para exibir filtros.")

        hoje = date.today()
        return {
            "cliente": "",
            "cidade": "Todos",
            "estado": "Todos",
            "codigo_produto": "Todos",
            "descricao_produto": "Todos",
            "pedido_venda": "Todos",
            "data_intervalo": (hoje, hoje),
        }

    data_min = df_base["data_faturamento"].min().date()
    data_max = df_base["data_faturamento"].max().date()

    cliente_busca = st.session_state.get("filtro_cliente", "")
    cidade_sel = st.session_state.get("filtro_cidade", "Todos")
    estado_sel = st.session_state.get("filtro_estado", "Todos")
    codigo_sel = st.session_state.get("filtro_codigo_produto", "Todos")
    desc_sel = st.session_state.get("filtro_descricao_produto", "Todos")
    pedido_sel = st.session_state.get("filtro_pedido_venda", "Todos")
    intervalo_sel = st.session_state.get("filtro_data_slider") or st.session_state.get(
        "filtro_data", (data_min, data_max)
    )

    if isinstance(intervalo_sel, tuple) and len(intervalo_sel) == 2:
        inicio_sel, fim_sel = intervalo_sel
    else:
        inicio_sel, fim_sel = data_min, data_max

    base_opcoes = df_base.copy()
    if cliente_busca.strip():
        base_opcoes = base_opcoes[
            base_opcoes["cliente_nome_fantasia"].str.contains(cliente_busca.strip(), case=False, na=False)
        ]
    if cidade_sel != "Todos":
        base_opcoes = base_opcoes[base_opcoes["cidade"] == cidade_sel]
    if estado_sel != "Todos":
        base_opcoes = base_opcoes[base_opcoes["uf"] == estado_sel]
    if codigo_sel != "Todos":
        base_opcoes = base_opcoes[base_opcoes["prd"] == codigo_sel]
    if desc_sel != "Todos":
        base_opcoes = base_opcoes[base_opcoes["descricao_produto"] == desc_sel]
    if pedido_sel != "Todos":
        base_opcoes = base_opcoes[base_opcoes["pedido_venda"] == pedido_sel]

    inicio_sel = max(min(inicio_sel, data_max), data_min)
    fim_sel = max(min(fim_sel, data_max), data_min)
    if inicio_sel > fim_sel:
        inicio_sel, fim_sel = fim_sel, inicio_sel

    with st.sidebar:
        st.markdown(logo_html, unsafe_allow_html=True)

        st.markdown("**Cliente (Nome Fantasia)**")
        cliente = st.text_input(
            "",
            placeholder="Buscar...",
            label_visibility="collapsed",
            key="filtro_cliente",
        )

        st.markdown("---")
        st.markdown("**Cidade**")
        cidade_options = _options(base_opcoes["cidade"])
        cidade_default = cidade_options.index(cidade_sel) if cidade_sel in cidade_options else 0
        cidade = st.selectbox(
            "",
            options=cidade_options,
            index=cidade_default,
            label_visibility="collapsed",
            key="filtro_cidade",
        )

        st.markdown("---")
        st.markdown("**Estado**")
        estado_options = _options(base_opcoes["uf"])
        estado_default = estado_options.index(estado_sel) if estado_sel in estado_options else 0
        estado = st.selectbox(
            "",
            options=estado_options,
            index=estado_default,
            label_visibility="collapsed",
            key="filtro_estado",
        )

        st.markdown("---")
        st.markdown("**Código do Produto**")
        codigo_options = _options(base_opcoes["prd"])
        codigo_default = codigo_options.index(codigo_sel) if codigo_sel in codigo_options else 0
        codigo_produto = st.selectbox(
            "",
            options=codigo_options,
            index=codigo_default,
            label_visibility="collapsed",
            key="filtro_codigo_produto",
        )

        st.markdown("---")
        st.markdown("**Descrição do Produto**")
        descricao_options = _options(base_opcoes["descricao_produto"])
        descricao_default = descricao_options.index(desc_sel) if desc_sel in descricao_options else 0
        descricao_produto = st.selectbox(
            "",
            options=descricao_options,
            index=descricao_default,
            label_visibility="collapsed",
            key="filtro_descricao_produto",
        )

        st.markdown("---")
        st.markdown("**Pedido de Venda**")
        pedido_options = _options(base_opcoes["pedido_venda"])
        pedido_default = pedido_options.index(pedido_sel) if pedido_sel in pedido_options else 0
        pedido_venda = st.selectbox(
            "",
            options=pedido_options,
            index=pedido_default,
            label_visibility="collapsed",
            key="filtro_pedido_venda",
        )

        st.markdown("---")
        st.markdown("**Data do Faturamento (Período)**")
        slider_intervalo = st.slider(
            "",
            min_value=data_min,
            max_value=data_max,
            value=(inicio_sel, fim_sel),
            format="DD/MM/YYYY",
            label_visibility="collapsed",
            key="filtro_data_slider",
        )
        manual_intervalo = st.date_input(
            "",
            value=slider_intervalo,
            min_value=data_min,
            max_value=data_max,
            label_visibility="collapsed",
            key="filtro_data_manual",
        )
        if isinstance(manual_intervalo, tuple) and len(manual_intervalo) == 2:
            if manual_intervalo != slider_intervalo:
                st.session_state["filtro_data_slider"] = manual_intervalo
                slider_intervalo = manual_intervalo

        data_intervalo = slider_intervalo
        st.markdown(
            f'<div class="sidebar-date-range">Período selecionado: {data_intervalo[0].strftime("%d/%m/%Y")} - {data_intervalo[1].strftime("%d/%m/%Y")}</div>',
            unsafe_allow_html=True,
        )

    return {
        "cliente": cliente,
        "cidade": cidade,
        "estado": estado,
        "codigo_produto": codigo_produto,
        "descricao_produto": descricao_produto,
        "pedido_venda": pedido_venda,
        "data_intervalo": data_intervalo,
    }
