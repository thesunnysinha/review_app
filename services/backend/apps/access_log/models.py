from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class AccessLog(Base):
    __tablename__ = "access_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
