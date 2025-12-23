from src.rag.base_rag import BaseRAG


class EarthRAG(BaseRAG):
    def __init__(self):
        super().__init__(collection_name="earth_docs")
