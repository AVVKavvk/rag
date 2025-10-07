from uuid import uuid4
from fastapi import Body, Form, Path, APIRouter, Query, Depends, File, UploadFile
from pydantic import ValidationError
from app.core.schema.embedded_document_schema import EmbeddedDocumentMetadata, SearchQuery
from app.core.schema.rag_schema import RagDocumentCreate
from app.utils.logger import logger, x_logger_response
from app.core.api.rag.rag_api import RagApi
router = APIRouter(
    tags=["RAG"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{org_id}/rag/generate-embedding")
async def generate_embedding(
    org_id: str,
    body: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        try:
            rag_data = RagDocumentCreate.model_validate_json(body)
        except ValidationError as e:
            logger.error(f"Invalid body format: {e}")
            return {"error": f"Invalid body format: {e}"}

        rag_api = await RagApi(org_id).initialize()
        content = await file.read()
        if file.filename is None:
            file.filename = f"{uuid4()}"
        if file.content_type is None:
            file.content_type = "application/octet-stream"
        await rag_api.generate_embedding(rag_data, content, file.filename, file.content_type)

        return {"message": "Embedding generated successfully"}
    except Exception as e:
        logger.error(f"Failed to generate embedding for org_id {org_id}: {e}")
        return {"error": f"Failed to generate embedding, {e}"}


@router.get("/{org_id}/rag/query")
async def query_embedding(org_id: str, query: str = Query(...), limit: int = Query(3), category: str = Query(None)):
    try:
        rag_api = await RagApi(org_id).initialize()
        data = SearchQuery(query=query, limit=limit, category=category, metadata=EmbeddedDocumentMetadata(org_id=org_id))
        return await rag_api.query_embedding(data)
    except Exception as e:
        logger.error(f"Failed to get query embedding for org_id {org_id}: {e}")
        return {"error": f"Failed to get query embedding, {e}"}
