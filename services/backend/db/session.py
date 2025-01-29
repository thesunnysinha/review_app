from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

def _get_sync_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(_get_sync_session)]