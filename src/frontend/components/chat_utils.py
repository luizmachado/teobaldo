import requests

CHAT_API_URL = "http://localhost:8000/api/v1/chat"

def enviar_mensagem(user_id, message, thread_id):
    try:
        payload = {
            "user_id": str(user_id),
            "message": message,
            "thread_id": thread_id,
        }
        response = requests.post(CHAT_API_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Erro ao enviar mensagem: {e}"

