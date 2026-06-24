"""
generate_hash.py
────────────────
Utilitário para gerar o hash SHA-256 das senhas antes de colocar
no secrets.toml.

Uso:
    python generate_hash.py

O script pede o salt (mesma string do secrets.toml) e a senha,
depois exibe o hash pronto para copiar.
"""

import hashlib
import getpass

print("=" * 55)
print("  Gerador de Hash de Senha – TPI Dashboard")
print("=" * 55)
print()

salt = getpass.getpass("Cole o password_salt do seu secrets.toml: ")
if not salt:
    salt = "tpi_default_salt"
    print(f"  (usando salt padrão: {salt})")

print()
while True:
    senha = getpass.getpass("Digite a senha (ou ENTER para sair): ")
    if not senha:
        break

    hashed = hashlib.sha256(f"{salt}{senha}".encode()).hexdigest()
    print(f"\n  ✅ Hash gerado:")
    print(f"  password_hash = \"{hashed}\"")
    print()

print("Pronto! Cole os hashes no seu .streamlit/secrets.toml")