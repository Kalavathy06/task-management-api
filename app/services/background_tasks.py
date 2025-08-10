from app.celery_worker import celery
from app.models import Task, User
from app.database import SessionLocal
from app.emailer import send_email

@celery.task
def send_task_assignment_email(task_id):
	db = SessionLocal()
	task = db.query(Task).filter(Task.id == task_id).first()
	if task and task.assignee_id:
		user = db.query(User).filter(User.id == task.assignee_id).first()
		if user:
			subject = f"Task Assigned: {task.title}"
			body = f"Hello {user.name or user.email},\n\nYou have been assigned a new task: {task.title}.\n\nDescription: {task.description or ''}\nDue Date: {task.due_date}"
			send_email(to_email=user.email, subject=subject, body=body)
	db.close()

@celery.task
def send_task_status_change_email(task_id):
	db = SessionLocal()
	task = db.query(Task).filter(Task.id == task_id).first()
	if task and task.assignee_id:
		user = db.query(User).filter(User.id == task.assignee_id).first()
		if user:
			subject = f"Task Status Updated: {task.title}"
			body = f"Hello {user.name or user.email},\n\nThe status of your assigned task '{task.title}' has changed to: {task.status}."
			send_email(to_email=user.email, subject=subject, body=body)
	db.close()
