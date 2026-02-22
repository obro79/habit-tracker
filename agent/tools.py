from google import genai
from google.genai import types


# Tools


def add_habit(name: str, description: str, frequency: str):
    """
    Add a new habit for the user.

    Args:
        name (str): The name of the habit.
        description (str): A brief description of the habit.
        frequency (str): How often the habit should be performed (e.g., daily)
    """
    pass


def list_habits():
    """List all habits for the user."""
    pass


def add_task(
    name: str, due_date: str, priority: str, description: str = "", category: str = ""
):
    """Adds a task for to a users task list

    Args:
        name (str): name of the task
        due_date (str): due date for the task in ISO format (YYYY-MM-DD)
        priority (str): priority level of the task (e.g., low, medium, high)
        description (str, optional): description of the task. Defaults to "".
        category (str, optional): category of the task. Defaults to "".
    """
    pass


def list_tasks():
    """List all tasks for the user."""
    pass


def check_habit(habit: str):
    """Marks a habit as completed for the day."""
    pass


def check_task(task: str):
    """Marks a task as complete

    Args:
        task (str): takes in a task
    """
    pass


def plan_day():
    pass


def get_unfinished_tasks():
    """
    Returns a list of unfinished tasks for the user.
    """
    pass


def get_unfinished_habits():
    """
    Returns a list of unfinished habits for the user.
    """
    pass


client = genai.Client()
tools = [
    add_habit,
    list_habits,
    add_task,
    list_tasks,
    check_habit,
    check_task,
    plan_day,
    get_unfinished_tasks,
    get_unfinished_habits,
]

config = types.GenerateContentConfig(
    tools=tools,
    max_output_tokens=4096,
)

response = client.models.generate_content(
    model="gemini-2-flash",
    contents="What should I do today?",  # TODO
    config=config,
)
