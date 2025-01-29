from sqlalchemy import String, func
from db.session import SessionDep

from apps.category.schema import CategoryCreate, TopCategoriesResponse
from apps.review.models import ReviewHistory
from apps.access_log.tasks import save_access_log
from ..category.models import Category
from sqlalchemy.exc import SQLAlchemyError
import structlog

logger = structlog.get_logger(__name__)


class ModelManager:

    @staticmethod
    def get_top_categories(session: SessionDep) -> TopCategoriesResponse:
        """Get top 5 categories based on average stars from latest review versions."""
        save_access_log.delay("GET /reviews/trends")

        try:
            # Subquery to get latest review versions with type casting
            latest_subq = (
                session.query(
                    ReviewHistory.category_id,
                    func.coalesce(
                        ReviewHistory.review_id,
                        func.cast(ReviewHistory.id, String)
                    ).label('review_group'),
                    ReviewHistory.stars,
                    func.row_number().over(
                        partition_by=func.coalesce(
                            ReviewHistory.review_id,
                            func.cast(ReviewHistory.id, String)
                        ),
                        order_by=ReviewHistory.created_at.desc()
                    ).label('row_num')
                )
                .subquery()
            )

            # Main aggregation query
            stats_query = (
                session.query(
                    Category.id,
                    Category.name,
                    Category.description,
                    func.avg(latest_subq.c.stars).label('avg_stars'),
                    func.count().label('total_reviews')
                )
                .join(latest_subq, Category.id == latest_subq.c.category_id)
                .filter(latest_subq.c.row_num == 1)
                .group_by(Category.id)
                .order_by(func.avg(latest_subq.c.stars).desc())
            )

            results = stats_query.limit(5).all()
            
            return [{
                "id": cat_id,
                "name": name,
                "description": description,
                "average_stars": round(float(avg_stars), 2) if avg_stars else 0.0,
                "total_reviews": total_reviews
            } for cat_id, name, description, avg_stars, total_reviews in results]

        except SQLAlchemyError as e:
            logger.error(f"Database error fetching top categories: {str(e)}")
            return []

    @staticmethod
    def create_category(session: SessionDep, category_data: CategoryCreate) -> Category:
        """Create a new category."""
        try:
            logger.info("Creating category", category_data=category_data)
            category = Category(**category_data.model_dump())
            session.add(category)
            session.commit()
            session.refresh(category)
            return category
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @staticmethod
    def get_category_by_id(session: SessionDep, category_id: int) -> Category:
        """Get category by ID."""
        return session.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_categories(
        session: SessionDep, page: int = 1, page_size: int = 15
    ) -> list[Category]:
        """Get a paginated list of categories."""
        categories = (
            session.query(Category)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )
        return categories