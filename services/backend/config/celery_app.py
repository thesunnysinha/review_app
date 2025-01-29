from celery import Celery
from config.config import settings
from apps import register_celery_tasks, register_managers

# Setup Celery
celery_app = Celery(
    settings.APP_NAME,
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Kolkata',
    enable_utc=False,
    broker_connection_retry_on_startup=True
)

register_celery_tasks()

register_managers()

