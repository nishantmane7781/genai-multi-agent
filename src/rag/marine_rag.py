from src.rag.base_rag import BaseRAG


class MarineRAG(BaseRAG):
    def __init__(self):
        super().__init__(collection_name="marine_docs")
