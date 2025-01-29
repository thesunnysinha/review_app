from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from db.base import Base
from sqlalchemy.orm import relationship, backref


class ReviewHistory(Base):
    __tablename__ = "review_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    stars = Column(Integer, CheckConstraint("stars BETWEEN 1 AND 10"))
    review_id = Column(String(255), nullable=True)
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship with Category
    category = relationship(
        "Category", backref=backref("reviews"), foreign_keys=[category_id]
    )
