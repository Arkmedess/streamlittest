"""
src/dashboard/config.py
───────────────────────
Responsabilidade: configuração da página e injeção do CSS global.
"""

import streamlit as st


def setup_page() -> None:
    """Configura a página e injeta o CSS global do tema TPI (Soft UI)."""

    st.set_page_config(
        page_title="Histórico de Compra do Clientes",
        page_icon="🛒",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        :root {
            --tpi-green-900: #0f5a2d;
            --tpi-green-800: #1a6b36;
            --tpi-green-700: #2a7e48;
            --bg-soft: #eef2ee;
            --bg-card: #f8fbf8;
            --text-main: #173f25;
            --text-muted: #6e7f74;
            --line-soft: #d3dfd4;
            --shadow-soft: 10px 10px 20px rgba(171, 186, 175, 0.34), -8px -8px 18px rgba(255, 255, 255, 0.85);
            --shadow-inset: inset 2px 2px 4px rgba(170, 184, 171, 0.28), inset -2px -2px 4px rgba(255, 255, 255, 0.88);
            --radius-card: 22px;
            --radius-pill: 999px;
            --font-body: clamp(0.96rem, 0.92rem + 0.15vw, 1.02rem);
            --font-small: clamp(0.82rem, 0.78rem + 0.14vw, 0.9rem);
            --font-title: clamp(1.6rem, 1.3rem + 1.2vw, 2.35rem);
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
            background: linear-gradient(180deg, #f7faf7 0%, var(--bg-soft) 100%);
            font-family: "Segoe UI", "Trebuchet MS", sans-serif;
            color: var(--text-main);
            font-size: var(--font-body);
        }

        [data-testid="stMainBlockContainer"] {
            padding-top: 1.1rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f5a2d 0%, #0e4f29 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.12);
            padding-top: 0 !important;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .stTextInput input {
            background: rgba(245, 250, 247, 0.96) !important;
            color: #114525 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.45) !important;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.12);
        }

        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
            background: rgba(245, 250, 247, 0.96) !important;
            color: #114525 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.45) !important;
            min-height: 2.35rem;
        }

        [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
            padding-top: 2px;
        }

        [data-testid="stSidebar"] .stDateInput input,
        [data-testid="stSidebar"] div[data-baseweb="input"] input {
            background: rgba(245, 250, 247, 0.96) !important;
            color: #114525 !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.45) !important;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.12);
        }

        [data-testid="stSidebar"] label {
            font-weight: 700;
            font-size: 0.9rem;
            letter-spacing: 0.1px;
        }

        .sidebar-logo {
            background: transparent;
            padding: 10px 4px 14px 4px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.23);
            margin-bottom: 16px;
        }

        .sidebar-logo-symbol {
            width: 36px;
            height: 36px;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.12);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 6px;
            box-shadow: inset 1px 1px 3px rgba(255, 255, 255, 0.2), inset -2px -2px 4px rgba(0, 0, 0, 0.2);
        }

        .sidebar-logo-symbol svg {
            width: 100%;
            height: 100%;
            fill: none;
            stroke: #ffffff;
            stroke-width: 1.7;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        .sidebar-logo-text {
            font-size: 2rem;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: 1.2px;
            line-height: 1;
        }

        .sidebar-date-range {
            margin-top: 8px;
            font-size: 0.76rem;
            color: rgba(255, 255, 255, 0.95);
            text-align: center;
        }

        .sidebar-date-box {
            background: rgba(255, 255, 255, 0.13);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 6px 8px;
            text-align: center;
            font-size: 0.76rem;
            font-weight: 600;
        }

        /* Header */
        .header-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 18px;
            align-items: stretch;
        }

        .header-grid > div[data-testid="column"] {
            flex: 1 1 240px;
        }

        .header-grid .stDownloadButton {
            width: 100%;
            height: 100%;
        }

        .header-shell {
            background: var(--bg-card);
            border: 1px solid var(--line-soft);
            border-radius: var(--radius-card);
            box-shadow: var(--shadow-soft);
            padding: 14px 16px;
            margin-bottom: 14px;
        }

        .main-header {
            color: var(--text-main);
            font-size: var(--font-title);
            font-weight: 800;
            margin: 0;
            line-height: 1.1;
        }

        .header-subtitle {
            color: var(--text-muted);
            font-size: var(--font-small);
            margin-top: 4px;
        }

        /* Buttons */
        .stDownloadButton button,
        .stButton button {
            border-radius: 12px !important;
            border: 1px solid #d2dfd3 !important;
            background: linear-gradient(145deg, #f5faf5, #e7f1e8) !important;
            color: #114727 !important;
            font-weight: 700 !important;
            box-shadow: 4px 4px 10px rgba(174, 187, 177, 0.35), -4px -4px 10px rgba(255, 255, 255, 0.82) !important;
            min-height: 40px;
        }

        .stDownloadButton button:hover,
        .stButton button:hover {
            border-color: #bdd1bf !important;
            background: linear-gradient(145deg, #f8fcf8, #ebf4ec) !important;
            color: #0d3c20 !important;
        }

        /* KPI cards */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }

        .metric-card {
            background: var(--bg-card);
            border-radius: var(--radius-card);
            border: 1px solid var(--line-soft);
            padding: 16px 18px;
            display: flex;
            align-items: center;
            gap: 14px;
            box-shadow: var(--shadow-soft);
            min-height: 84px;
            height: 100%;
        }

        .metric-icon {
            background: #dff2e5;
            border: 1px solid #b9e0c4;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--tpi-green-800);
            font-size: 1.05rem;
            font-weight: 700;
            box-shadow: 0 6px 12px rgba(20, 80, 46, 0.18);
            flex-shrink: 0;
        }

        .metric-icon svg {
            width: 22px;
            height: 22px;
            fill: none;
            stroke: currentColor;
            stroke-width: 1.7;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        .metric-label {
            font-size: clamp(0.68rem, 0.62rem + 0.28vw, 0.85rem);
            color: var(--text-muted);
            margin-bottom: 2px;
            text-transform: uppercase;
            letter-spacing: 0.55px;
            font-weight: 700;
        }

        .metric-value {
            font-size: clamp(1.1rem, 1rem + 0.4vw, 1.52rem);
            font-weight: 750;
            color: var(--text-main);
        }

        .content-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 22px;
            align-items: stretch;
        }

        .content-grid > div[data-testid="column"] {
            flex: 1 1 360px;
        }

        .content-grid > div[data-testid="column"]:last-child {
            flex: 0 0 340px;
            max-width: 420px;
        }

        /* Section cards */
        .section-box {
            background: var(--bg-card);
            border-radius: var(--radius-card);
            border: 1px solid var(--line-soft);
            padding: 18px 20px;
            box-shadow: var(--shadow-soft);
            margin-bottom: 16px;
        }

        .section-title {
            background: linear-gradient(145deg, var(--tpi-green-700), var(--tpi-green-900));
            color: #ffffff;
            font-weight: 700;
            font-size: 0.84rem;
            border-radius: var(--radius-pill);
            display: inline-block;
            padding: 5px 14px;
            margin-bottom: 14px;
        }

        /* Tables */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: clamp(0.78rem, 0.72rem + 0.25vw, 0.95rem);
        }

        .styled-table thead th {
            background-color: #e3ece4;
            color: var(--text-main);
            font-weight: 700;
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid #ccdbce;
            white-space: nowrap;
        }

        .styled-table tbody tr:nth-child(even) {
            background-color: #f1f6f2;
        }

        .styled-table tbody td {
            padding: 9px 12px;
            border-bottom: 1px solid #e5ece6;
            color: #2e3f33;
            white-space: nowrap;
        }

        .table-scroll {
            max-height: 52vh;
            overflow-y: auto;
            border-radius: 18px;
            border: 1px solid #d9e4da;
            background: #fbfdfb;
            box-shadow: var(--shadow-inset);
        }

        .pager-text {
            color: var(--text-muted);
            font-size: var(--font-small);
            text-align: center;
            margin-top: 10px;
        }

        /* Badges */
        .badge-active {
            background-color: #d9f1df;
            color: #1b6a34;
            border-radius: var(--radius-pill);
            padding: 3px 11px;
            font-size: 0.75rem;
            font-weight: 700;
            border: 1px solid #bde2c6;
        }

        .badge-warning {
            background-color: #fff1c9;
            color: #875f00;
            border-radius: var(--radius-pill);
            padding: 3px 11px;
            font-size: 0.75rem;
            font-weight: 700;
            border: 1px solid #efd68a;
        }

        .badge-inactive {
            background-color: #f8d9d9;
            color: #912f2f;
            border-radius: var(--radius-pill);
            padding: 3px 11px;
            font-size: 0.75rem;
            font-weight: 700;
            border: 1px solid #edb8b8;
        }

        .badge-pending {
            background-color: #fff1c9;
            color: #875f00;
            border-radius: var(--radius-pill);
            padding: 3px 11px;
            font-size: 0.75rem;
            font-weight: 700;
            border: 1px solid #efd68a;
        }

        /* Right-side cards */
        .right-panel {
            background: var(--bg-card);
            border-radius: var(--radius-card);
            border: 1px solid var(--line-soft);
            padding: 18px 20px;
            box-shadow: var(--shadow-soft);
            margin-bottom: 14px;
        }

        .right-panel-title {
            color: var(--text-main);
            font-weight: 700;
            font-size: 0.92rem;
            margin-bottom: 12px;
            padding-bottom: 6px;
            border-bottom: 1px solid #cfdbd0;
        }

        .insight-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 10px;
        }

        .insight-item {
            background: #edf4ee;
            border-radius: 14px;
            padding: 14px 12px;
            text-align: center;
            box-shadow: var(--shadow-inset);
        }

        .insight-label {
            font-size: clamp(0.65rem, 0.6rem + 0.25vw, 0.82rem);
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.35px;
            font-weight: 700;
        }

        .insight-value {
            font-size: clamp(1rem, 0.92rem + 0.35vw, 1.28rem);
            font-weight: 750;
            color: var(--text-main);
            margin-top: 6px;
        }

        .status-legend {
            margin-top: 8px;
            color: #4e6455;
            font-size: var(--font-small);
            line-height: 1.45;
        }

        @media (max-width: 1260px) {
            .header-grid {
                flex-direction: column;
            }
            .header-grid > div[data-testid="column"] {
                width: 100% !important;
            }
            .header-shell {
                margin-bottom: 0;
            }
        }

        @media (max-width: 1024px) {
            [data-testid="stMainBlockContainer"] {
                padding-left: 1rem;
                padding-right: 1rem;
            }
            .metric-grid {
                gap: 14px;
            }
            .section-box,
            .right-panel {
                padding: 16px;
            }
            .content-grid {
                flex-direction: column;
            }
            .content-grid > div[data-testid="column"]:last-child {
                max-width: none;
                flex: 1 1 auto;
            }
        }

        @media (max-width: 768px) {
            .metric-grid {
                grid-template-columns: 1fr;
            }
            .header-grid {
                gap: 12px;
            }
            .header-shell {
                padding: 12px;
            }
            .table-scroll {
                max-height: 60vh;
            }
            .status-legend {
                font-size: 0.82rem;
            }
            .content-grid {
                gap: 16px;
            }
            .right-panel,
            .section-box {
                padding: 14px;
            }
        }

        /* Hide Streamlit chrome */
        #MainMenu, footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )
