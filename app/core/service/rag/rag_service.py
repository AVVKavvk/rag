from typing import List
from langchain_core.documents import Document
from app.core.langchain.embedding import LangchainEmbeddingService
from app.core.schema.embedded_document_schema import EmbeddedDocumentCreate, EmbeddedDocumentMetadata, SearchQuery
from app.core.schema.rag_schema import RagDocumentCreate
from app.core.service.embedded_document.embedded_document_service import EmbeddedDocumentService
from app.utils.logger import logger
from app.core.splitter.text_splitter import load_and_split_from_s3
from app.core.utils.s3 import upload_file_to_s3
from fastapi.responses import JSONResponse


class RagService():
    def __init__(self, org_id: str, db_name: str):
        self.logger = logger
        self.embedder = LangchainEmbeddingService()
        self.embedder_document_service = EmbeddedDocumentService(org_id=org_id, db_name=db_name)
        self.org_id = org_id
        self.db_name = db_name

    async def generate_embedding_service(self, body: RagDocumentCreate, file_data: bytes, filename: str, content_type: str):
        try:
            self.logger.info(f"Generating embedding for {filename}")
            self.logger.info("Uploading file to S3")
            s3_key = upload_file_to_s3(self.org_id, file_data, filename, content_type)
            self.logger.info("File uploaded to S3")

            self.logger.info(f"Generating chunks for {filename}")

            chunks = load_and_split_from_s3(s3_key, filename)

            self.logger.info(f"Generated chunks for {filename}")
            await self._handle_document_chunks(body, chunks)

            self.logger.info(f"Generated embedding for {filename}")
            return JSONResponse(content={"message": f"Generated embedding for {filename}"}, status_code=200)
        except Exception as e:
            self.logger.error(f"Failed to generate embedding for {filename}: {e}")
            raise

    async def query_embedding_service(self, query: SearchQuery):
        try:
            self.logger.info(f"Generating query embedding for {query.query}")
            return await self._handle_query_embedding(query)
        except Exception as e:
            self.logger.error(f"Failed to get query embedding: {e}")
            raise e

    async def _handle_query_embedding(self, query: SearchQuery):
        try:
            self.logger.info(f"Generating query embedding for by gemini {query.query}")

            query_embeddings = await self.embedder.langchain_generate_query_embedding_by_gemini(query.query)

            self.logger.info(f"Generated query embedding for by gemini {query.query}")
            return await self.embedder_document_service.search_embedded_documents(query_embeddings, query)
        except Exception as e:
            self.logger.error(f"Failed to get query embedding: {e}")
            raise e

    async def _handle_document_chunks(self, body: RagDocumentCreate, chunks: List[Document]):
        try:
            self.logger.info(f"Generating embedding for chunks and Storing in DB, TOtal Chunks: {len(chunks)}", )
            for i, chunk in enumerate(chunks):
                try:
                    self.logger.info(f"Generating embedding for chunk {i}")
                    embeddings: List[float] = await self.embedder.langchain_generate_embedding_by_gemini(chunk)
                    metadata: EmbeddedDocumentMetadata = EmbeddedDocumentMetadata()
                    if body.metadata:
                        metadata.org_id = body.metadata.org_id

                    rag_data: EmbeddedDocumentCreate = EmbeddedDocumentCreate(
                        title=body.title,
                        content=chunk.page_content,
                        chunk_number=i,
                        category=body.category,
                        metadata=metadata,
                        embeddings=embeddings,
                    )

                    await self.embedder_document_service.store_embedded_document(rag_data)
                except Exception as e:
                    self.logger.error(f"Failed to generate embedding for chunk {i}: {e}")
        except Exception as e:
            self.logger.error(f"Failed to create documents: {e}")
            raise e
