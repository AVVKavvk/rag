from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import HTTPException
from app.utils.logger import logger
from app.core.config.mongodb import mongo_client
from app.core.schema.tool_schema import ToolSchema, ToolUpdate

TOOL_COLLECTION = "Tool"


class ToolService:
    def __init__(self, org_id: str, db_name: str):
        self.logger = logger
        self.mongo_client = mongo_client
        self.org_id = org_id
        self.db_name = db_name

    async def create_tool_service(self, tool: ToolSchema):
        try:
            collection = self.mongo_client[self.db_name][TOOL_COLLECTION]
            tool.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tool.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = await collection.insert_one(tool.model_dump(exclude_unset=True, exclude_none=True))
            tool.id = str(result.inserted_id)
            return tool
        except Exception as e:
            self.logger.error(f"Failed to create tool: {e}")
            raise e

    async def get_tools_service(self):
        try:
            collection = self.mongo_client[self.db_name][TOOL_COLLECTION]
            tools = []
            async for tool in collection.find():
                tool["_id"] = str(tool["_id"])
                tools.append(ToolSchema(**tool))
            return tools
        except Exception as e:
            self.logger.error(f"Failed to get tools: {e}")
            raise e

    async def get_tool_service(self, tool_id: str):
        try:
            if not ObjectId.is_valid(tool_id):
                raise HTTPException(status_code=400, detail="Invalid Tool ID")
            collection = self.mongo_client[self.db_name][TOOL_COLLECTION]
            tool = await collection.find_one({"_id": ObjectId(tool_id)})
            if tool is None:
                return None
            tool["_id"] = str(tool["_id"])
            return ToolSchema(**tool)
        except Exception as e:
            self.logger.error(f"Failed to get tool: {e}")
            raise e

    async def delete_tool_service(self, tool_id: str):
        try:
            collection = self.mongo_client[self.db_name][TOOL_COLLECTION]
            result = await collection.delete_one({"_id": ObjectId(tool_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Tool not found")
        except Exception as e:
            self.logger.error(f"Failed to delete tool: {e}")
            raise e

    async def update_tool_service(self, tool_id: str, tool_update: ToolUpdate):
        try:
            collection = self.mongo_client[self.db_name][TOOL_COLLECTION]
            update_data = {k: v for k, v in tool_update.model_dump(exclude_unset=True, exclude_none=True).items() if v is not None}
            if not update_data:
                raise HTTPException(status_code=400, detail="No fields to update")

            update_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            result = await collection.update_one(
                {"_id": ObjectId(tool_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Tool not found")

            updated_tool = await collection.find_one({"_id": ObjectId(tool_id)})
            if not updated_tool:
                raise HTTPException(status_code=404, detail="Tool not found after update")

            updated_tool["_id"] = str(updated_tool["_id"])

            return ToolSchema(**updated_tool)

        except Exception as e:
            self.logger.error(f"Failed to update tool: {e}")
            raise e
