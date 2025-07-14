import yaml
from pathlib import Path
from app.models.gemini_model import GeminiLLM
from app.models.ollama_model import OllamaLLM
from langchain_core.prompts import PromptTemplate 


class LLMFactory:
    def __init__(self, config_path=None):
        config_path = config_path or Path(__file__).resolve().parents[3] / "llm_config.yaml"
        with open(config_path, "r") as f:
            self.configs = yaml.safe_load(f)

    def get_model(self, name):
        """ Carrega uma LLM a partir do arquivo de llm_config """
        if name not in self.configs:
            raise ValueError(f"Arquivo de configuração '{name}' não foi encontrado.")

        cfg = self.configs[name]
        provider = cfg.pop("provider")

        if provider == "gemini":
            return GeminiLLM(**cfg)
        elif provider == "openai":
            return OpenAILLM(**cfg)
        elif provider == "ollama":
            return OllamaLLM(**cfg)
        else:
            raise ValueError(f"'{provider}' não suportado.")

    def get_prompt(self, name):
        """ Carrega um PromptTemplate a partir do arquivo de llm_config """

        try:
            prompt_config = self.configs["prompts"][name]
        except KeyError:
            raise ValueError(f"Configuração de prompt '{name}' não encontrada")

        template = prompt_config.get("template")
        input_vars = prompt_config.get("input_variables", [])

        if not template:
            raise ValueError(f"O prompt '{name}' não possui uma chave 'template'")

        return PromptTemplate(template=template, input_variables=input_vars)

