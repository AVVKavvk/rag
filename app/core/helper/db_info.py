from typing import Optional
from app.core.config.mongodb import mongo_client
from app.core.schema.db_info_schema import DBInfo
from app.utils.logger import logger

HELPER_DB_NAME = "ASS_ORG_ID_DB_NAME"
HELPER_COLL_NAME = "ASS_ORG_ID_DB_NAME_COLL"


async def get_db_info(org_id: str) -> DBInfo | None:
    try:
        result = await mongo_client[HELPER_DB_NAME][HELPER_COLL_NAME].find_one({"orgId": org_id})
        if not result:
            logger.warning(f"No DB info found for org_id: {org_id}")
            return None

        data = DBInfo(
            org_id=result.get("orgId"),
            db_name=result.get("dbName"),
            metadata=result.get("metadata")
        )
        if data.db_name is None or data.db_name == "":
            logger.warning(f"No DB name found for org_id: {org_id}")
            return None
        return data or None
    except Exception as e:
        logger.error(f"Failed to get db info: {e}")
        return None
