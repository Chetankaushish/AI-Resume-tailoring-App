from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

import os


class ResumeRAG:

    def __init__(self):

        self.embeddings = (
            GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=os.getenv(
                    "GOOGLE_API_KEY"
                )
            )
        )

    def build_vector_store(
        self,
        resume_text
    ):

        splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
        )

        chunks = splitter.split_text(
            resume_text
        )

        vector_store = FAISS.from_texts(
            chunks,
            self.embeddings
        )

        return vector_store

    def retrieve(
        self,
        vector_store,
        job_description,
        k=5
    ):

        docs = (
            vector_store
            .similarity_search(
                job_description,
                k=k
            )
        )

        return "\n".join(
            [
                d.page_content
                for d in docs
            ]
        )