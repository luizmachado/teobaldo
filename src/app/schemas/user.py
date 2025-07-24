from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class User(BaseModel):
    """ Modelo base para um usuário no sistema. """
    idCliente: int
    nomeRazaoSocial: str
    documento: str
    contato: Dict[str, Any]
    status: str

class UserInDB(User):
    """ Modelo completo do usuário como está no 'banco de dados' (JSON). """
    produtosContratados: Dict[str, Any]

class Token(BaseModel):
    """ Modelo para o token de acesso retornado ao cliente. """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """ Modelo para os dados contidos dentro do JWT. """
    documento: Optional[str] = None
