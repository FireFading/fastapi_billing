from app.config import settings
from celery import Celery
from celery.schedules import crontab

app = Celery(
    "app.tools",
    broker=settings.celery_broker,
    backend=settings.celery_result_backend,
    include=["app.tools.tasks"],
)
app.conf.timezone = "Europe/Moscow"
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update_currencies": {
        "task": "update_currencies",
        "schedule": crontab(minute="*/2"),
    },
}
