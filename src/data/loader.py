"""Carregamento e transformação de dados de vendas para o dashboard."""

from __future__ import annotations

import pandas as pd

from src.data.supabase_client import fetch_vendas
from src.logging import setup_logger

logger = setup_logger(__name__)


BASE_COLUMNS = [
    "cliente_nome_fantasia",
    "cidade",
    "uf",
    "email_cliente",
    "data_faturamento",
    "tipo_operacao",
    "status",
    "pedido_venda",
    "nota_fiscal",
    "prd",
    "descricao_produto",
    "qtd",
    "vlr_total_mercadoria",
    "vlr_total_nf",
]


def _empty_base() -> pd.DataFrame:
    return pd.DataFrame(columns=BASE_COLUMNS)


def _normalize_base(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return _empty_base()

    base = df.copy()

    for col in BASE_COLUMNS:
        if col not in base.columns:
            base[col] = None

    base = base[BASE_COLUMNS]

    base["data_faturamento"] = pd.to_datetime(base["data_faturamento"], errors="coerce")
    base = base[base["data_faturamento"].notna()].copy()

    for col in ["qtd", "vlr_total_mercadoria", "vlr_total_nf"]:
        base[col] = pd.to_numeric(base[col], errors="coerce")

    base["cliente_nome_fantasia"] = base["cliente_nome_fantasia"].fillna("Não Informado").astype(str)
    base["cidade"] = base["cidade"].fillna("Não Informado").astype(str)
    base["uf"] = base["uf"].fillna("--").astype(str)
    base["tipo_operacao"] = base["tipo_operacao"].fillna("Não Informado").astype(str)
    base["status"] = base["status"].fillna("Não Informado").astype(str)
    base["pedido_venda"] = base["pedido_venda"].fillna("Não Informado").astype(str)
    base["nota_fiscal"] = base["nota_fiscal"].fillna("Não Informado").astype(str)
    base["prd"] = base["prd"].fillna("Não Informado").astype(str)
    base["descricao_produto"] = base["descricao_produto"].fillna("Não Informado").astype(str)

    base = base.sort_values("data_faturamento", ascending=False).reset_index(drop=True)
    return base


def carregar_base() -> pd.DataFrame:
    """Busca os dados de vendas da fonte real (Supabase) e normaliza o schema."""
    try:
        raw = fetch_vendas()
    except Exception:
        logger.exception("Falha ao carregar base de vendas. Retornando base vazia.")
        return _empty_base()

    return _normalize_base(raw)


def filtrar_base(df: pd.DataFrame, filtros: dict) -> pd.DataFrame:
    """Aplica filtros cruzados ao dataframe base."""
    if df.empty:
        return df.copy()

    view = df.copy()

    cliente = (filtros.get("cliente") or "").strip()
    if cliente:
        view = view[
            view["cliente_nome_fantasia"].str.contains(cliente, case=False, na=False)
        ]

    for filtro, col in [
        ("cidade", "cidade"),
        ("estado", "uf"),
        ("codigo_produto", "prd"),
        ("descricao_produto", "descricao_produto"),
        ("pedido_venda", "pedido_venda"),
    ]:
        val = filtros.get(filtro)
        if val and val != "Todos":
            view = view[view[col] == val]

    intervalo = filtros.get("data_intervalo")
    if intervalo:
        data_inicio = pd.to_datetime(intervalo[0])
        data_fim = pd.to_datetime(intervalo[1])
        view = view[
            (view["data_faturamento"] >= data_inicio)
            & (view["data_faturamento"] <= data_fim)
        ]

    return view.reset_index(drop=True)


def carregar_nfs() -> pd.DataFrame:
    """Compatibilidade: retorna visão granular já no formato da tabela de itens."""
    base = carregar_base()
    if base.empty:
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

    view = base.copy()
    view["valor_unitario"] = view["vlr_total_mercadoria"] / view["qtd"].replace(0, pd.NA)

    return pd.DataFrame(
        {
            "NF": view["nota_fiscal"],
            "Data": view["data_faturamento"].dt.strftime("%d/%m/%Y"),
            "Cód. Produto": view["prd"],
            "Descrição de Produto": view["descricao_produto"],
            "Qtd": view["qtd"],
            "Valor Unitário": view["valor_unitario"],
            "Total Mercadoria": view["vlr_total_mercadoria"],
            "Status Item": view["status"],
            "Pedido de Venda": view["pedido_venda"],
        }
    )


def carregar_historico() -> pd.DataFrame:
    """Compatibilidade: retorna visão consolidada por NF + cliente."""
    base = carregar_base()
    if base.empty:
        return pd.DataFrame(
            columns=[
                "NF",
                "Data Faturamento",
                "Cliente",
                "Valor Total NF",
                "Operação",
                "Cidade",
                "Estado",
            ]
        )

    hist = (
        base.groupby(
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
