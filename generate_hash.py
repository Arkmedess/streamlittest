"""
generate_hash.py
────────────────
Utilitário de linha de comando para gerar os hashes de senha
que vão no secrets.toml.

Uso:
    python generate_hash.py
"""

import hashlib
import getpass

print()
print("=" * 50)
print("  Gerador de Hash – TPI Dashboard")
print("=" * 50)
print()

salt = getpass.getpass("Cole o password_salt do secrets.toml: ").strip()
if not salt:
    salt = "tpi_salt_padrao"
    print(f"  (usando salt padrão: {salt})")

print()
while True:
    senha = getpass.getpass("Senha (ENTER para sair): ").strip()
    if not senha:
        break
    hashed = hashlib.sha256(f"{salt}{senha}".encode()).hexdigest()
    print(f"\n  ✅  password_hash = \"{hashed}\"\n")

print("Pronto! Cole os valores acima no .streamlit/secrets.toml")