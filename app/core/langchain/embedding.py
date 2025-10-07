from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import SecretStr
from app.utils.logger import logger
import os
from typing import List, Union
from dotenv import load_dotenv
load_dotenv()

EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL") or ""
if EMBEDDING_MODEL is None or EMBEDDING_MODEL == "":
    raise Exception("GEMINI_EMBEDDING_MODEL is not set")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""
if GEMINI_API_KEY is None or GEMINI_API_KEY == "":
    raise Exception("GEMINI_API_KEY is not set")


class LangchainEmbeddingService():
    def __init__(self):
        self.embedder = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=SecretStr(GEMINI_API_KEY), task_type="retrieval_document")
        self.logger = logger
        self.model = EMBEDDING_MODEL

    async def langchain_generate_embedding_by_gemini(self, document: Document) -> List[float]:
        """
        Generate embedding for a single document.

        Args:
            document: A LangChain Document object

        Returns:
            List of floats representing the embedding vector
        """
        try:
            embeddings = await self.embedder.aembed_documents([document.page_content])
            return embeddings[0]
        except Exception as e:
            self.logger.error(f"Failed to generate embedding for document: {e}")
            raise e

    async def langchain_generate_embedding_by_gemini_batch(self, documents: List[Document]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents in batch.

        Args:
            documents: List of LangChain Document objects

        Returns:
            List of embedding vectors
        """
        try:
            texts = [doc.page_content for doc in documents]
            embeddings = await self.embedder.aembed_documents(texts)
            self.logger.info(f"Successfully generated embeddings for {len(documents)} documents")
            return embeddings
        except Exception as e:
            self.logger.error(f"Failed to generate batch embeddings: {e}")
            raise e

    async def langchain_generate_query_embedding_by_gemini(self, query: str) -> List[float]:
        """
        Generate embedding for a query string.

        Args:
            query: Query text string

        Returns:
            Embedding vector for the query
        """
        try:
            embedding = await self.embedder.aembed_query(query)
            return embedding
        except Exception as e:
            self.logger.error(f"Failed to generate query embedding: {e}")
            raise e
