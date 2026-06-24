"""
main.py
───────
Ponto de entrada da aplicação.
Responsabilidade: orquestrar autenticação → dashboard.

Execute:
    streamlit run main.py

O app.py NÃO foi modificado.
"""

import runpy
import streamlit as st
from auth import require_login, render_logout_button

# 1️⃣  Guard – para aqui se não estiver logado
require_login()

# 2️⃣  Injeta o botão de logout na sidebar (antes do dashboard renderizar)
render_logout_button()

# 3️⃣  Executa o dashboard original sem nenhuma alteração
runpy.run_path("app.py", run_name="__main__")