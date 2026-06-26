"""
src/auth/service.py
───────────────────
Responsabilidade exclusiva: autenticação e controle de sessão.

Não conhece o dashboard. Não renderiza CSS do dashboard.
Interface pública (consumida via src/auth/__init__.py):

    require_login()        → guard: para execução se não autenticado
    render_logout_button() → widget de logout na sidebar
    get_current_user()     → dict com dados do usuário logado
"""

import hashlib
import hmac
import time

import streamlit as st

# ── Configurações ─────────────────────────────────────────────────────────────
SESSION_TIMEOUT_MIN = 30
MAX_ATTEMPTS        = 5
LOCKOUT_SECONDS     = 300


# ══════════════════════════════════════════════════════════════════════════════
# PRIVADO
# ══════════════════════════════════════════════════════════════════════════════

def _salt() -> str:
    return st.secrets.get("auth", {}).get("password_salt", "tpi_salt_padrao")


def _hash(password: str) -> str:
    return hashlib.sha256(f"{_salt()}{password}".encode()).hexdigest()


def _verify(plain: str, hashed: str) -> bool:
    return hmac.compare_digest(_hash(plain), hashed)


def _load_users() -> dict:
    try:
        return dict(st.secrets["users"])
    except KeyError:
        st.error("⚠️ Seção [users] ausente no secrets.toml.")
        st.stop()


# ── Rate-limit ────────────────────────────────────────────────────────────────

def _init_rate_limit():
    st.session_state.setdefault("_login_attempts", 0)
    st.session_state.setdefault("_lockout_until", 0.0)


def _locked() -> bool:
    return time.time() < st.session_state.get("_lockout_until", 0)


def _lockout_remaining() -> tuple[int, int]:
    secs = max(0, int(st.session_state["_lockout_until"] - time.time()))
    return secs // 60, secs % 60


def _fail():
    st.session_state["_login_attempts"] += 1
    if st.session_state["_login_attempts"] >= MAX_ATTEMPTS:
        st.session_state["_lockout_until"] = time.time() + LOCKOUT_SECONDS
        st.session_state["_login_attempts"] = 0


def _reset_rate_limit():
    st.session_state["_login_attempts"] = 0
    st.session_state["_lockout_until"]  = 0.0


# ── Sessão ────────────────────────────────────────────────────────────────────

def _logout():
    for k in ("_authenticated", "_username", "_nome", "_role", "_last_activity"):
        st.session_state.pop(k, None)


def _touch():
    st.session_state["_last_activity"] = time.time()


def _check_timeout():
    last = st.session_state.get("_last_activity", time.time())
    if time.time() - last > SESSION_TIMEOUT_MIN * 60:
        _logout()
        st.warning("⏱️ Sessão expirada por inatividade. Faça login novamente.")
        st.rerun()
    _touch()


# ── Tela de login ─────────────────────────────────────────────────────────────

def _render_login():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #f0f4f0;
            font-family: 'Segoe UI', sans-serif;
        }
        #MainMenu, footer, header { visibility: hidden; }
        .login-logo {
            text-align: center;
            font-size: 2rem;
            font-weight: 900;
            color: #1a5c2a;
            letter-spacing: 4px;
            margin-bottom: 4px;
        }
        .login-sub {
            text-align: center;
            color: #888;
            font-size: 0.82rem;
            margin-bottom: 28px;
        }
        </style>
    """, unsafe_allow_html=True)

    _init_rate_limit()

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="login-logo">⚙ TPI</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Histórico de Compra do Clientes</div>', unsafe_allow_html=True)

        if _locked():
            m, s = _lockout_remaining()
            st.error(f"🔒 Conta bloqueada. Aguarde {m}m {s}s.")
            return

        with st.form("_login_form", clear_on_submit=False):
            username  = st.text_input("👤 Usuário", placeholder="seu.usuario")
            password  = st.text_input("🔑 Senha",   placeholder="••••••••", type="password")
            submitted = st.form_submit_button("Entrar", width='stretch')

        if submitted:
            users     = _load_users()
            user_data = users.get(username)

            if user_data and _verify(password, user_data["password_hash"]):
                _reset_rate_limit()
                st.session_state["_authenticated"] = True
                st.session_state["_username"]      = username
                st.session_state["_nome"]          = user_data.get("nome", username)
                st.session_state["_role"]          = user_data.get("role", "viewer")
                st.session_state["_last_activity"] = time.time()
                st.rerun()
            else:
                _fail()
                remaining = MAX_ATTEMPTS - st.session_state["_login_attempts"]
                if remaining > 0:
                    st.error(f"❌ Credenciais inválidas. {remaining} tentativa(s) restante(s).")
                else:
                    st.error("🔒 Muitas tentativas. Conta bloqueada temporariamente.")


# ══════════════════════════════════════════════════════════════════════════════
# PÚBLICO
# ══════════════════════════════════════════════════════════════════════════════

def require_login() -> None:
    if not st.session_state.get("_authenticated", False):
        _render_login()
        st.stop()
    _check_timeout()


def render_logout_button() -> None:
    nome = st.session_state.get("_nome", "Usuário")
    role = st.session_state.get("_role", "")
    st.sidebar.markdown(
        f"""
        <div style="margin-top:24px;padding-top:12px;border-top:1px solid #2d7a40;">
            <div style="font-size:0.68rem;opacity:0.65;">Logado como</div>
            <div style="font-weight:700;font-size:0.95rem;">{nome}</div>
            <div style="font-size:0.70rem;opacity:0.55;text-transform:uppercase;
                        letter-spacing:0.5px;">{role}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.sidebar.button("🚪 Sair", width='stretch', key="_logout_btn"):
        _logout()
        st.rerun()


def get_current_user() -> dict:
    return {
        "username": st.session_state.get("_username", ""),
        "nome":     st.session_state.get("_nome", ""),
        "role":     st.session_state.get("_role", "viewer"),
    }