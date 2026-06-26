"""
src/data/supabase_client.py
────────────────────────────
Estratégia: REPLACE TOTAL (delete + insert)

O banco sempre reflete exatamente o CSV atual.
Linhas removidas do CSV somem do banco.
Linhas novas entram. Linhas alteradas são substituídas.

Fluxo:
    1. Autentica
    2. DELETE sem filtro (esvazia a tabela respeitando RLS)
    3. INSERT em lotes do DataFrame inteiro
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from supabase import Client, create_client


# ── Helpers ───────────────────────────────────────────────────────────────────

def _chunks(lista: list, tamanho: int):
    for i in range(0, len(lista), tamanho):
        yield lista[i : i + tamanho]


def _autenticar() -> tuple[Client, str]:
    """Cria o client, autentica e retorna (client, user_uuid)."""
    url      = st.secrets["supabase"]["url"]
    key      = st.secrets["supabase"]["key"]
    email    = st.secrets["supabase"]["user_email"]
    password = st.secrets["supabase"]["user_password"]

    client: Client = create_client(url, key)

    sessao = client.auth.sign_in_with_password(
        {"email": email, "password": password}
    )

    if not sessao.session or not sessao.session.access_token:
        raise PermissionError("Token JWT não obtido. Verifique as credenciais.")

    if sessao.user is None:
        raise PermissionError("Usuário não retornado pelo Supabase.")

    print(f"✅ Autenticado como: {sessao.user.email} ({sessao.user.id})")
    return client, sessao.user.id


def _preparar_df(df: pd.DataFrame, user_uuid: str) -> list[dict]:
    """Serializa o DataFrame injetando user_id antes do to_dict."""
    df_envio = df.copy()
    df_envio["user_id"] = user_uuid

    for col in df_envio.columns:
        if pd.api.types.is_datetime64_any_dtype(df_envio[col]):
            df_envio[col] = df_envio[col].dt.strftime("%Y-%m-%d")
        elif df_envio[col].dtype == "object":
            df_envio[col] = df_envio[col].astype(str)

    return df_envio.to_dict(orient="records")


def fetch_vendas() -> pd.DataFrame:
    """Busca todas as linhas da tabela `vendas` do usuário autenticado."""
    client, _ = _autenticar()

    response = client.table("vendas").select("*").execute()
    dados = response.data or []

    return pd.DataFrame(dados)


# ── Interface pública ─────────────────────────────────────────────────────────

def replace_vendas(df: pd.DataFrame, lote: int = 500) -> None:
    """
    Substitui TODA a tabela 'vendas' pelo conteúdo do DataFrame.

    Passos:
        1. Apaga todas as linhas do usuário autenticado (respeita RLS)
        2. Insere o DataFrame inteiro em lotes

    Args:
        df:   DataFrame já com colunas mapeadas (≤ 63 chars)
        lote: tamanho do batch de insert (padrão 500 linhas)
    """
    client, user_uuid = _autenticar()

    # ── 1. Apaga tudo ─────────────────────────────────────────────────────────
    # neq("user_id", "") → condição sempre verdadeira para o RLS do usuário
    print("🗑️  Limpando tabela vendas...")
    client.table("vendas").delete().eq("user_id", user_uuid).execute()
    print("✅ Tabela limpa.")

    # ── 2. Insere o DataFrame inteiro ─────────────────────────────────────────
    dados    = _preparar_df(df, user_uuid)
    total    = len(dados)
    enviados = 0

    print(f"📤 Inserindo {total} linhas em lotes de {lote}...")

    try:
        for lote_atual in _chunks(dados, lote):
            client.table("vendas").insert(lote_atual).execute()
            enviados += len(lote_atual)
            print(f"  → {enviados}/{total}")

        print(f"✅ Replace concluído: {total} linhas no banco.")

    except Exception as e:
        print(f"❌ Erro após {enviados}/{total} linhas: {e}")
        print("⚠️  A tabela foi limpa mas o insert falhou. Rode novamente.")
        raise