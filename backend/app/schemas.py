from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=2, examples=["Show diabetic patients above age 50 from Pune"])


class ChatResponse(BaseModel):
    user_message: str
    assistant_message: str
    sql_query: str
    data: List[Dict[str, Any]]
