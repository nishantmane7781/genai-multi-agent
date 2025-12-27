from src.rag.dino_rag import DinoRAG
from src.rag.marine_rag import MarineRAG
from src.rag.earth_rag import EarthRAG
from src.agents.domain_guard import is_question_in_domain
from typing import Optional


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

    def query(self, question: str, agent: Optional[str] = None):
        if not agent:
            return {
                "agent": "generic",
                "response": self.earth_rag.run(question)
            }

        agent = agent.lower()

        # ------------------------
        # Domain Guard
        # ------------------------
        if not is_question_in_domain(question, agent):
            return {
                "agent": agent,
                "error": (
                    f"This question is outside the scope of the '{agent}' agent. "
                    f"Please ask a relevant question."
                )
            }

        # ------------------------
        # Agent Routing
        # ------------------------
        if agent == "dino":
            return {
                "agent": "dino",
                "response": self.dino_rag.run(question)
            }

        if agent == "marine":
            return {
                "agent": "marine",
                "response": self.marine_rag.run(question)
            }

        if agent == "earth":
            return {
                "agent": "earth",
                "response": self.earth_rag.run(question)
            }

        raise ValueError("Invalid agent")
