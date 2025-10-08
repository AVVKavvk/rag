from uuid import uuid4
from fastapi import Body, Form, Path, APIRouter, Query, Depends
from pydantic import ValidationError
from app.core.schema.prompt_schema import PromptSchema, PromptUpdate
from app.utils.logger import logger, x_logger_response
from app.core.api.prompt_api import PromptApi
router = APIRouter(
    tags=["Prompt"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{org_id}/prompt")
async def create_prompt(org_id: str, prompt: PromptSchema = Body(...)):
    try:
        prompt_api = await PromptApi(org_id).initialize()
        return await prompt_api.create_prompt(prompt)
    except Exception as e:
        logger.error(f"Failed to create prompt for org_id {org_id}: {e}")
        return {"error": f"Failed to create prompt, {e}"}


@router.get("/{org_id}/prompt")
async def get_all_prompt(org_id: str):
    try:
        prompt_api = await PromptApi(org_id).initialize()
        return await prompt_api.get_all_prompt()
    except Exception as e:
        logger.error(f"Failed to get prompts for org_id {org_id}: {e}")
        return {"error": f"Failed to get prompts, {e}"}


@router.get("/{org_id}/prompt/first")
async def get_only_first_prompt(org_id: str):
    try:
        prompt_api = await PromptApi(org_id).initialize()
        return await prompt_api.get_only_first_prompt()
    except Exception as e:
        logger.error(f"Failed to get prompt for org_id {org_id}: {e}")
        return {"error": f"Failed to get prompt, {e}"}


@router.get("/{org_id}/prompt/{prompt_id}")
async def get_prompt(org_id: str, prompt_id: str):
    try:
        prompt_api = await PromptApi(org_id).initialize()
        return await prompt_api.get_prompt(prompt_id)
    except Exception as e:
        logger.error(f"Failed to get prompt for org_id {org_id}: {e}")
        return {"error": f"Failed to get prompt, {e}"}


@router.put("/{org_id}/prompt/{prompt_id}")
async def update_prompt(org_id: str, prompt_id: str, prompt_update: PromptUpdate = Body(...)):
    try:
        prompt_api = await PromptApi(org_id).initialize()
        return await prompt_api.update_prompt(prompt_id, prompt_update)
    except Exception as e:
        logger.error(f"Failed to update prompt for org_id {org_id}: {e}")
        return {"error": f"Failed to update prompt, {e}"}


@router.delete("/{org_id}/prompt/{prompt_id}")
async def delete_prompt(org_id: str, prompt_id: str):
    try:
        prompt_api = await PromptApi(org_id).initialize()
        return await prompt_api.delete_prompt(prompt_id)
    except Exception as e:
        logger.error(f"Failed to delete prompt for org_id {org_id}: {e}")
        return {"error": f"Failed to delete prompt, {e}"}
