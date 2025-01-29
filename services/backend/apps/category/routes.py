from fastapi import APIRouter
from .schema import (
    CategoryCreate,
    CategoryResponse,
    PaginationParams,
)
from registry.manager_registry import db_manager
from db.session import SessionDep

router = APIRouter(prefix="/category", tags=["Category"])


# Create category endpoint
@router.post("/create", response_model=CategoryResponse)
def create_category(*, category_data: CategoryCreate, session: SessionDep):
    """Create a new category."""
    model_manager = db_manager.get_manager("category")
    category = model_manager.create_category(session, category_data)
    return category

# Get list of categories with pagination (via Pydantic model)
@router.post("/list", response_model=list[CategoryResponse])
def get_categories(*, pagination: PaginationParams, session: SessionDep):
    """Get a paginated list of categories."""
    model_manager = db_manager.get_manager("category")
    categories = model_manager.get_categories(
        session, pagination.page, pagination.page_size
    )
    return categories