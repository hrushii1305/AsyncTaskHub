import os
import resend
from app.celery_app import celery


@celery.task(name="app.tasks.process_task", bind=True, max_retries=3)
def process_task(self, task_id: str, title: str, recipient_email: str):
    """Send a notification email via Resend's HTTP API."""

    # Read API key inside the function (Concept #2: no module-level crash)
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        raise RuntimeError("RESEND_API_KEY must be set")

    resend.api_key = api_key

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": recipient_email,
            "subject": f"New Task: {title}",
            "html": f"""
                <h2>New Task Created</h2>
                <p>A new task has been created for you:</p>
                <ul>
                    <li><strong>Task ID:</strong> {task_id}</li>
                    <li><strong>Title:</strong> {title}</li>
                </ul>
                <p>Regards,<br>AsyncTaskHub</p>
            """
        })
        return f"Email sent successfully to {recipient_email}"

    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)