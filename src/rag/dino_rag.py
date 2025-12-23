from src.rag.base_rag import BaseRAG


class DinoRAG(BaseRAG):
    def __init__(self):
        super().__init__(collection_name="dino_docs")
