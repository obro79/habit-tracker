import argparse
import json
from datetime import date, timedelta

file_path = "data/habits.json"


def get_json(file_path=file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data


def save_json(data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def add_habit(args):
    """Adds the habit to the Json file

    Args:
        args (_type_): _command line arguments
    """
    print(f"Adding habit: {args.name}")
    new_entry = {
        "name": args.name,
        "streak": 0,
        "last_checked": None,
    }

    data = get_json()

    if args.name in data:
        print(f"Error: Habit '{args.name}' already exists.")
        return
    data[args.name] = new_entry

    save_json(data)
    print(f"Habit '{args.name}' added successfully.")


def list_habits(args):
    """List all habits in the Json file"""

    data = get_json()
    if not data:
        print("No habits found.")
        return

    res = [f"- {habit['name']}: Streak {habit['streak']}" for habit in data.values()]
    for line in res:
        print(line)


def check_habit(args):
    """Check off a habit for today"""

    data = get_json()
    if args.name not in data:
        raise ValueError(f"Habit '{args.name}' does not exist.")

    habit = data[args.name]
    last_checked = (
        date.fromisoformat(habit["last_checked"]) if habit["last_checked"] else None
    )
    today = date.today()
    if last_checked == today:
        print(f"Habit '{args.name}' already checked for today.")
        return
    elif last_checked == today - timedelta(days=1):
        habit["streak"] += 1
    else:
        habit["streak"] = 1

    habit["last_checked"] = today.isoformat()

    save_json(data)
    print(f"Habit '{args.name}' checked successfully.")


def get_streak(args):
    """Get the current streak of a habit"""

    data = get_json()
    if args.name not in data:
        raise ValueError(f"Habit '{args.name}' does not exist.")

    habit = data[args.name]
    print(f"Habit '{args.name}' has a streak of {habit['streak']}.")


def remove_habit(args):
    """Removes a habit from the Json file

    Args:
        args (_type_): _command line arguments
    """
    data = get_json()

    if args.name in data:
        del data[args.name]
        save_json(data)
    else:
        print(f"{args.name} was already removed")
        return

    print("Habit was removed successfully")


def main():
    parser = argparse.ArgumentParser(description="Habit Tracker CLI")

    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new habit")
    add_parser.add_argument("name", type=str, help="Name of the habit")
    add_parser.set_defaults(func=add_habit)

    check_parser = subparsers.add_parser("check", help="Check off a habit")
    check_parser.add_argument("name", type=str, help="Name of the habit")
    check_parser.set_defaults(func=check_habit)

    list_parser = subparsers.add_parser("list", help="List all habits")
    list_parser.set_defaults(func=list_habits)

    remove_parser = subparsers.add_parser("remove", help="Remove a habits")
    remove_parser.add_argument("name", type=str, help="Name of the habit")
    remove_parser.set_defaults(func=remove_habit)

    streak_parser = subparsers.add_parser("streak", help="Get habit streak")
    streak_parser.add_argument("name", type=str, help="Name of the habit")
    streak_parser.set_defaults(func=get_streak)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
