import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Histórico de Compra do Clientes",
    page_icon="🛒",
    layout="wide",
)

# ── CSS – TPI green theme ─────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---------- global ---------- */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f0f4f0;
        font-family: 'Segoe UI', sans-serif;
    }

    /* ---------- sidebar ---------- */
    [data-testid="stSidebar"] {
        background-color: #1a5c2a !important;
        padding-top: 0 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] .stSelectbox select,
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #1a5c2a !important;
        border-radius: 4px;
    }
    [data-testid="stSidebar"] label {
        font-weight: 700;
        text-decoration: underline;
        font-size: 1rem;
    }
    /* logo banner */
    .sidebar-logo {
        background-color: #1a5c2a;
        padding: 16px 20px 12px 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid #2d7a40;
        margin-bottom: 20px;
    }
    .sidebar-logo span {
        font-size: 1.6rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 2px;
    }

    /* ---------- main header ---------- */
    .main-header {
        color: #1a5c2a;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 18px;
        border-bottom: 2px solid #c8ddc8;
        padding-bottom: 8px;
    }

    /* ---------- metric cards ---------- */
    .metric-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 16px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        min-height: 80px;
    }
    .metric-icon {
        background-color: #1a5c2a;
        border-radius: 50%;
        width: 46px;
        height: 46px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
    }
    .metric-label {
        font-size: 0.72rem;
        color: #888;
        margin-bottom: 2px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1a5c2a;
    }

    /* ---------- section boxes ---------- */
    .section-box {
        background: #ffffff;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        margin-bottom: 16px;
    }
    .section-title {
        background-color: #1a5c2a;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.88rem;
        border-radius: 20px;
        display: inline-block;
        padding: 4px 14px;
        margin-bottom: 14px;
    }

    /* ---------- tables ---------- */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
    }
    .styled-table thead th {
        background-color: #e8f0e8;
        color: #1a5c2a;
        font-weight: 700;
        padding: 8px 10px;
        text-align: left;
        border-bottom: 2px solid #c8ddc8;
    }
    .styled-table tbody tr:nth-child(even) {
        background-color: #f7fbf7;
    }
    .styled-table tbody td {
        padding: 7px 10px;
        border-bottom: 1px solid #e8f0e8;
        color: #333;
    }
    .badge-active {
        background-color: #d4edda;
        color: #155724;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-inactive {
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 12px;
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* ---------- right panel ---------- */
    .right-panel {
        background: #ffffff;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        height: 100%;
    }
    .right-panel-title {
        color: #1a5c2a;
        font-weight: 700;
        font-size: 0.92rem;
        margin-bottom: 12px;
        padding-bottom: 6px;
        border-bottom: 2px solid #c8ddc8;
    }

    /* ---------- hide streamlit chrome ---------- */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Generic data ──────────────────────────────────────────────────────────────
CLIENTES = ["Alfa Distribuidora", "Beta Comércio", "Gama Industrial", "Delta Suprimentos", "Épsilon Atacado"]
PRODUTOS  = ["Cabo PP 2x2,5mm", "Disjuntor 25A", "Tomada 20A", "Interruptor Simples", "Fio Flex 6mm", "Rele Temporizador"]
STATUS    = ["Ativo", "Inativo", "Pendente"]

random.seed(42)

def gerar_nfs(n=8):
    hoje = datetime.today()
    rows = []
    for i in range(n):
        data = hoje - timedelta(days=random.randint(1, 365))
        rows.append({
            "NF": f"{random.randint(10000,99999)}",
            "Data": data.strftime("%d/%m/%Y"),
            "Produto": random.choice(PRODUTOS),
            "Qtd": random.randint(1, 50),
            "Valor (R$)": f"{random.uniform(80, 4500):.2f}",
            "Status": random.choice(STATUS),
        })
    return pd.DataFrame(rows).sort_values("Data", ascending=False)

def gerar_historico(n=10):
    hoje = datetime.today()
    rows = []
    for i in range(n):
        data = hoje - timedelta(days=random.randint(1, 730))
        rows.append({
            "NF": f"{random.randint(10000,99999)}",
            "Data": data.strftime("%d/%m/%Y"),
            "Cliente": random.choice(CLIENTES),
            "Valor Total (R$)": f"{random.uniform(200, 15000):.2f}",
            "Itens": random.randint(1, 12),
            "Status": random.choice(STATUS),
        })
    return pd.DataFrame(rows).sort_values("Data", ascending=False)

df_nfs      = gerar_nfs()
df_historico = gerar_historico()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="sidebar-logo"><span>⚙ TPI</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown("**Cliente**")
    cliente_sel = st.text_input("", placeholder="Buscar cliente…", label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**Produto**")
    produto_sel = st.text_input("", placeholder="Buscar produto…", label_visibility="collapsed", key="prod")

    st.markdown("---")
    st.markdown("**Status**")
    status_sel = st.multiselect("", options=STATUS, default=[], label_visibility="collapsed")

# ── MAIN ──────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">📋 Histórico de Compra do Clientes</p>', unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
ultima_nf   = df_nfs["NF"].iloc[0]
ultima_data = df_nfs["Data"].iloc[0]
datas_dt    = pd.to_datetime(df_historico["Data"], dayfirst=True)
dias_ult    = (datetime.today() - datas_dt.max()).days
media_dias  = round((datas_dt.max() - datas_dt.min()).days / max(len(df_historico) - 1, 1))

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "🧾", "Última NF",         ultima_nf),
    (c2, "📅", "Última Data",        ultima_data),
    (c3, "🗓️", "Dias últ. compra",   f"{dias_ult} dias"),
    (c4, "📈", "Média de dias",       f"{media_dias} dias"),
]
for col, icon, label, value in cards:
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

# ── BODY: two columns (left wide, right narrow) ───────────────────────────────
left, right = st.columns([3, 1.1])

with left:
    # ── Itens da NF ──────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-box">'
        '<span class="section-title">Itens da NF</span>',
        unsafe_allow_html=True,
    )

    # apply filters
    df_view = df_nfs.copy()
    if produto_sel:
        df_view = df_view[df_view["Produto"].str.contains(produto_sel, case=False)]
    if status_sel:
        df_view = df_view[df_view["Status"].isin(status_sel)]

    def render_status(s):
        cls = "badge-active" if s == "Ativo" else "badge-inactive"
        return f'<span class="{cls}">{s}</span>'

    rows_html = ""
    for _, row in df_view.iterrows():
        rows_html += (
            f"<tr>"
            f"<td>{row['NF']}</td>"
            f"<td>{row['Data']}</td>"
            f"<td>{row['Produto']}</td>"
            f"<td>{row['Qtd']}</td>"
            f"<td>R$ {row['Valor (R$)']}</td>"
            f"<td>{render_status(row['Status'])}</td>"
            f"</tr>"
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
          <tbody>{rows_html}</tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Histórico de Compras ──────────────────────────────────────────────────
    st.markdown(
        '<div class="section-box">'
        '<span class="section-title">Histórico de Compras</span>',
        unsafe_allow_html=True,
    )

    df_hist_view = df_historico.copy()
    if cliente_sel:
        df_hist_view = df_hist_view[df_hist_view["Cliente"].str.contains(cliente_sel, case=False)]
    if status_sel:
        df_hist_view = df_hist_view[df_hist_view["Status"].isin(status_sel)]

    hist_rows = ""
    for _, row in df_hist_view.iterrows():
        hist_rows += (
            f"<tr>"
            f"<td>{row['NF']}</td>"
            f"<td>{row['Data']}</td>"
            f"<td>{row['Cliente']}</td>"
            f"<td>R$ {row['Valor Total (R$)']}</td>"
            f"<td>{row['Itens']}</td>"
            f"<td>{render_status(row['Status'])}</td>"
            f"</tr>"
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
          <tbody>{hist_rows}</tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── RIGHT PANEL ───────────────────────────────────────────────────────────────
with right:
    st.markdown(
        '<div class="right-panel">'
        '<div class="right-panel-title">📊 Resumo do Cliente</div>',
        unsafe_allow_html=True,
    )

    total_compras  = len(df_historico)
    total_valor    = df_historico["Valor Total (R$)"].astype(float).sum()
    cliente_top    = df_historico["Cliente"].value_counts().idxmax()
    ticket_medio   = total_valor / max(total_compras, 1)

    resumo_items = [
        ("🧾 Total de NFs",        str(total_compras)),
        ("💰 Volume total",         f"R$ {total_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
        ("🎯 Ticket médio",         f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
        ("👑 Cliente mais ativo",   cliente_top),
        ("📦 Produtos distintos",   str(df_nfs["Produto"].nunique())),
        ("📅 Período analisado",    "Últimos 24 meses"),
    ]

    for label, val in resumo_items:
        st.markdown(
            f"""
            <div style="padding:10px 0; border-bottom:1px solid #e8f0e8;">
              <div style="font-size:0.72rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">{label}</div>
              <div style="font-size:1rem;font-weight:700;color:#1a5c2a;">{val}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Mini chart ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="right-panel">'
        '<div class="right-panel-title">📈 Compras por Status</div>',
        unsafe_allow_html=True,
    )

    status_counts = df_historico["Status"].value_counts()
    chart_data    = pd.DataFrame({"Quantidade": status_counts})
    st.bar_chart(chart_data, color="#1a5c2a", height=200)

    st.markdown("</div>", unsafe_allow_html=True)