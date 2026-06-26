"""
src/dashboard/components/shared.py
────────────────────────────────────
Responsabilidade: helpers HTML reutilizáveis entre componentes.
Não faz chamadas ao Streamlit — retorna apenas strings HTML.
"""


def render_badge(status: str) -> str:
    """Retorna o HTML do badge colorido de status."""
    cls = {
        "Ativo":    "badge-active",
        "Inativo":  "badge-inactive",
        "Pendente": "badge-pending",
    }.get(status, "badge-pending")
    return f'<span class="{cls}">{status}</span>'


def brl(valor: float) -> str:
    """Formata float como moeda BRL: R$ 1.234,56"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")