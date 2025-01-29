from sqlalchemy import Column, Integer, String, Text
from db.base import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    description = Column(Text)

    def __repr__(self):
        return f"<Category(name={self.name}, description={self.description})>"
