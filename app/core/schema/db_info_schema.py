from pydantic import BaseModel
from typing import Optional, Dict


class DBInfo(BaseModel):
    org_id: str
    db_name: str
    metadata: Optional[Dict[str, str]]
