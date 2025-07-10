from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import call_model, call_tools, update_long_term_memory

def should_continue(state):
    last_message = state["messages"][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        # Se o LLM chamar, vá para o nó de ferramentas
        return "call_tools"
    else:
        # Se não há chamada de ferramenta.
        return "update_memory"

# Constrói o grafo
workflow = StateGraph(AgentState)

# Adiciona os nós
workflow.add_node("call_model", call_model)
workflow.add_node("call_tools", call_tools)
workflow.add_node("update_memory", update_long_term_memory)

# Define o ponto de entrada
workflow.set_entry_point("call_model")

# Adiciona as arestas
workflow.add_conditional_edges(
    "call_model",
    should_continue,
    {
        "call_tools": "call_tools",
        "update_memory": "update_memory",
    }
)
# Volte para o modelo para ele analisar o resultado
workflow.add_edge("call_tools", "call_model")

# Após atualizar a memória, finalizar o grafo
workflow.add_edge("update_memory", END)
app_graph = workflow.compile()
