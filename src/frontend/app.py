# app.py
import sys
from pathlib import Path
import streamlit as st
import uuid

# Importação das funções internas
sys.path.append(str(Path(__file__).resolve().parent / "components"))
sys.path.append(str(Path(__file__).resolve().parent / "views"))
from views.chat import chat_interface
from auth import login_interface

STYLE_PATH = Path(__file__).resolve().parent / "styles" / "layout.css"

if STYLE_PATH.exists():
    st.markdown(f"<style>{STYLE_PATH.read_text()}</style>", unsafe_allow_html=True)
else:
    st.error(f"❌ Arquivo CSS não encontrado em: {STYLE_PATH.resolve()}")

st.set_page_config(page_title="Teobaldo - Assistente de Viagens", layout="centered")

if "cliente" not in st.session_state:
    st.session_state.cliente = None
if "chat" not in st.session_state:
    st.session_state.chat = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if st.session_state.cliente:
    chat_interface()
else:
    login_interface()
