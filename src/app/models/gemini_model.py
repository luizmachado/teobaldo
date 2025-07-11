import os
import inspect
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold


class GeminiLLM:
    def __init__(self, **kwargs):

        # Configurações de segurança (compliance)
        safety_settings = kwargs.pop("safety_settings", {})
        safety_settings = self._parse_safety_settings(safety_settings)

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Variável de ambiente GEMINI_API_KEY não está definida.")

        # Definir modelo padrão
        model_name = kwargs.pop("model", "gemini-2.5-flash")  # valor padrão 

        # Instanciar modelo
        try:
            self.model = ChatGoogleGenerativeAI(
                    model=model_name,
                    api_key=api_key,
                    **kwargs)
        except TypeError as e:
            raise ValueError(f"Erro ao instanciar ChatGoogleGenerativeAI: {e}")

    # Função para converter dicionário em enum
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

    def invoke(self, messages):
        return self.model.invoke(messages)

