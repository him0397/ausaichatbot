from typing import Any, Dict

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., example="Daily care tasks in kindergarten")
    field: str = Field(..., example="Activity given to childern's")


class QueryResponse(BaseModel):
    response: str


class AutoCompleteRequest(BaseModel):
    template: Dict[str, Any] = Field(...)


class AutoCompleteResponse(BaseModel):
    completed_template: Dict[str, Any]
