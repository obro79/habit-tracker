from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import db

router = APIRouter()


class TaskCreate(BaseModel):
    taskId: str
    category: str
    dueDate: datetime
    priority: str


class Task(BaseModel):
    id: str
    taskId: str
    category: str
    userId: str
    dueDate: datetime
    priority: str


@router.get("/{task_id}", response_model=Task)
async def get_task(user_id: str, task_id: str):
    task = await db.task.find_unique(where={"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=list[Task])
async def list_tasks(user_id: str):
    tasks = await db.task.find_many(where={"userId": user_id})
    return tasks


@router.post("/", response_model=Task)
async def create_task(user_id: str, task: TaskCreate):
    new_task = await db.task.create(
        data={
            "taskId": task.taskId,
            "category": task.category,
            "dueDate": task.dueDate,
            "priority": task.priority,
            "user": {"connect": {"id": user_id}},
        }
    )
    return new_task


@router.delete("/{task_id}")
async def delete_task(user_id: str, task_id: str):
    task = await db.task.find_unique(where={"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.task.delete(where={"id": task_id})
    return {"detail": "Task deleted"}
