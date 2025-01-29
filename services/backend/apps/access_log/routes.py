from fastapi import APIRouter
from registry.manager_registry import db_manager
from db.session import SessionDep
from apps.access_log.access_log import AccessLogResponse

router = APIRouter(prefix="/access-log", tags=["AccessLog"])


@router.get("/list", response_model=list[AccessLogResponse])
def get_access_logs(*, session: SessionDep):
    """Get reviews for a specific category."""
    model_manager = db_manager.get_manager("access_log")
    reviews = model_manager.get_access_logs(session)
    return reviews