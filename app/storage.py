import json
import os


class JsonStorage:
    def __init__(self, file_path="data/users.json"):
        self.file_path = file_path
        self.create_storage()

    def create_storage(self):
        folder = os.path.dirname(self.file_path)

        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump({}, file)

    def load_data(self):
        self.create_storage()

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_data(self, data):
        self.create_storage()

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)