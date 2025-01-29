from pydantic import BaseModel, Field


# Base model for category
class CategoryBase(BaseModel):
    name: str = Field(..., description="Name of the category")
    description: str = Field(..., description="Description of the category")


# Create category model
class CategoryCreate(CategoryBase):
    pass


# Response model for category
class CategoryResponse(CategoryBase):
    id: int = Field(..., description="ID of the category")

    class Config:
        from_attributes = True

class TopCategoriesResponse(CategoryResponse):
    average_stars: float = Field(..., description="Average stars of a product")
    total_reviews: int = Field(...,description="Total reviews of the category.")


# Pagination model for category list
class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 15