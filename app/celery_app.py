from celery import Celery

celery = Celery(
    "asynctaskhub",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks"]
)