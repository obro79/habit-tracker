from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import db

router = APIRouter()


class HabitCreate(BaseModel):
    name: str
    description: str
    frequency: str
    userId: str


class Habit(BaseModel):
    id: str
    name: str
    description: str
    frequency: str
    userId: str


class HabitUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    frequency: str | None = None
    userId: str | None = None


@router.get("/{task_id}", response_model=Habit)
async def get_habit(habit_id: str):
    habit = await db.habit.find_unique(where={"id": habit_id})
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.get("/", response_model=list[Habit])
async def list_habits(user_id: str):
    habits = await db.habit.find_many(where={"userId": user_id})
    return habits


@router.post("/", response_model=Habit)
async def create_habit(habit: HabitCreate):
    new_habit = await db.habit.create(
        data={
            "name": habit.name,
            "description": habit.description,
            "frequency": habit.frequency,
            "userId": habit.userId,
        }
    )
    return new_habit
