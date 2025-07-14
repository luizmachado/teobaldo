from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.agent.graph import get_agent_executor
from langchain_core.messages import HumanMessage
import traceback

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Identificador único do usuário.")
    message: str = Field(..., description="Mensagem do usuário para o Teobaldo.")
    thread_id: str = Field(..., description="Identificador da sessão de conversa para manter o histórico.")

class ChatResponse(BaseModel):
    response: str
    thread_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, agent_executor=Depends(get_agent_executor)):
    """ Endpoint para interagir com o Teobaldo """
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        inputs = {"messages": [HumanMessage(content=request.message)], "user_id": request.user_id}

        # Use 'ainvoke' para obter o resultado final diretamente
        final_state = await agent_executor.ainvoke(inputs, config=config)

        # Extraia a última mensagem da lista de mensagens no estado final
        final_response = final_state.get("messages", [])[-1].content

        if not final_response:
            raise HTTPException(status_code=500, detail="O agente não produziu uma resposta final com conteúdo.")

        return ChatResponse(response=final_response, thread_id=request.thread_id)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
