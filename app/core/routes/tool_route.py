from fastapi import Body, Form, Path, APIRouter, Query, Depends
from pydantic import ValidationError
from app.core.schema.tool_schema import ToolSchema, ToolUpdate
from app.utils.logger import logger, x_logger_response
from app.core.api.tool_api import ToolApi
router = APIRouter(
    tags=["Tool"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{org_id}/tool")
async def create_tool(org_id: str, tool: ToolSchema = Body(...)):
    try:
        tool_api = await ToolApi(org_id).initialize()
        return await tool_api.create_tool(tool)
    except Exception as e:
        logger.error(f"Failed to create tool for org_id {org_id}: {e}")
        return {"error": f"Failed to create tool, {e}"}


@router.get("/{org_id}/tool")
async def get_all_tool(org_id: str):
    try:
        tool_api = await ToolApi(org_id).initialize()
        return await tool_api.get_tools()
    except Exception as e:
        logger.error(f"Failed to get tools for org_id {org_id}: {e}")
        return {"error": f"Failed to get tools, {e}"}


@router.get("/{org_id}/tool/{tool_id}")
async def get_tool(org_id: str, tool_id: str):
    try:
        tool_api = await ToolApi(org_id).initialize()
        return await tool_api.get_tool(tool_id)
    except Exception as e:
        logger.error(f"Failed to get tool for org_id {org_id}: {e}")
        return {"error": f"Failed to get tool, {e}"}


@router.put("/{org_id}/tool/{tool_id}")
async def update_tool(org_id: str, tool_id: str, tool_update: ToolUpdate = Body(...)):
    try:
        tool_api = await ToolApi(org_id).initialize()
        return await tool_api.update_tool(tool_id, tool_update)
    except Exception as e:
        logger.error(f"Failed to update tool for org_id {org_id}: {e}")
        return {"error": f"Failed to update tool, {e}"}


@router.delete("/{org_id}/tool/{tool_id}")
async def delete_tool(org_id: str, tool_id: str):
    try:
        tool_api = await ToolApi(org_id).initialize()
        return await tool_api.delete_tool(tool_id)
    except Exception as e:
        logger.error(f"Failed to delete tool for org_id {org_id}: {e}")
        return {"error": f"Failed to delete tool, {e}"}
