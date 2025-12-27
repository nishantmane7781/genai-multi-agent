from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable import RunnablePassthrough

from src.vectorstore.chroma_store import ChromaVectorStore
from src.prompts.response_schema import AgentResponse


class BaseRAG:
    def __init__(self, collection_name: str):

        # --------------------
        # LLM
        # --------------------
        self.llm = Ollama(
            model="phi3:mini",
            temperature=0
        )

        # --------------------
        # Embeddings
        # --------------------
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # --------------------
        # Vector Store
        # --------------------
        self.vectorstore = ChromaVectorStore(
            persist_dir="chroma_db",
            collection_name=collection_name,
            embeddings=self.embeddings
        )

        self.retriever = self.vectorstore.as_retriever()

        # --------------------
        # Output Parser
        # --------------------
        self.parser = PydanticOutputParser(
            pydantic_object=AgentResponse
        )

        # --------------------
        # Prompt
        # --------------------
        self.prompt = PromptTemplate(
            template="""
You are a domain expert assistant.

Use ONLY the given context to answer.
If the answer is not present, say "Not found in documents".

Return output strictly in JSON format:
{format_instructions}

Context:
{context}

Question:
{question}
""",
            input_variables=["context", "question"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            }
        )

        # --------------------
        # Runnable Chain
        # --------------------
        self.chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | self.parser
        )

    def run(self, question: str) -> dict:
        """
        Returns structured JSON output
        """
        response = self.chain.invoke(question)
        return response.dict()
