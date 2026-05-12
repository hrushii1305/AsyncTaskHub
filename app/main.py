from fastapi import FastAPI
from app.database import engine, Base
from app.models.task import Task
from app.models.user import User
from app.routers.tasks import router as tasks_router
from app.routers.auth import router as auth_router

app = FastAPI(title="AsyncTaskHub")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(tasks_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "AsyncTaskHub is running!"}