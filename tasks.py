import argparse
from ast import arg
from datetime import date
from utils import get_json, save_json

habit_file_path = "data/tasks.json"


def add_task(args):
    data = get_json(habit_file_path)
    new_task = {
        "description": args.description,
        "due": args.due,
        "priority": args.priority,
        "category": args.category,
        "completed": False,
    }
    data[args.name] = new_task
    save_json(data, habit_file_path)


def complete_task(args):
    data = get_json(habit_file_path)
    if args.name in data:
        data[args.name]["completed"] = True
        save_json(data, habit_file_path)
    else:
        print(f"Task '{args.name}' not found.")


def list_today_tasks(args):
    data = get_json(habit_file_path)
    today = date.today().isoformat()
    tasks_due_today = [
        (name, info)
        for name, info in data.items()
        if info["due"] == today and not info.get("completed", False)
    ]
    if not tasks_due_today:
        print("No tasks due today.")
        return


def main():
    parser = argparse.ArgumentParser(description="Todo List CLI")
    sub_parsers = parser.add_subparsers(dest="command")

    add_parser = sub_parsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("name", type=str, help="Task name")
    add_parser.add_argument(
        "--description", type=str, help="Task description", default=""
    )
    add_parser.add_argument(
        "--due", type=str, help="Due date", default=date.today().isoformat()
    )
    add_parser.add_argument(
        "--priority", type=str, help="Task priority", default="Medium"
    )
    add_parser.add_argument(
        "--category", type=str, help="Task category", default="Misc"
    )
    add_parser.set_defaults(func=add_task)

    complete_parser = sub_parsers.add_parser("complete", help="Complete a task")
    complete_parser.add_argument("name", type=str, help="Task name")
    complete_parser.set_defaults(func=complete_task)

    list_today_parser = sub_parsers.add_parser("list-today", help="List today's tasks")
    list_today_parser.set_defaults(func=list_today_tasks)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
