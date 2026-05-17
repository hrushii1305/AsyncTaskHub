from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.auth import get_current_user
from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

async def get_current_user_obj(current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == current_user))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_obj)):
    new_task = Task(
        user_id=current_user.id,
        title=task.title,
        description=task.description,
        priority=task.priority
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    from app.tasks import process_task
    process_task.delay(str(new_task.id), new_task.title, new_task.description)

    return new_task

@router.get("/", response_model=list[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_obj)):
    result = await db.execute(select(Task).where(Task.user_id == current_user.id))
    tasks = result.scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_obj)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: UUID, updates: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_obj)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_obj)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()
    return {"message": "Task deleted"}