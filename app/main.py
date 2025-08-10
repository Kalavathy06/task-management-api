
from fastapi import FastAPI
from app.routers import projects, tasks, users

app = FastAPI(title="Task Management API")

app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Task Management API is running"}
