from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import db

router = APIRouter()


class UserCreate(BaseModel):
    email: str
    password: str
    phoneNumber: str


class User(BaseModel):
    id: str
    email: str
    phoneNumber: str | None = None


class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None
    phoneNumber: str | None = None


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[User])
async def list_users():
    users = await db.user.find_many()
    return users


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    user = await db.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.habit.delete_many(where={"userId": user_id})
    await db.task.delete_many(where={"userId": user_id})
    await db.user.delete(where={"id": user_id})
    return {"detail": "User deleted"}


@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    new_user = await db.user.create(
        data={
            "email": user.email,
            "password": user.password,
            "phoneNumber": user.phoneNumber,
        }
    )
    return new_user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: UserUpdate):
    existing_user = await db.user.find_unique(where={"id": user_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await db.user.update(
        where={"id": user_id},
        data={
            "email": user.email if user.email is not None else existing_user.email,
            "password": (
                user.password if user.password is not None else existing_user.password
            ),
            "phoneNumber": (
                user.phoneNumber if user.phoneNumber is not None else existing_user.phoneNumber
            ),
        },
    )
    return updated_user


