from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import HTTPException
from app.utils.logger import logger
from app.core.config.mongodb import mongo_client
from app.core.schema.prompt_schema import PromptSchema, PromptUpdate

PROMPT_COLLECTION = "Prompt"


class PromptService:
    def __init__(self, org_id: str, db_name: str):
        self.logger = logger
        self.mongo_client = mongo_client
        self.org_id = org_id
        self.db_name = db_name

    async def create_prompt_service(self, prompt: PromptSchema):
        try:
            collection = self.mongo_client[self.db_name][PROMPT_COLLECTION]
            result = await collection.insert_one(prompt.model_dump(exclude_unset=True, exclude_none=True))
            prompt.id = str(result.inserted_id)
            return prompt
        except Exception as e:
            self.logger.error(f"Failed to create prompt: {e}")
            raise e

    async def get_all_prompt_service(self):
        try:
            collection = self.mongo_client[self.db_name][PROMPT_COLLECTION]
            prompts = []
            async for prompt in collection.find():
                prompt["_id"] = str(prompt["_id"])
                prompts.append(PromptSchema(**prompt))
            return prompts
        except Exception as e:
            self.logger.error(f"Failed to get prompts: {e}")
            raise e

    async def get_only_first_prompt_service(self):
        try:
            collection = self.mongo_client[self.db_name][PROMPT_COLLECTION]
            prompt = await collection.find_one()
            if prompt is None:
                return None
            prompt["_id"] = str(prompt["_id"])
            return PromptSchema(**prompt)
        except Exception as e:
            self.logger.error(f"Failed to get prompt: {e}")
            raise e

    async def get_prompt_service(self, prompt_id: str):
        try:
            if not ObjectId.is_valid(prompt_id):
                raise HTTPException(status_code=400, detail="Invalid Prompt ID")
            collection = self.mongo_client[self.db_name][PROMPT_COLLECTION]

            prompt = await collection.find_one({"_id": ObjectId(prompt_id)})
            if prompt is None:
                return None
            prompt["_id"] = str(prompt["_id"])
            return PromptSchema(**prompt)
        except Exception as e:
            self.logger.error(f"Failed to get prompt: {e}")
            raise e

    async def update_prompt_service(self, prompt_id: str, prompt_update: PromptUpdate):
        try:
            collection = self.mongo_client[self.db_name][PROMPT_COLLECTION]
            update_data = {k: v for k, v in prompt_update.model_dump(exclude_unset=True, exclude_none=True).items() if v is not None}
            if not update_data:
                raise HTTPException(status_code=400, detail="No fields to update")

            update_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            result = await collection.update_one(
                {"_id": ObjectId(prompt_id)},
                {"$set": update_data}
            )

            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Prompt not found")

            updated_prompt = await collection.find_one({"_id": ObjectId(prompt_id)})
            if not updated_prompt:
                raise HTTPException(status_code=404, detail="Prompt not found after update")

            updated_prompt["_id"] = str(updated_prompt["_id"])

            return PromptSchema(**updated_prompt)

        except Exception as e:
            self.logger.error(f"Failed to update prompt: {e}")
            raise e

    async def delete_prompt_service(self, prompt_id: str):
        try:
            collection = self.mongo_client[self.db_name][PROMPT_COLLECTION]
            result = await collection.delete_one({"_id": ObjectId(prompt_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Prompt not found")
        except Exception as e:
            self.logger.error(f"Failed to delete prompt: {e}")
            raise e
