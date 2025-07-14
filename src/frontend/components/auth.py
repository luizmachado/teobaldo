import streamlit as st
import json
from pathlib import Path

USERS_FILE = Path("data/users.json")

def autenticar(usuario, senha):
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for cliente in data.get("clientes", []):
        if cliente["documento"] == usuario and usuario == senha:
            return cliente
    return None

def login():
    st.subheader("Login")
    usuario = st.text_input("Documento (CPF/CNPJ)")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        cliente = autenticar(usuario, senha)
        if cliente:
            st.session_state.cliente = cliente
            st.success(f"Bem-vindo(a), {cliente['nomeRazaoSocial']}!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

