from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash
from datetime import datetime
from typing import Optional, Dict

# ==============================
# Users
# ==============================
def create_user(db: Session, user_in: schemas.UserCreate):
    user = models.User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ==============================
# Projects
# ==============================
def create_project(db: Session, owner_id: int, project_in: schemas.ProjectCreate):
    proj = models.Project(
        title=project_in.title,
        description=project_in.description,
        owner_id=owner_id
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

def get_projects_for_user(db: Session, owner_id: int):
    return db.query(models.Project).filter(models.Project.owner_id == owner_id).all()

def get_project_with_tasks(db: Session, project_id: int, owner_id: int):
    return db.query(models.Project)\
        .filter(models.Project.id == project_id, models.Project.owner_id == owner_id)\
        .first()

def update_project(db: Session, project_id: int, owner_id: int, project_in: schemas.ProjectUpdate):
    project = get_project_with_tasks(db, project_id, owner_id)
    if not project:
        return None
    for field, value in project_in.dict(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int, owner_id: int):
    project = get_project_with_tasks(db, project_id, owner_id)
    if not project:
        return False
    db.delete(project)
    db.commit()
    return True


# ==============================
# Tasks
# ==============================
def create_task(db: Session, task_in: schemas.TaskCreate):
    task = models.Task(
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        priority=task_in.priority or models.Priority.medium,
        status=task_in.status or models.TaskStatus.todo,
        project_id=task_in.project_id,
        assignee_id=task_in.assignee_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int, owner_id: int):
    return db.query(models.Task)\
        .join(models.Project)\
        .filter(models.Task.id == task_id, models.Project.owner_id == owner_id)\
        .first()

def list_tasks(
    db: Session,
    owner_id: int,
    filters: Dict,
    skip: int = 0,
    limit: int = 20,
    sort: Optional[str] = None
):
    q = db.query(models.Task).join(models.Project).filter(models.Project.owner_id == owner_id)

    if filters.get("status"):
        q = q.filter(models.Task.status == filters["status"])
    if filters.get("priority"):
        q = q.filter(models.Task.priority == filters["priority"])
    if filters.get("project_id"):
        q = q.filter(models.Task.project_id == int(filters["project_id"]))
    if filters.get("due_date"):
        q = q.filter(models.Task.due_date <= filters["due_date"])

    # Sorting
    if sort == "priority":
        q = q.order_by(models.Task.priority.desc())
    elif sort == "due_date":
        q = q.order_by(models.Task.due_date.asc())

    return q.offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, owner_id: int, task_in: schemas.TaskUpdate):
    task = get_task(db, task_id, owner_id)
    if not task:
        return None
    for field, value in task_in.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, owner_id: int):
    task = get_task(db, task_id, owner_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True
