import yaml
from pathlib import Path
from app.models.gemini_model import GeminiLLM

class LLMFactory:
    def __init__(self, config_path=None):
        config_path = config_path or Path(__file__).resolve().parents[3] / "llm_config.yaml"
        with open(config_path, "r") as f:
            self.configs = yaml.safe_load(f)

    def get_model(self, name):
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
