from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import db
from app.routes import habits, tasks, users
from agent.webhook import router as webhook_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(title="Habit Tracker API", lifespan=lifespan)

app.include_router(habits.router, prefix="/users/{user_id}/habits", tags=["habits"])
app.include_router(tasks.router, prefix="/users/{user_id}/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(webhook_router, tags=["webhook"])
