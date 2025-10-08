from app.core.schema.db_info_schema import DBInfo
from app.utils.logger import logger
from app.core.schema.prompt_schema import PromptSchema, PromptUpdate
from app.core.service.prompt_service import PromptService
from app.core.helper.db_info import get_db_info


class PromptApi:
    def __init__(self, org_id: str):
        self.logger = logger
        self.org_id = org_id

    async def initialize(self):
        await self.get_db_name()
        self.service = PromptService(org_id=self.org_id, db_name=self.db_name)
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

    async def create_prompt(self, prompt: PromptSchema):
        try:
            return await self.service.create_prompt_service(prompt)
        except Exception as e:
            self.logger.error(f"Failed to create prompt: {e}")
            raise e

    async def get_all_prompt(self):
        try:
            return await self.service.get_all_prompt_service()
        except Exception as e:
            self.logger.error(f"Failed to get prompts: {e}")
            raise e

    async def get_only_first_prompt(self):
        try:
            return await self.service.get_only_first_prompt_service()
        except Exception as e:
            self.logger.error(f"Failed to get prompt: {e}")
            raise e

    async def get_prompt(self, prompt_id: str):
        try:
            return await self.service.get_prompt_service(prompt_id)
        except Exception as e:
            self.logger.error(f"Failed to get prompt: {e}")
            raise e

    async def update_prompt(self, prompt_id: str, prompt_update: PromptUpdate):
        try:
            return await self.service.update_prompt_service(prompt_id, prompt_update)
        except Exception as e:
            self.logger.error(f"Failed to update prompt: {e}")
            raise e

    async def delete_prompt(self, prompt_id: str):
        try:
            return await self.service.delete_prompt_service(prompt_id)
        except Exception as e:
            self.logger.error(f"Failed to delete prompt: {e}")
            raise e
