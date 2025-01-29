from fastapi import APIRouter
from ..category.schema import TopCategoriesResponse
from .schema import ReviewCreate, ReviewResponse
from registry.manager_registry import db_manager
from db.session import SessionDep

router = APIRouter(prefix="/reviews", tags=["Review"])


@router.get("/trends", response_model=list[TopCategoriesResponse])
def get_reviews_trends(*, session: SessionDep):
    """Get top 5 categories based on average stars."""
    model_manager = db_manager.get_manager("category")
    trends = model_manager.get_top_categories(session)
    return trends


@router.get("/", response_model=list[ReviewResponse])
def get_reviews(*, category_id: int, session: SessionDep):
    """Get reviews for a specific category."""
    model_manager = db_manager.get_manager("review")
    reviews = model_manager.get_reviews_by_category(session, category_id)
    return reviews


@router.post("/create", response_model=ReviewResponse)
def post_review(*, review_data: ReviewCreate, session: SessionDep):
    """Post a new review."""
    model_manager = db_manager.get_manager("review")
    # Create review and handle sentiment and tone in ModelManager
    review = model_manager.create_review(session, review_data)
    return review
