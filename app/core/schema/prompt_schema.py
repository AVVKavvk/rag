from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PromptSchema(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    system_prompt: str
    user_prompt_template: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 5000
    created_at: Optional[str] = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: Optional[str] = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class PromptCreate(BaseModel):
    name: str
    system_prompt: str
    user_prompt_template: str
    tool_ids: List[str] = []
    max_tokens: int = 5000


class PromptUpdate(BaseModel):
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    updated_at: Optional[str] = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
