import os
from typing import List
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langgraph.prebuilt import ToolNode
from langchain_chroma import Chroma
from langchain.prompts import load_prompt
from app.models.llm_factory import LLMFactory
from app.agent.state import AgentState
from app.tools.maps_tools import get_route_and_polyline
from app.tools.weather_tools import get_weather_forecast
from app.tools.partner_tools import find_partners_on_route

# Escolha do modelo padrão
llm = LLMFactory().get_model("gemini-default")

tools = [get_route_and_polyline, get_weather_forecast, find_partners_on_route]
llm_with_tools = llm.bind_tools(tools)

# Modelo para extração de memória
memory_extraction_llm = llm
embedding_model = OllamaEmbeddings(model="nomic-embed-text") 

# Configuração do banco de dados vetorial
vector_store = Chroma(
    persist_directory="src/vector_store",
    embedding_function=embedding_model
)
retriever = vector_store.as_retriever()


def call_model(state):
    """ Nó de Raciocínio """

    print("---NODE: CALL_MODEL---")
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def call_tools_and_update_state(state: AgentState) -> dict:
    """ Nó de Chamada de Tools """

    print("---NODE: CALL_TOOLS_AND_UPDATE_STATE---")
    last_message = state["messages"][-1]
    
    # Mapeia nomes de ferramentas para funções
    tool_map = {tool.name: tool for tool in tools}
    
    updates = {"messages": []}
    
    # Itera sobre todas as chamadas de ferramenta na última mensagem
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        if tool_name in tool_map:
            tool_to_call = tool_map[tool_name]
            tool_args = tool_call["args"]
            
            observation = tool_to_call.invoke(tool_args)
            
            # Se a ferramenta for a de rota, atualiza o estado
            if tool_name == "get_route_and_polyline":
                updates["route_info"] = observation
                updates["origin"] = observation.get("origin")
                updates["destination"] = observation.get("destination")
                
                # Resumo legível
                summary = observation.get("summary", "N/A")
                polyline = observation.get("polyline", "N/A")
                
                # Usamos um formato claro para que o LLM possa extrair a polyline facilmente.
                tool_content = f"Resumo da Rota: {summary}\nPolyline da Rota: {polyline}"
            else:
                tool_content = str(observation)

            # Adiciona a ToolMessage para o histórico da conversa
            updates["messages"].append(
                ToolMessage(content=tool_content, tool_call_id=tool_call["id"])
            )
            
    return updates

def update_long_term_memory(state):
    """ Nó da Memória de Longo Prazo """
    print("---NODE: UPDATE_LONG_TERM_MEMORY---")
    
    try:
        user_id = state.get("user_id")
        if not user_id:
            print("AVISO: O user_id não foi encontrado no estado. Pulando atualização de memória.")
            return {}

        chat_history_str = "\n".join(
            f"{msg.type}: {msg.content}" for msg in state["messages"]
        )
        

        # Prompt para instruir o LLM a extrair preferências
        mem_extraction_template = LLMFactory().get_prompt("memory_extraction")

        # Cria uma cadeia para extrair as preferências
        extraction_chain = mem_extraction_template | memory_extraction_llm
        
        # Invoca a cadeia com o histórico
        response_obj = extraction_chain.invoke({"chat_history": chat_history_str})
        extracted_info = response_obj.content
        
        print(f"Informação extraída para memória: {extracted_info}")

        # Se o LLM extrair uma preferência, salvar no banco de dados vetorial
        if extracted_info and "N/A" not in extracted_info:
            vector_store.add_texts(
                texts=[extracted_info],
                metadatas=[{"user_id": user_id}]
            )
            print(f"SUCESSO: Preferência salva para o usuário '{user_id}'.")

    except Exception as e:
        # ISSO IRÁ CAPTURAR O ERRO REAL E IMPRIMI-LO NO TERMINAL
        import traceback
        print("--- ERRO CRÍTICO EM UPDATE_LONG_TERM_MEMORY ---")
        print(f"TIPO DE EXCEÇÃO: {type(e).__name__}")
        print(f"MENSAGEM DE ERRO: {e}")
        print("RASTREAMENTO DO ERRO (TRACEBACK):")
        traceback.print_exc()
        print("---------------------------------------------")

    return {}
