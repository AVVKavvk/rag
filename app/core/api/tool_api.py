from app.core.schema.db_info_schema import DBInfo
from app.utils.logger import logger
from app.core.schema.tool_schema import ToolSchema, ToolUpdate
from app.core.service.tool_service import ToolService
from app.core.helper.db_info import get_db_info


class ToolApi:
    def __init__(self, org_id: str):
        self.logger = logger
        self.org_id = org_id

    async def initialize(self):
        await self.get_db_name()
        self.service = ToolService(org_id=self.org_id, db_name=self.db_name)
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

    async def create_tool(self, tool: ToolSchema):
        try:
            return await self.service.create_tool_service(tool)
        except Exception as e:
            self.logger.error(f"Failed to create tool: {e}")
            raise e

    async def get_tools(self):
        try:
            return await self.service.get_tools_service()
        except Exception as e:
            self.logger.error(f"Failed to get tools: {e}")
            raise e

    async def get_tool(self, tool_id: str):
        try:
            return await self.service.get_tool_service(tool_id)
        except Exception as e:
            self.logger.error(f"Failed to get tool: {e}")
            raise e

    async def update_tool(self, tool_id: str, tool_update: ToolUpdate):
        try:
            return await self.service.update_tool_service(tool_id, tool_update)
        except Exception as e:
            self.logger.error(f"Failed to update tool: {e}")
            raise e

    async def delete_tool(self, tool_id: str):
        try:
            return await self.service.delete_tool_service(tool_id)
        except Exception as e:
            self.logger.error(f"Failed to delete tool: {e}")
            raise e
