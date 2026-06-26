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

from __future__ import annotations

from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import streamlit as st

from src.auth import get_current_user, require_login, render_logout_button
from src.dashboard import setup_page
from src.dashboard.components import (
    render_sidebar,
    render_kpi_cards,
    render_tabela_nfs,
    render_tabela_historico,
    render_painel_resumo,
)
from src.dashboard.components.logs import render_logs
from src.data import carregar_base, filtrar_base
from src.data.supabase_client import replace_vendas
from src.data.uploader import processar_csv
from src.logging import setup_logger

logger = setup_logger(__name__)


def _table_nfs(df_filtrado: pd.DataFrame) -> pd.DataFrame:
    if df_filtrado.empty:
        return pd.DataFrame(
            columns=[
                "NF",
                "Data",
                "Cód. Produto",
                "Descrição de Produto",
                "Qtd",
                "Valor Unitário",
                "Total Mercadoria",
                "Status Item",
                "Pedido de Venda",
            ]
        )

    view = df_filtrado.copy()
    view["Valor Unitário"] = view["vlr_total_mercadoria"] / view["qtd"].replace(0, pd.NA)

    return pd.DataFrame(
        {
            "NF": view["nota_fiscal"],
            "Data": view["data_faturamento"].dt.strftime("%d/%m/%Y"),
            "Cód. Produto": view["prd"],
            "Descrição de Produto": view["descricao_produto"],
            "Qtd": view["qtd"],
            "Valor Unitário": view["Valor Unitário"],
            "Total Mercadoria": view["vlr_total_mercadoria"],
            "Status Item": view["status"],
            "Pedido de Venda": view["pedido_venda"],
        }
    )


def _table_historico(df_filtrado: pd.DataFrame) -> pd.DataFrame:
    if df_filtrado.empty:
        return pd.DataFrame(
            columns=["NF", "Data Faturamento", "Cliente", "Valor Total NF", "Operação", "Cidade", "Estado"]
        )

    hist = (
        df_filtrado.groupby(
            ["nota_fiscal", "data_faturamento", "cliente_nome_fantasia", "tipo_operacao", "cidade", "uf"],
            as_index=False,
        )
        .agg(vlr_total_nf=("vlr_total_nf", "max"))
        .sort_values("data_faturamento", ascending=False)
    )

    return pd.DataFrame(
        {
            "NF": hist["nota_fiscal"],
            "Data Faturamento": hist["data_faturamento"].dt.strftime("%d/%m/%Y"),
            "Cliente": hist["cliente_nome_fantasia"],
            "Valor Total NF": hist["vlr_total_nf"],
            "Operação": hist["tipo_operacao"],
            "Cidade": hist["cidade"],
            "Estado": hist["uf"],
        }
    )


def _excel_bytes(df_nfs: pd.DataFrame, df_hist: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_nfs.to_excel(writer, index=False, sheet_name="Itens NF")
        df_hist.to_excel(writer, index=False, sheet_name="Historico Consolidado")
    buffer.seek(0)
    return buffer.getvalue()


def _pdf_bytes(df_nfs: pd.DataFrame, df_hist: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    w, h = landscape(A4)

    c.setTitle("Relatorio Compras")
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#1a5c2a"))
    c.drawString(20 * mm, h - 20 * mm, "Relatorio de Compras - Dados Filtrados")

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(20 * mm, h - 30 * mm, f"Itens NF: {len(df_nfs)} linhas")
    c.drawString(20 * mm, h - 37 * mm, f"Historico Consolidado: {len(df_hist)} linhas")

    amostra_nfs = df_nfs.head(12).fillna("")
    amostra_hist = df_hist.head(12).fillna("")

    y = h - 50 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Amostra - Itens da Nota Fiscal")
    y -= 6 * mm
    c.setFont("Helvetica", 8)
    for row in amostra_nfs.itertuples(index=False):
        texto = " | ".join(str(v) for v in row[:6])
        c.drawString(20 * mm, y, texto[:145])
        y -= 4.5 * mm
        if y < 18 * mm:
            c.showPage()
            y = h - 20 * mm

    y -= 3 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Amostra - Historico Consolidado")
    y -= 6 * mm
    c.setFont("Helvetica", 8)
    for row in amostra_hist.itertuples(index=False):
        texto = " | ".join(str(v) for v in row)
        c.drawString(20 * mm, y, texto[:145])
        y -= 4.5 * mm
        if y < 18 * mm:
            c.showPage()
            y = h - 20 * mm

    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# ── 1. Auth ───────────────────────────────────────────────────────────────────
require_login()

# ── 2. Configuração da página + CSS global ────────────────────────────────────
setup_page()

# ── 3. Logout na sidebar ──────────────────────────────────────────────────────
render_logout_button()
user = get_current_user()
logger.info("Usuário atual: %s (role=%s)", user.get("email", "-"), user.get("role"))

# ── 4. Dados ──────────────────────────────────────────────────────────────────
df_base = carregar_base()
logger.info("Base carregada: %d linhas", len(df_base))

# ── 5. Layout ─────────────────────────────────────────────────────────────────
filtros = render_sidebar(df_base)
df_filtrado = filtrar_base(df_base, filtros)
df_export_nfs = _table_nfs(df_filtrado)
df_export_hist = _table_historico(df_filtrado)

if user["role"] == "admin":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<span class="section-title">Upload de Arquivos</span>', unsafe_allow_html=True)
    arquivo = st.file_uploader(
        "Selecione um CSV consolidado",
        type=["csv"],
        label_visibility="collapsed",
    )

    if arquivo is not None and st.button("Importar para o banco", width='stretch'):
        try:
            df_upload = processar_csv(arquivo)
            replace_vendas(df_upload)
            st.success("Arquivo importado com sucesso.")
        except Exception as e:
            st.error(f"Falha ao importar arquivo: {e}")
            # render recent logs for debugging to admins
            with st.expander("Ver logs de erro", expanded=True):
                render_logs(200)

    st.markdown("</div>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="header-grid">', unsafe_allow_html=True)
    hdr1, hdr2, hdr3 = st.columns([6.5, 1.2, 1.2], gap="medium")
    with hdr1:
        st.markdown(
            '<div class="header-shell"><p class="main-header">Histórico de Compra do Clientes</p><div class="header-subtitle">Análise de recência, consolidação de faturamento e comportamento de compra</div></div>',
            unsafe_allow_html=True,
        )
    with hdr2:
        st.download_button(
            "🧾 Exportar PDF",
            data=_pdf_bytes(df_export_nfs, df_export_hist),
            file_name="dashboard_compras_filtrado.pdf",
            mime="application/pdf",
            width='stretch',
        )
    with hdr3:
        st.download_button(
            "📊 Exportar Excel",
            data=_excel_bytes(df_export_nfs, df_export_hist),
            file_name="dashboard_compras_filtrado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width='stretch',
        )
    st.markdown('</div>', unsafe_allow_html=True)

render_kpi_cards(df_filtrado)

with st.container():
    st.markdown('<div class="content-grid">', unsafe_allow_html=True)
    col_esq, col_dir = st.columns([3, 1.1], gap="large")

    with col_esq:
        render_tabela_nfs(df_filtrado)
        render_tabela_historico(df_filtrado)

    with col_dir:
        render_painel_resumo(df_filtrado)

    st.markdown('</div>', unsafe_allow_html=True)
