import os
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold

class GeminiLLM(ChatGoogleGenerativeAI):

    def __init__(self, **kwargs):

        # Adicionar a chave de API
    if "api_key" not in kwargs:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("A chave de API não foi passada como argumento nem definida na variável de ambiente GEMINI_API_KEY.")
        kwargs["api_key"] = api_key

        # Processar configuracoes de compliance
        if "safety_settings" in kwargs:
            safety_settings = kwargs.pop("safety_settings", {})
            parsed_safety_settings = self._parse_safety_settings(safety_settings)
            if parsed_safety_settings:
                kwargs["safety_settings"] = parsed_safety_settings

        if "model" not in kwargs:
            kwargs["model"] = "gemini-2.5-flash"

        try:
            super().__init__(**kwargs)
        except TypeError as e:
            raise ValueError(f"Erro ao instanciar ChatGoogleGenerativeAI: {e}")

    def _parse_safety_settings(self, safety_dict):

        if not isinstance(safety_dict, dict):
            return None

        parsed = {}

        for key, value in safety_dict.items():
            try:
                category = getattr(HarmCategory, key)
                threshold = getattr(HarmBlockThreshold, value)
                parsed[category] = threshold
            except AttributeError:
                raise ValueError(f"Par inválido: {key}: {value}")
        return parsed
