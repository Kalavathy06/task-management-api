# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# --- Tokens ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Users ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: Optional[str]

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str] = Field(None, min_length=6)

# --- Projects ---
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

class ProjectOut(ProjectBase):
    id: int
    owner_id: int
    tasks: List["TaskOut"] = []
    created_at: datetime
    class Config:
        form_attributes = True

# --- Tasks ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime]
    priority: Optional[str]
    status: Optional[str]
    assignee_id: Optional[int]
    project_id: Optional[int]

class TaskCreate(TaskBase):
    project_id: int  # required on creation

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
    priority: Optional[str]
    status: Optional[str]
    assignee_id: Optional[int]

class TaskOut(TaskBase):
    id: int
    project: Optional[ProjectBase]
    assignee: Optional[UserOut]
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# allow forward refs
ProjectOut.update_forward_refs()
