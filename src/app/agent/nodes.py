from langchain_core.messages import AIMessage, BaseMessage
from app.agent.state import AgentState
from app.models.llm_factory import LLMFactory
from app.tools import mock_tools as maps_tools
weather_tools = maps_tools
partner_tools = maps_tools


# Escolha do modelo padrão
llm = LLMFactory().get_model("gemini-default")


def call_model(state):
    """Chama o LLM com base nas mensagens atuais."""
    messages = state["messages"]

    response: BaseMessage = llm.invoke(messages)

    return {
        **state,
        "messages": messages + [response],
    }


def call_tools(state):
    """Executa ferramentas com base nas chamadas de ferramenta presentes na última mensagem."""
    last_message = state["messages"][-1]
    tool_calls = getattr(last_message, "tool_calls", [])

    # Dicionário para incluir Tools 
    tool_dispatch = {
            "get_route_info": mock_tools.get_route_info,
            "get_weather": mock_tools.get_weather,
            "find_partner": mock_tools.find_partner,
            }

    results = []

    
    for call in tool_calls:
        tool_name = call["name"]
        args = call["args"]

        tool_fn = tool_dispatch.get(tool_name)
        if tool_fn:
            result = tool_fn(**args)
        else:
            result = f"'{tool_name}' não reconhecida."

        results.append(result)

    tool_response = AIMessage(content=str(results))

    return {
        **state,
        "messages": state["messages"] + [tool_response],
    }


def update_long_term_memory(state):
    """Atualiza a memória de longo prazo (necessário implementar)."""
    print(f"[Memória] Estado salvo: {state}")
    return state

