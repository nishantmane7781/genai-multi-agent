import os
import pandas as pd
from pypdf import PdfReader
from langchain.schema import Document


class MarineDocumentLoader:

    @staticmethod
    def load_pdf(folder: str):
        docs = []
        for file in os.listdir(folder):
            if file.endswith(".pdf"):
                reader = PdfReader(os.path.join(folder, file))
                for page in reader.pages:
                    docs.append(
                        Document(
                            page_content=page.extract_text(),
                            metadata={"source": file, "type": "pdf"}
                        )
                    )
        return docs

    @staticmethod
    def load_excel(folder: str):
        docs = []
        for file in os.listdir(folder):
            if file.endswith(".xlsx"):
                df = pd.read_excel(os.path.join(folder, file))
                text = df.to_string(index=False)
                docs.append(
                    Document(
                        page_content=text,
                        metadata={"source": file, "type": "excel"}
                    )
                )
        return docs

    @classmethod
    def load_all(cls, base_path="data/marine"):
        pdf_docs = cls.load_pdf(f"{base_path}/pdf")
        excel_docs = cls.load_excel(f"{base_path}/excel")
        return pdf_docs + excel_docs
