import argparse


def add_habit(name):
    pass


def list_habits():
    pass


def check_habit(name):
    pass


def remove_habit(name):
    pass


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
