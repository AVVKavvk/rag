from uuid import uuid4
from fastapi import Body, Path, APIRouter, Query, Depends, File, UploadFile
from app.utils.logger import logger, x_logger_response
from app.core.api.rag.rag_api import RagApi
router = APIRouter(
    tags=["RAG"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{org_id}/rag/generate-embedding")
async def generate_embedding(org_id: str, file: UploadFile = File(...)):
    try:
        rag_api = await RagApi(org_id).initialize()
        content = await file.read()
        if file.filename is None:
            file.filename = f"{uuid4()}"
        if file.content_type is None:
            file.content_type = "application/octet-stream"
        await rag_api.generate_embedding(content, file.filename, file.content_type)
    except Exception as e:
        logger.error(f"Failed to generate embedding for org_id {org_id}: {e}")
        return {"error": f"Failed to generate embedding, {e}"}
