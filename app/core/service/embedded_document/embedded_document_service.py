from typing import List

from numpy import ogrid
from app.utils.logger import logger
from app.core.config.mongodb import mongo_client
from app.core.schema.embedded_document_schema import EmbeddedDocumentCreate, EmbeddedDocumentResponse, EmbeddedDocumentMetadata, SearchResult, SearchQuery

EMBEDDED_DOCUMENT_COLLECTION = "EmbeddedDocuments"
EMBEDDED_DOCUMENT_INDEX_NAME = "VectorIndex"
NUM_CANDIDATES = 150
EMBEDDING_PATH = "embeddings"


class EmbeddedDocumentService:
    def __init__(self, org_id: str, db_name: str):
        self.logger = logger
        self.mongo_client = mongo_client
        self.org_id = org_id
        self.db_name = db_name

    async def store_embedded_document(self, embedded_document: EmbeddedDocumentCreate):
        try:
            collection = self.mongo_client[self.db_name][EMBEDDED_DOCUMENT_COLLECTION]
            result = await collection.insert_one(embedded_document.model_dump(exclude_unset=True))
            return EmbeddedDocumentResponse(
                id=str(result.inserted_id),
                title=embedded_document.title,
                content=embedded_document.content,
                category=embedded_document.category,
                metadata=embedded_document.metadata
            )
        except Exception as e:
            self.logger.error(f"Failed to store embedded document: {e}")
            raise e

    async def search_embedded_documents(self, query_embedding: List[float], query: SearchQuery):
        try:
            self.logger.info("Searching embedded documents in DB")

            # filter dictionary
            filter_conditions = {}
            if query.category:
                self.logger.info(f"Filtering by category: {query.category}")
                filter_conditions["category"] = {"$eq": query.category}

            if query.metadata and query.metadata.org_id:
                self.logger.info(f"Filtering by org_id: {query.metadata.org_id}")
                filter_conditions["metadata.org_id"] = {"$eq": query.metadata.org_id}

            vector_search_stage = {
                "$vectorSearch": {
                    "index": EMBEDDED_DOCUMENT_INDEX_NAME,
                    "path": EMBEDDING_PATH,
                    "queryVector": query_embedding,
                    "numCandidates": NUM_CANDIDATES,
                    "limit": query.limit
                }
            }

            # Add filter only if there are conditions
            if filter_conditions:
                vector_search_stage["$vectorSearch"]["filter"] = filter_conditions

            pipeline = [
                vector_search_stage,
                {
                    "$project": {
                        "_id": 1,
                        "title": 1,
                        "content": 1,
                        "category": 1,
                        "metadata": 1,
                        "chunk_number": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]

            collection = self.mongo_client[self.db_name][EMBEDDED_DOCUMENT_COLLECTION]
            cursor = collection.aggregate(pipeline)
            results = await cursor.to_list(length=query.limit)

            search_results = [
                SearchResult(
                    id=str(doc["_id"]),
                    title=doc["title"],
                    content=doc["content"],
                    category=doc.get("category"),
                    score=doc["score"],
                    chunk_number=doc["chunk_number"],
                    metadata=doc.get("metadata")
                )
                for doc in results
            ]

            return search_results
        except Exception as e:
            self.logger.error(f"Failed to search embedded documents: {e}")
            raise e
