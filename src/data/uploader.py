# src/data/uploader.py

import pandas as pd

from decimal import Decimal
from pydantic import ValidationError

from .mapper import COLUMN_MAP, CSV_COLUMNS
from .schema import Venda

def _to_decimal(valor):

    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    if valor in ("", "N/D"):
        return None

    return Decimal(
        valor.replace(".", "")
             .replace(",", ".")
    )

def _read_csv(file):

    return pd.read_csv(
        file,
        sep=";",
        usecols=CSV_COLUMNS,
        dtype=str,
        encoding="utf-8",
    )

def _rename_columns(df):

    return df.rename(columns=COLUMN_MAP)

def _clean_data(df):

    df = df.replace("N/D", None)

    return df

def _convert_types(df):

    df["data_faturamento"] = pd.to_datetime(
        df["data_faturamento"],
        format="%d/%m/%Y",
        errors="coerce",
    ).dt.date

    df["qtd"] = df["qtd"].apply(_to_decimal)

    df["vlr_total_mercadoria"] = (
        df["vlr_total_mercadoria"]
        .apply(_to_decimal)
    )

    df["vlr_total_nf"] = (
        df["vlr_total_nf"]
        .apply(_to_decimal)
    )

    return df

def _validate_dataframe(df):

    if df["data_faturamento"].isna().any():
        raise ValueError(
            "Existem datas de faturamento inválidas."
        )

    campos_obrigatorios = [
        "pedido_venda",
        "nota_fiscal",
        "prd",
        "descricao_produto",
        "cliente_nome_fantasia",
    ]

    for campo in campos_obrigatorios:

        if df[campo].isna().any():

            raise ValueError(
                f"Campo obrigatório ausente: {campo}"
            )
        
def _validate_schema(df):

    registros = []
    erros = []

    for idx, row in enumerate(
        df.to_dict("records"),
        start=1,
    ):

        try:

            venda = Venda.model_validate(row)

            registros.append(
                venda.model_dump()
            )

        except ValidationError as e:

            erros.append(
                {
                    "linha": idx,
                    "erro": str(e),
                }
            )

    if erros:

        print("\n=== EXEMPLOS DE ERROS DE VALIDAÇÃO DO PYDANTIC ===")
        # Mostra os 5 primeiros erros para entender o padrão
        for i, erro in enumerate(erros[:5]):
            print(f"Erro {i+1}: {erro}")
        print("==================================================\n")

        raise ValueError(
            f"Foram encontradas {len(erros)} linhas inválidas."
        )

    return pd.DataFrame(registros)

def processar_csv(file):

    df = _read_csv(file)

    df = _rename_columns(df)

    df = df[df['status'] == 'Faturado']

    df['email_cliente'] = df['email_cliente'].astype(str).str.split(',').str[0].str.strip()

    df = _clean_data(df)

    df = _convert_types(df)

    _validate_dataframe(df)

    df['cidade'] = df['cidade'].fillna("Não Informado").astype(str)

    df = _validate_schema(df)

    return df