from sqlalchemy import func
from db.session import SessionDep

from apps.review.schema import ReviewCreate
from apps.access_log.tasks import save_access_log
from ..category.models import Category
from .models import ReviewHistory
from sqlalchemy.exc import SQLAlchemyError
from .tasks import update_sentiment_and_tone
import structlog

logger = structlog.get_logger(__name__)


class ModelManager:
    @staticmethod
    def create_review(session: SessionDep, review_data: ReviewCreate) -> ReviewHistory:
        """Create a new review."""
        try:
            review = ReviewHistory(**review_data.model_dump())
            session.add(review)
            session.commit()
            session.refresh(review)

            # Trigger sentiment and tone update task
            update_sentiment_and_tone.delay(review.id)

            return review
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @staticmethod
    def get_reviews_by_category(
        session: SessionDep, category_id: int, page: int = 1, page_size: int = 15
    ):
        """Get paginated LATEST EDITS of reviews for a specific category"""
        save_access_log.delay(f"GET /reviews/?category_id={category_id}")

        # Get category first
        category = session.get(Category, category_id)
        if not category:
            logger.info(f"Category {category_id} not found")
            return []

        # Subquery to get latest edit for each review
        subquery = (
            session.query(
                ReviewHistory.review_id,
                func.max(ReviewHistory.created_at).label('max_created_at')
            )
            .filter(ReviewHistory.category_id == category_id)
            .group_by(ReviewHistory.review_id)
            .subquery()
        )

        # Main query with pagination
        query = (
            session.query(ReviewHistory)
            .join(
                subquery,
                (ReviewHistory.review_id == subquery.c.review_id) &
                (ReviewHistory.created_at == subquery.c.max_created_at)
            )
            .order_by(ReviewHistory.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        final_reviews = query.all()

        return final_reviews
