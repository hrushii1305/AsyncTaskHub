import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.celery_app import celery


@celery.task(name="app.tasks.process_task", bind=True, max_retries=3)
def process_task(self, task_id: str, title: str, recipient_email: str):
    """Send a notification email when a task is created."""

    # ✅ Concept #2: credentials read INSIDE the function, not at module level
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not email_user or not email_password:
        raise RuntimeError("EMAIL_USER and EMAIL_PASSWORD must be set")

    # Build the email
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = recipient_email          # ✅ Concept #1: the user's real email
    msg["Subject"] = f"New Task: {title}"

    body = f"""Hello,

A new task has been created for you:

  Task ID: {task_id}
  Title: {title}

Regards,
AsyncTaskHub
"""
    msg.attach(MIMEText(body, "plain"))

    try:
        # ✅ Fix: port 465 with SMTP_SSL (Railway blocks port 587)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
            server.login(email_user, email_password)
            server.sendmail(email_user, recipient_email, msg.as_string())

        return f"Email sent successfully to {recipient_email}"

    except Exception as exc:
        # ✅ Fix: raise (not return) so Celery sees a real failure, with auto-retry
        raise self.retry(exc=exc, countdown=60)