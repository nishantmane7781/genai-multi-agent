from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from src.vectorstore.chroma_store import ChromaVectorStore


class BaseRAG:
    def __init__(self, collection_name: str):
        self.llm = Ollama(
            model="phi3:mini",
            temperature=0
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = ChromaVectorStore(
            persist_dir="chroma_db",
            collection_name=collection_name,
            embeddings=self.embeddings
        )

        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            chain_type="stuff"
        )

    def run(self, question: str) -> str:
        return self.qa.run(question)
