import argparse
import json

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
    print(f"Checking off habit: {args.name}")


def remove_habit(args):
    print(f"Removing habit: {args.name}")


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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
