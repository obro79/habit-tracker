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
        script = f'display notification "{message}" with title "Habit Tracker"'
        subprocess.run(["osascript", "-e", script], check=True)


if __name__ == "__main__":
    send_notification()
