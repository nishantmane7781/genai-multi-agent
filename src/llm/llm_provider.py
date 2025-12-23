
from langchain_community.llms import Ollama

class LLMProvider:
    def __init__(self, model_name):
        self.llm = Ollama(model=model_name)

    def get_llm(self):
        return self.llm
