"""
src/data/loader.py
──────────────────
Responsabilidade: fornecer os DataFrames para o dashboard.

Hoje: dados mock gerados localmente.
Amanhã: substitua o corpo de carregar_nfs() e carregar_historico()
por queries reais — o restante do projeto não muda.
"""

import random
from datetime import datetime, timedelta

import pandas as pd

# ── Constantes de domínio ─────────────────────────────────────────────────────
CLIENTES = [
    "Alfa Distribuidora",
    "Beta Comércio",
    "Gama Industrial",
    "Delta Suprimentos",
    "Épsilon Atacado",
]
PRODUTOS = [
    "Cabo PP 2x2,5mm",
    "Disjuntor 25A",
    "Tomada 20A",
    "Interruptor Simples",
    "Fio Flex 6mm",
    "Rele Temporizador",
]
STATUS = ["Ativo", "Inativo", "Pendente"]

# Seed fixa para reprodutibilidade durante desenvolvimento
random.seed(42)


# ── Interface pública ─────────────────────────────────────────────────────────

def carregar_nfs(n: int = 8) -> pd.DataFrame:
    """
    Retorna DataFrame com itens de NF.

    Colunas: NF | Data | Produto | Qtd | Valor (R$) | Status
    """
    hoje = datetime.today()
    rows = [
        {
            "NF":         str(random.randint(10000, 99999)),
            "Data":       (hoje - timedelta(days=random.randint(1, 365))).strftime("%d/%m/%Y"),
            "Produto":    random.choice(PRODUTOS),
            "Qtd":        random.randint(1, 50),
            "Valor (R$)": round(random.uniform(80, 4500), 2),
            "Status":     random.choice(STATUS),
        }
        for _ in range(n)
    ]
    return pd.DataFrame(rows).sort_values("Data", ascending=False).reset_index(drop=True)


def carregar_historico(n: int = 10) -> pd.DataFrame:
    """
    Retorna DataFrame com histórico de compras por cliente.

    Colunas: NF | Data | Cliente | Valor Total (R$) | Itens | Status
    """
    hoje = datetime.today()
    rows = [
        {
            "NF":               str(random.randint(10000, 99999)),
            "Data":             (hoje - timedelta(days=random.randint(1, 730))).strftime("%d/%m/%Y"),
            "Cliente":          random.choice(CLIENTES),
            "Valor Total (R$)": round(random.uniform(200, 15000), 2),
            "Itens":            random.randint(1, 12),
            "Status":           random.choice(STATUS),
        }
        for _ in range(n)
    ]
    return pd.DataFrame(rows).sort_values("Data", ascending=False).reset_index(drop=True)