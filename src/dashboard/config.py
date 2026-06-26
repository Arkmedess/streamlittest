"""
src/dashboard/config.py
───────────────────────
Responsabilidade: configuração da página e injeção do CSS global.

Uma única chamada setup_page() no main.py é suficiente.
O CSS aqui é exatamente o do app.py original, sem alterações.
"""

import streamlit as st


def setup_page() -> None:
    """Configura a página e injeta o CSS global do tema TPI."""

    st.set_page_config(
        page_title="Histórico de Compra do Clientes",
        page_icon="🛒",
        layout="wide",
    )

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
        .badge-pending {
            background-color: #fff3cd;
            color: #856404;
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
        #MainMenu, footer, header { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )