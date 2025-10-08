from app.core.schema.db_info_schema import DBInfo
from app.core.schema.embedded_document_schema import SearchQuery
from app.core.schema.rag_schema import RagDocumentCreate
from app.utils.logger import logger
from app.core.service.rag.rag_service import RagService
from app.core.helper.db_info import get_db_info


class RagApi:
    def __init__(self, org_id: str):
        self.logger = logger
        self.org_id = org_id

    async def initialize(self):
        await self.get_db_name()
        self.service = RagService(org_id=self.org_id, db_name=self.db_name)
        return self

    async def get_db_name(self):
        try:
            data: DBInfo | None = await get_db_info(self.org_id)
            if data is None:
                raise Exception("OrgId not found, please login again")
            self.db_name = data.db_name
            return True
        except Exception as e:
            self.logger.error(f"Failed to get db name: {e}")
            raise e

    async def generate_embedding(self, body: RagDocumentCreate, file_data: bytes, filename: str, content_type: str):
        try:
            await self.service.generate_embedding_service(body, file_data, filename, content_type)
        except Exception as e:
            self.logger.error(f"Failed to generate embedding for {filename}: {e}")
            raise e

    async def query_embedding(self, query: SearchQuery):
        try:
            return await self.service.query_embedding_service(query)
        except Exception as e:
            self.logger.error(f"Failed to get query embedding: {e}")
            raise e
