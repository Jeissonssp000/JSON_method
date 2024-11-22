import os
import json
import datetime


class DataHandler:
    def __init__(self, base_dir="app_data"):
        self.base_dir = base_dir
        self.config_file = os.path.join(self.base_dir, "config.json")

        # Crear la carpeta base si no existe
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def save_config(self, last_time, notes):
        config_data = {"last_time": last_time, "notes": notes}
        with open(self.config_file, "w") as file:
            json.dump(config_data, file, indent=4)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    pass
        return {"last_time": "", "notes": ""}

    def save_activity(self, elapsed_time, notes):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        activity_file = os.path.join(self.base_dir, f"{current_date}.json")
        activity_data = {}

        if os.path.exists(activity_file):
            with open(activity_file, "r") as file:
                try:
                    activity_data = json.load(file)
                except json.JSONDecodeError:
                    pass

        activity_data[current_time] = f"{elapsed_time} {notes}"

        with open(activity_file, "w") as file:
            json.dump(activity_data, file, indent=4)
