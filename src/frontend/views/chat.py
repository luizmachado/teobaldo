import streamlit as st
from components.chat_utils import enviar_mensagem
from components.ui import chat_bubble_user, chat_bubble_bot
import uuid

def chat_interface():
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        cliente = st.session_state.cliente
        st.markdown(f"## Olá, {cliente['nomeRazaoSocial'].split()[0]}!", unsafe_allow_html=True)
        st.markdown("Fale com o Teobaldo para planejar sua viagem:")
    
    with col2:
        if st.button("🚪", key="logout_button"):
            st.session_state.cliente = None
            st.session_state.chat = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()

    st.divider()

    # Histórico de mensagens
    for entrada in st.session_state.chat:
        chat_bubble_user(entrada["pergunta"])
        chat_bubble_bot(entrada["resposta"])

    if prompt := st.chat_input("Digite sua pergunta..."):
        resposta = enviar_mensagem(
            cliente["idCliente"], prompt, st.session_state.thread_id
        )
        st.session_state.chat.append({
            "pergunta": prompt,
            "resposta": resposta,
        })
        st.rerun()
