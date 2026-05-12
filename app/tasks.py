import time
from app.celery_app import celery

@celery.task(name="app.tasks.process_task")
def process_task(task_id: str):
    # Simulating heavy work
    time.sleep(5)
    return f"Task {task_id} processed successfully!"