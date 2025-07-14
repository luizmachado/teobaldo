from langchain_community.chat_models import ChatOllama

class OllamaLLM:
    def __init__(self, **kwargs):
        model = kwargs.pop("model", "llama3")
        base_url = kwargs.pop("base_url", None)

        params = {"model": model}
        if base_url:
            params["base_url"] = base_url
        params.update(kwargs)

        self.model = ChatOllama(**params)

    def __call__(self, prompt, **kwargs):
        return self.model.invoke(prompt, **kwargs)

    def __getattr__(self, name):
        """ Delega chamadas de atributos para o modelo encapsulado """
        return getattr(self.model, name)

