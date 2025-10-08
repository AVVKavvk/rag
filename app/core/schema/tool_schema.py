from datetime import datetime
from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class APIToolConfig(BaseModel):
    """Configuration for REST API tool"""
    url: str
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] = "GET"
    headers: Dict[str, str] = {}
    query_params: Dict[str, str] = {}
    path_params: Dict[str, str] = {}
    body: Optional[Dict[str, Any]] = None
    body_type: Literal["json", "form", "text"] = "json"
    timeout: int = 60
    auth_type: Optional[Literal["bearer", "basic", "api_key"]] = None
    auth_config: Dict[str, str] = {}


class ToolSchema(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    description: str
    api_config: Optional[APIToolConfig] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_parser: Optional[str] = None
    created_at: Optional[str] = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: Optional[str] = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class ToolCreate(BaseModel):
    name: str
    description: str
    api_config: APIToolConfig
    input_schema: Dict[str, Any] = {}
    output_parser: Optional[str] = None


class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    api_config: Optional[APIToolConfig] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_parser: Optional[str] = None
    updated_at: Optional[str] = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
