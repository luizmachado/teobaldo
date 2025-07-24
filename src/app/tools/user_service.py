import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from app.schemas.user import UserInDB

# Caminho para o arquivo JSON de usuários
DATA_PATH = Path(__file__).parent.parent.parent / "data" / "users.json"

_users_cache: Optional[List[Dict[str, Any]]] = None

def _load_users() -> List[Dict[str, Any]]:
    """ Carrega os usuários do arquivo JSON. Usa um cache simples em memória. """
    global _users_cache
    if _users_cache is None:
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                _users_cache = json.load(f).get("clientes", [])
        except (FileNotFoundError, json.JSONDecodeError):
            _users_cache = []
    return _users_cache

def get_user_by_document(documento: str) -> Optional[UserInDB]:
    """ Busca um usuário pelo seu número de documento. """
    users = _load_users()
    for user_data in users:
        if user_data.get("documento") == documento:
            return UserInDB(**user_data)
    return None
