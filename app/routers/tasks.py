# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import schemas, crud, database, auth
from ..services.background_tasks import send_task_assignment_email, send_task_status_change_email

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    # verify project belongs to user
    proj = crud.get_project_with_tasks(db, task_in.project_id, current_user.id)
    if not proj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project not found or not yours")
    # optional: verify assignee exists
    if task_in.assignee_id:
        assignee = crud.get_user(db, task_in.assignee_id)
        if not assignee:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignee not found")
    task = crud.create_task(db, task_in)
    if task.assignee_id:
        send_task_assignment_email.delay(task.id)
    return task

@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    project_id: Optional[int] = None,
    due_date: Optional[str] = None,
    sort: Optional[str] = Query(None, regex="^(priority|due_date)$"),
    skip: int = 0, limit: int = 20,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.get_current_user)
):
    filters = {k: v for k, v in {"status": status, "priority": priority, "project_id": project_id, "due_date": due_date}.items() if v is not None}
    tasks = crud.list_tasks(db, current_user.id, filters, skip, limit, sort)
    return tasks

@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    t = crud.get_task(db, task_id, current_user.id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t

@router.patch("/{task_id}", response_model=schemas.TaskOut)
def patch_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    t = crud.get_task(db, task_id, current_user.id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")

    old_assignee = t.assignee_id
    old_status = t.status

    updated = crud.update_task(db, task_id, current_user.id, task_in)
    if not updated:
        raise HTTPException(status_code=400, detail="Unable to update task")

    # enqueue emails if assignment changed or status changed
    if task_in.assignee_id is not None and task_in.assignee_id != old_assignee:
        send_task_assignment_email.delay(updated.id)
    if task_in.status is not None and task_in.status != old_status:
        send_task_status_change_email.delay(updated.id)
    return updated

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    ok = crud.delete_task(db, task_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found or not yours")
    return
