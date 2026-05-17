import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.celery_app import celery
import os

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL_USER or not EMAIL_PASSWORD:
    raise RuntimeError("EMAIL_USER and EMAIL_PASSWORD environment variables are not set!")

@celery.task(name="app.tasks.process_task")
def process_task(task_id: str, title: str = "", description: str = ""):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = description  # description contains the recipient email
        msg["Subject"] = f"Task: {title}"

        body = f"""
        Hello,

        You have a new task assigned:

        Task ID: {task_id}
        Title: {title}

        Regards,
        AsyncTaskHub
        """

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, description, msg.as_string())

        return f"Email sent successfully for task {task_id}"

    except Exception as e:
        return f"Failed to send email: {str(e)}"