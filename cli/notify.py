import subprocess
import json
from datetime import date


def get_unchecked_habits(habits: dict) -> list:
    """Returns a list of unchecked habits from the given habits dictionary

    Args:
        habits (dict): Dictionary with habit names and bool values if checked

    Returns:
        list: List of unchecked habit names
    """
    today = date.today().isoformat()
    return [name for name, info in habits.items() if info["last_checked"] != today]


def get_data(filepath="data/habits.json") -> dict:
    """Reads habit data from a JSON file"""
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data


def send_notification():
    """Sends a desktop notification using osascript (macOS)

    Args:
        title (str): Title of the notification
        message (str): Message body of the notification
    """
    unchecked_habits = get_unchecked_habits(get_data())
    for habit in unchecked_habits:
        message = f"You have not completed your habit: {habit}"
        script = f'display notification "{message}" with title "Habit Tracker" sound name "Ping"'
        subprocess.run(["osascript", "-e", script], check=True)


def send_task_notification():
    """Sends a desktop notification for tasks due today using osascript (macOS)"""
    try:
        with open("data/tasks.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = {}

    today = date.today().isoformat()
    tasks_due_today = [
        name
        for name, info in tasks.items()
        if info["due"] == today and not info.get("completed", False)
    ]

    for task in tasks_due_today:
        message = f"You have a task due today: {task}"
        script = f'display notification "{message}" with title "Task Reminder" sound name "Ping"'
        subprocess.run(["osascript", "-e", script], check=True)


if __name__ == "__main__":
    send_notification()
    send_task_notification()
