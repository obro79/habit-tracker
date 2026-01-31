import argparse
import json
from datetime import date, timedelta

file_path = "data/habits.json"


def add_habit(args):
    """Adds the habit to the Json file

    Args:
        args (_type_): _command line arguments
    """
    print(f"Adding habit: {args.name}")
    new_entry = {
        "Name": args.name,
        "Streak": 0,
        "Last Checked": date.today().isoformat(),
    }

    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if args.name in data:
        raise ValueError(f"Habit '{args.name}' already exists.")
    data[args.name] = new_entry

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Habit '{args.name}' added successfully.")


def list_habits(args):
    """List all habits in the Json file"""
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    res = [f"- {habit['Name']}: Streak {habit['Streak']}" for habit in data.values()]
    for line in res:
        print(line)


def check_habit(args):
    """Check off a habit for today"""

    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    if args.name not in data:
        raise ValueError(f"Habit '{args.name}' does not exist.")

    habit = data[args.name]
    last_checked = date.fromisoformat(habit["Last Checked"])
    today = date.today()
    if last_checked == today:
        print(f"Habit '{args.name}' already checked for today.")
        return
    elif last_checked == today - timedelta(days=1):
        habit["Streak"] += 1
    else:
        habit["Streak"] = 1

    habit["Last Checked"] = today.isoformat()

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Habit '{args.name}' checked successfully.")


def remove_habit(args):
    """Removes a habit from the Json file

    Args:
        args (_type_): _command line arguments
    """
    try:
        with open(file_path, mode="r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if args.name in data:
        del data[args.name]
    else:
        print(f"{args.name} was already removed")

    with open(file_path, mode="w") as json_file:
        json.dump(data, json_file, indent=4)

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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
