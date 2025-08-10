# MacV AI Task API

A robust **Task Management System API** built with **FastAPI**, **PostgreSQL**, **Redis**, and **Celery** for background task processing and scheduled jobs.  
Includes JWT authentication, task assignment email notifications, daily overdue task summaries, and filtering/pagination support.

---

## 🚀 Live Deployment

- **API Base URL:** `https://your-deployed-api.com`
- **Sample Credentials:**
  - **Username:** testuser
  - **Password:** Test@1234

---

## 📂 Features

- User registration & login (JWT Auth)
- CRUD operations for Projects & Tasks
- Task assignment email notifications
- Daily overdue task summaries (Celery Beat)
- Filtering, sorting, and pagination for tasks
- Alembic migrations for DB schema management
- Dockerized with `docker-compose` for local setup

---

## 🛠 Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **Cache/Broker:** Redis
- **Task Queue:** Celery
- **Containerization:** Docker & Docker Compose
- **ORM:** SQLAlchemy + Alembic

---

## 🖥 Local Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Kalavathy06/task-management-api.git
cd macv-ai-task-api
