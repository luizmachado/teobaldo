import streamlit as st
import json
import requests
import uuid
from pathlib import Path

# Cores customizadas (para usar via st.markdown)
PRIMARY_COLOR = "#d60b52"

# Caminho para o arquivo users.json
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
USERS_FILE = PROJECT_ROOT / "data" / "users.json"

# Endpoint da API
CHAT_API_URL = "http://localhost:8000/api/v1/chat"

# Função de autenticação
def autenticar(usuario, senha):
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for cliente in data.get("clientes", []):
        if cliente["documento"] == usuario and usuario == senha:
            return cliente
    return None

# Função para chamar o Teobaldo
def enviar_mensagem(user_id, message, thread_id):
    try:
        payload = {
            "user_id": str(user_id),
            "message": message,
            "thread_id": thread_id,
        }
        response = requests.post(CHAT_API_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Erro ao enviar mensagem: {e}"

# Interface
st.set_page_config(page_title="Teobaldo - Assistente de Viagens", layout="centered")
st.markdown(f"<h1 style='color:{PRIMARY_COLOR}'>Teobaldo</h1>", unsafe_allow_html=True)

if "cliente" not in st.session_state:
    st.session_state.cliente = None
if "chat" not in st.session_state:
    st.session_state.chat = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Login
if st.session_state.cliente is None:
    st.subheader("Login")
    usuario = st.text_input("Documento (CPF/CNPJ)")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        cliente = autenticar(usuario, senha)
        if cliente:
            st.session_state.cliente = cliente
            st.success(f"Bem-vindo(a), {cliente['nomeRazaoSocial']}!")
        else:
            st.error("Usuário ou senha inválidos.")
else:
    cliente = st.session_state.cliente
    st.subheader(f"Olá, {cliente['nomeRazaoSocial']}")
    st.markdown("Digite sua mensagem para o Teobaldo:")

    # Chat interface
    for entrada in st.session_state.chat:
        st.markdown(f"**Você:** {entrada['pergunta']}")
        st.markdown(f"**Teobaldo:** {entrada['resposta']}")

    pergunta = st.text_input("Sua pergunta", key="pergunta_input")
    if st.button("Enviar"):
        if pergunta.strip():
            resposta = enviar_mensagem(cliente["idCliente"], pergunta, st.session_state.thread_id)
            st.session_state.chat.append({
                "pergunta": pergunta,
                "resposta": resposta,
            })
            st.rerun()

    if st.button("Encerrar sessão"):
        st.session_state.cliente = None
        st.session_state.chat = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

