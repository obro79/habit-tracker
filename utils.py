import json


def get_json(file_path="data/habits.json"):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data


def save_json(data, file_path="data/habits.json"):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
