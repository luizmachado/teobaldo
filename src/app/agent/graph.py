import aiosqlite
from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from langgraph.prebuilt import ToolNode
from app.agent.nodes import call_model, update_long_term_memory, call_tools_and_update_state, retrieve_long_term_memory
from app.tools.maps_tools import get_route_and_polyline
from app.tools.weather_tools import get_weather_forecast
from app.tools.partner_tools import find_partners_on_route
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver




async def get_agent_executor():
    """ Criar e compilar grafo """

    tools = [get_route_and_polyline, get_weather_forecast, find_partners_on_route]
    tool_node = ToolNode(tools)

    conn = await aiosqlite.connect("src/data/conversations.sqlite")
    memory = AsyncSqliteSaver(conn=conn)

    def should_continue(state):
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "call_tools"
        else:
            return "update_memory"

    workflow = StateGraph(AgentState)

    # Adicionar nós
    workflow.add_node("retrieve_memory", retrieve_long_term_memory)
    workflow.add_node("call_model", call_model)
    workflow.add_node("call_tools", call_tools_and_update_state)
    workflow.add_node("update_memory", update_long_term_memory)

    # Ponto de entrada
    workflow.set_entry_point("retrieve_memory")

    # Adicionar arestas
    workflow.add_edge("retrieve_memory", "call_model")
    workflow.add_conditional_edges(
        "call_model",
        should_continue,
        {
            "call_tools": "call_tools",
            "update_memory": "update_memory",
        }
    )
    workflow.add_edge("call_tools", "call_model")
    workflow.add_edge("update_memory", END)



    # Compilar grafo
    app_graph = workflow.compile(checkpointer=memory)

    return app_graph
