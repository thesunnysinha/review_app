from config.celery_app import celery_app
from db.session import SessionLocal
from registry.manager_registry import db_manager
import structlog

logger = structlog.get_logger(__name__)

@celery_app.task
def save_access_log(log_text: str):
    """Save access log asynchronously."""
    db = SessionLocal()
    model_manager = db_manager.get_manager("access_log")
    try:
        model_manager.log_access(db, log_text)
    except Exception as e:
        logger.error(f"Error while saving access log: {str(e)}")
    finally:
        db.close()
