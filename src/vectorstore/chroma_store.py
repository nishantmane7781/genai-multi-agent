from langchain_chroma import Chroma


class ChromaVectorStore:
    def __init__(self, persist_dir: str, collection_name: str, embeddings):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embeddings = embeddings

        self.store = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_dir,
            embedding_function=self.embeddings
        )

    def as_retriever(self):
        return self.store.as_retriever(search_kwargs={"k": 4})
