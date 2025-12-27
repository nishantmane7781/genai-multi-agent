from langchain_community.llms import Ollama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable import RunnablePassthrough

from src.vectorstore.chroma_store import ChromaVectorStore
from src.prompts.response_schema import AgentResponse
from src.config.settings import (
    LLM_MODEL,
    VECTOR_DB_DIR,
    LLM_TEMPERATURE,
    EMBEDDING_MODEL
)


class BaseRAG:
    def __init__(self, collection_name: str):

        # --------------------
        # LLM
        # --------------------
        self.llm = Ollama(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE
        )

        # --------------------
        # Embeddings
        # --------------------
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        # --------------------
        # Vector Store
        # --------------------
        self.vectorstore = ChromaVectorStore(
            persist_dir=VECTOR_DB_DIR,
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

Use ONLY the given context to answer the question.
If the answer is not present in the context, use "Not found in documents".

You MUST return a valid JSON object that strictly follows this schema:
{format_instructions}

IMPORTANT RULES (DO NOT BREAK):
- "summary" must be a single string
- "key_points" must be an array of STRINGS only
- "sources" must be an array of STRINGS only
- Do NOT return objects inside arrays
- Do NOT add title/description pairs
- Do NOT add extra fields
- Do NOT add explanations outside JSON

If information is missing:
- Use "Not found in documents" as string values

Context:
{context}

Question:
{question}

Return ONLY valid JSON.

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
