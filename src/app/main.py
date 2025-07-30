from fastapi import FastAPI
from app.api.v1 import chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SuperApp Sem Parar - Teobaldo")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1 import chat, auth

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": f"Teobaldo - Seu assistente de viagens Sem Parar"}
