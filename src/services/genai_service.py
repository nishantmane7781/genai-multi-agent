from src.rag.dino_rag import DinoRAG
from src.rag.marine_rag import MarineRAG
from src.rag.earth_rag import EarthRAG

class GenAIService:
    _instance = None

    def __init__(self):
        self.dino_rag = DinoRAG()
        self.marine_rag = MarineRAG()
        self.earth_rag = EarthRAG()

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def query(self, question: str, agent: str):
        agent = agent.lower()

        if agent == "dino":
            return self.dino_rag.run(question)

        if agent == "marine":
            return self.marine_rag.run(question)

        if agent == "earth":
            return self.earth_rag.run(question)

        raise ValueError("Invalid agent")
