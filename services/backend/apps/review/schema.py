from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ReviewBase(BaseModel):
    text: Optional[str] = Field(None, title="Review Text")
    stars: int = Field(..., title="Stars")
    review_id: Optional[int] = Field(None, title="Review ID")
    tone: Optional[str] = Field(None, title="Tone")
    sentiment: Optional[str] = Field(None, title="Sentiment")
    category_id: int = Field(..., title="Category ID")


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int = Field(..., title="ID")
    created_at: datetime = Field(..., title="Created At")
    updated_at: datetime = Field(..., title="Updated At")

    class Config:
        from_attributes = True
