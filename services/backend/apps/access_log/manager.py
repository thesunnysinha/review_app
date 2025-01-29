from ..access_log.models import AccessLog
from db.session import SessionDep
import structlog

logger = structlog.get_logger(__name__)

class ModelManager:

    @staticmethod
    def log_access(session: SessionDep, text: str) -> AccessLog:
        """Log access to the AccessLog table."""
        access_log = AccessLog(text=text)
        session.add(access_log)
        session.commit()
        session.refresh(access_log)
        return access_log
    
    @staticmethod
    def get_access_logs(session: SessionDep) -> list[AccessLog]:
        access_logs = session.query(AccessLog).all()
        return access_logs