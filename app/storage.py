import json
import os


class JsonStorage:
    def __init__(self, file_path: str = "data/users.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump({}, file)

    def load_data(self) -> dict:
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_data(self, data: dict):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)