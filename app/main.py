from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import db
from app.routes import habits, tasks, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(title="Habit Tracker API", lifespan=lifespan)

app.include_router(habits.router, prefix="/habits", tags=["habits"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/users", tags=["users"])
