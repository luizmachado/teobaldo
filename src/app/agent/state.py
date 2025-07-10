from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from operator import add


class AgentState(TypedDict):
    """Estado mantido durante a execução do agente."""

    messages: Annotated[list[BaseMessage], add]
    user_id: str

    origin: NotRequired[str]
    destination: NotRequired[str]
    route_info: NotRequired[dict]
    retrieved_context: NotRequired[str]
