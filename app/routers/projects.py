# app/routers/projects.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, database, auth

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    return crud.create_project(db, current_user.id, project_in)

@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    return crud.get_projects_for_user(db, current_user.id)

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    p = crud.get_project_with_tasks(db, project_id, current_user.id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@router.patch("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, project_in: schemas.ProjectUpdate, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    p = crud.update_project(db, project_id, current_user.id, project_in)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found or not yours")
    return p

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(database.get_db), current_user = Depends(auth.get_current_user)):
    ok = crud.delete_project(db, project_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found or not yours")
    return
