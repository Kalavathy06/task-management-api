from datetime import date
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Task, User
from app.database import SessionLocal
from app.emailer import send_email
from app.celery_worker import celery

@celery.task
def send_daily_overdue_summary():
    """
    Celery task to send a daily summary of overdue tasks to each user.
    """
    db: Session = SessionLocal()
    today = date.today()

    # Find all overdue tasks grouped by user
    users_with_overdue = (
        db.query(User)
        .join(Task, Task.assignee_id == User.id)
        .filter(Task.due_date < today, Task.status != "completed")
        .all()
    )

    for user in users_with_overdue:
        overdue_tasks = (
            db.query(Task)
            .filter(
                Task.assignee_id == user.id,
                Task.due_date < today,
                Task.status != "completed"
            )
            .all()
        )

        if overdue_tasks:
            subject = "Daily Summary: Overdue Tasks"
            task_list = "\n".join(
                [f"- {t.title} (Due: {t.due_date})" for t in overdue_tasks]
            )
            body = f"Hello {user.name},\n\nYou have the following overdue tasks:\n\n{task_list}\n\nPlease take action as soon as possible."

            send_email(
                to_email=user.email,
                subject=subject,
                body=body
            )

    db.close()
