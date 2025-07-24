from fastapi import FastAPI
from app.api.v1 import chat, auth

app = FastAPI(
    title="Teobaldo - Assistente de Viagem",
    description="API para interagir com o assistente de viagem inteligente.",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo ao Teobaldo !"}
