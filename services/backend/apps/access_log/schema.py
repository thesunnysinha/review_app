from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class AccessLogBase(BaseModel):
    text: Optional[str] = Field(None, title="Text")

class AccessLogResponse(AccessLogBase):
    id: int = Field(..., title="ID")
    created_at: datetime = Field(..., title="Created At")
    updated_at: datetime = Field(..., title="Updated At")

    class Config:
        from_attributes = True