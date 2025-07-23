# auth.py
from pathlib import Path
import json
import streamlit as st
import uuid

try:
    BASE_DIR = Path(__file__).resolve().parents[2]
    USERS_FILE = BASE_DIR / "data" / "users.json"

except IndexError:
    USERS_FILE = Path("src/data/users.json")


def check_credentials(usuario, senha):
    """Verifica as credenciais do usuário no arquivo JSON."""
    if not USERS_FILE.exists():
        st.error(f"Arquivo de usuários não encontrado em: {USERS_FILE.resolve()}")
        return None
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for cliente in data.get("clientes", []):
        # A senha deve ser igual ao documento (usuário)
        if cliente["documento"] == usuario and usuario == senha:
            return cliente
    return None

def login_interface():
    """Cria a interface de login com Streamlit."""
    st.markdown("<h3 class='text-center'>Login</h3>", unsafe_allow_html=True)
    
    usuario = st.text_input("Usuário (Documento)", key="login_usuario")
    senha = st.text_input("Senha", type="password", key="login_senha")

    if st.button("Entrar", key="login_button"):
        if not usuario or not senha:
            st.warning("Por favor, preencha usuário e senha.")
            return

        cliente_logado = check_credentials(usuario, senha)

        if cliente_logado:
            st.session_state.cliente = cliente_logado
            st.session_state.chat = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
