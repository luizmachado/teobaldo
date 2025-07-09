from app.models.llm_factory import LLMFactory

llms = LLMFactory()
model = llms.get_model("gemini-default")


messages = [
        ("system", "Translate to French."),
        ("human", "I love programming.")
        ]

response = model.invoke(messages)
print(response.content)
