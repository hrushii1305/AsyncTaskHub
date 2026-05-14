# AsyncTaskHub

A REST API for managing and processing tasks asynchronously. Built with FastAPI and PostgreSQL, it uses Celery and Redis for background task processing — users get instant responses while heavy work happens in the background.

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** — ORM
- **Redis** — message queue
- **Celery** — background task worker
- **JWT** — authentication
- **Docker** — containerization
- **GitHub Actions** — CI/CD

## Features

- User registration and login with JWT authentication
- Create, read, update, delete tasks
- Async background task processing via Celery + Redis
- Dockerized — runs with one command
- CI pipeline with GitHub Actions

## Run with Docker

```bash
docker-compose up --build
```

API available at: `http://localhost:8000/docs`

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8001
```

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /auth/register | Register user | No |
| POST | /auth/login | Login and get token | No |
| GET | /tasks/ | Get all tasks | Yes |
| POST | /tasks/ | Create a task | Yes |
| GET | /tasks/{id} | Get one task | Yes |
| PATCH | /tasks/{id} | Update a task | Yes |
| DELETE | /tasks/{id} | Delete a task | Yes |