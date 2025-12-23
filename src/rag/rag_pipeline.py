
from langchain.chains import RetrievalQA

class RAGPipeline:
    def __init__(self, llm, retriever, chunk_size, chunk_overlap):
        self.qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    def run(self, query):
        return self.qa.run(query)
