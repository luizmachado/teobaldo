from fastapi import FastAPI
from app.api.v1 import chat

app = FastAPI(title="SuperApp Sem Parar - Teobaldo")

# Inclui o router da API
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": f"Teobaldo - Seu assistente de viagens Sem Parar"}
