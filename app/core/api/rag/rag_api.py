from numpy import ogrid
from app.core.schema.db_info_schema import DBInfo
from app.utils.logger import logger
from app.core.service.rag.rag_service import RagService
from app.core.helper.db_info import get_db_info


class RagApi:
    async def __init__(self, org_id: str):
        self.logger = logger
        self.org_id = org_id
        self.service = RagService(org_id=org_id)
        await self.get_db_name()

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

    async def generate_embedding(self, file_data: bytes, filename: str, content_type: str):
        try:
            await self.service.generate_embedding_service(file_data, filename, content_type)
        except Exception as e:
            self.logger.error(f"Failed to generate embedding for {filename}: {e}")
            raise e
