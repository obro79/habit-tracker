from datetime import datetime

from app.db import db


# Tools


async def add_habit(user_id: str, name: str, description: str, frequency: str):
    """Add a new habit for the user.

    Args:
        user_id: The user's ID
        name: The name of the habit
        description: A brief description of the habit
        frequency: How often the habit should be performed (e.g., daily)
    """
    await db.habit.create(
        data={
            "name": name,
            "description": description,
            "frequency": frequency,
            "user": {"connect": {"id": user_id}},
        }
    )
    return {"status": "created", "name": name, "frequency": frequency}


async def list_habits(user_id: str):
    """List all habits for the user.

    Args:
        user_id: The user's ID
    """
    habits = await db.habit.find_many(where={"userId": user_id})
    return [
        {
            "name": h.name,
            "frequency": h.frequency,
            "currentStreak": h.currentStreak,
            "longestStreak": h.longestStreak,
        }
        for h in habits
    ]


async def add_task(
    user_id: str,
    name: str,
    due_date: str,
    priority: str,
    description: str = "",
    category: str = "Misc",
):
    """Adds a task to the user's task list.

    Args:
        user_id: The user's ID
        name: Name of the task
        due_date: Due date in ISO format (YYYY-MM-DD)
        priority: Priority level (low, medium, high)
        description: Description of the task
        category: Category of the task
    """
    await db.task.create(
        data={
            "taskId": name,
            "category": category,
            "dueDate": datetime.fromisoformat(due_date),
            "priority": priority,
            "user": {"connect": {"id": user_id}},
        }
    )
    return {
        "status": "created",
        "name": name,
        "due_date": due_date,
        "priority": priority,
    }


async def list_tasks(user_id: str):
    """List all tasks for the user.

    Args:
        user_id: The user's ID
    """
    tasks = await db.task.find_many(where={"userId": user_id})
    return [
        {
            "name": t.taskId,
            "category": t.category,
            "due": str(t.dueDate),
            "priority": t.priority,
        }
        for t in tasks
    ]


async def check_habit(user_id: str, name: str):
    """Marks a habit as completed for the day and updates the streak.

    Args:
        user_id: The user's ID
        name: The name of the habit to check off
    """
    found = await db.habit.find_first(where={"name": name, "userId": user_id})
    if not found:
        return {"status": "error", "message": "Habit not found"}

    await db.habit.update(
        where={"id": found.id},
        data={"currentStreak": found.currentStreak + 1},
    )
    return {
        "status": "checked",
        "name": found.name,
        "streak": found.currentStreak + 1,
    }


async def check_task(user_id: str, name: str):
    """Marks a task as complete by removing it.

    Args:
        user_id: The user's ID
        name: The name of the task to complete
    """
    found = await db.task.find_first(where={"taskId": name, "userId": user_id})
    if not found:
        return {"status": "error", "message": "Task not found"}

    await db.task.delete(where={"id": found.id})
    return {"status": "completed", "name": found.taskId}


async def get_unfinished_tasks(user_id: str):
    """Returns all tasks that are not yet completed for the user.

    Args:
        user_id: The user's ID
    """
    return await list_tasks(user_id)


async def get_unfinished_habits(user_id: str):
    """Returns habits the user hasn't checked off today.

    Args:
        user_id: The user's ID
    """
    return await list_habits(user_id)


async def plan_day(user_id: str):
    """Returns all habits and tasks to help the user plan their day.

    Args:
        user_id: The user's ID
    """
    habits = await list_habits(user_id)
    tasks = await list_tasks(user_id)
    return {"habits": habits, "tasks": tasks}


ALL_TOOLS = [
    add_habit,
    list_habits,
    add_task,
    list_tasks,
    check_habit,
    check_task,
    get_unfinished_tasks,
    get_unfinished_habits,
    plan_day,
]

TOOL_MAP = {tool.__name__: tool for tool in ALL_TOOLS}
