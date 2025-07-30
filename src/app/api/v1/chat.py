from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.agent.graph import get_agent_executor
from langchain_core.messages import HumanMessage
import traceback
from app.security.security import get_current_user
from app.schemas.user import User

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Identificador único do usuário (documento).")
    message: str = Field(..., description="Mensagem do usuário para o Teobaldo.")
    thread_id: str = Field(..., description="Identificador da sessão de conversa para manter o histórico.")

class ChatResponse(BaseModel):
    response: str
    thread_id: str
    embed_map_url: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    agent_executor=Depends(get_agent_executor),
    current_user: User = Depends(get_current_user)
):
    """ Endpoint para interagir com o Teobaldo. Requer autenticação. """
    if request.user_id != current_user.documento:
        raise HTTPException(status_code=403, detail="Operação não permitida para esse usuário.")

    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        inputs = {"messages": [HumanMessage(content=request.message)], "user_id": request.user_id}
        
        final_state = await agent_executor.ainvoke(inputs, config=config)
        final_response = final_state.get("messages", [])[-1].content
        embed_map_url = final_state.get("embed_map_url")


        if not final_response:
            raise HTTPException(status_code=500, detail="O agente não produziu uma resposta final com conteúdo.")

        return ChatResponse(response=final_response, thread_id=request.thread_id, embed_map_url=embed_map_url)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
