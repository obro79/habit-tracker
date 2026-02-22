from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import db

router = APIRouter()


class HabitCreate(BaseModel):
    name: str
    description: str
    frequency: str


class Habit(BaseModel):
    id: str
    name: str
    description: str
    frequency: str
    userId: str


@router.get("/{habit_id}", response_model=Habit)
async def get_habit(user_id: str, habit_id: str):
    habit = await db.habit.find_unique(where={"id": habit_id, "userId": user_id})
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.get("/", response_model=list[Habit])
async def list_habits(user_id: str):
    habits = await db.habit.find_many(where={"userId": user_id})
    return habits


@router.post("/", response_model=Habit)
async def create_habit(user_id: str, habit: HabitCreate):
    new_habit = await db.habit.create(
        data={
            "name": habit.name,
            "description": habit.description,
            "frequency": habit.frequency,
            "user": {"connect": {"id": user_id}},
        }
    )
    return new_habit
