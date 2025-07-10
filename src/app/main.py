import streamlit as st
from app.agent.graph import app_graph
from app.agent.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

st.set_page_config(page_title="SuperApp - Semp Parar", layout="centered")

st.title("SuperApp Sem Parar")

# Estado da sessão
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content=(
            """
            Você é um assistente virtual especializado em viagens para clientes do Sem Parar.
            Seu papel é ajudar o usuário a planejar deslocamentos, sugerindo rotas otimizadas,
            indicando parceiros (postos de combustível, estacionamentos, pedágios etc.) e
            informando sobre as condições climáticas ao longo do trajeto.
            
            Seja proativo, ofereça vantagens quando possível e garanta uma experiência fluida e personalizada.
            Sempre que necessário, solicite informações de origem e destino para fornecer as melhores recomendações.
            """.strip()
        ))
    ]

    st.session_state.user_id = "user-001"

def process_user_input(user_input):
    """ Função para processar a mensagem do usuário """

    # Adiciona a mensagem do usuário
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Prepara o estado inicial para o grafo
    agent_state: AgentState = {
        "messages": st.session_state.chat_history,
        "user_id": st.session_state.user_id,
    }

    # Executa o grafo
    final_state = app_graph.invoke(agent_state)

    # Recupera e adiciona resposta do modelo
    final_response = final_state["messages"][-1]
    st.session_state.chat_history.append(final_response)


# Input do usuário
with st.form("chat-form", clear_on_submit=True):
    user_input = st.text_input("Digite sua mensagem:", "")
    submitted = st.form_submit_button("Enviar")
    if submitted and user_input.strip():
        process_user_input(user_input)

# Mostra o histórico do chat
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").markdown(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").markdown(msg.content)

