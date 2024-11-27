import json
import os
import datetime
import sys


def get_app_path():
    if getattr(sys, "frozen", False):  # Si está empaquetado con PyInstaller
        return os.path.dirname(sys.executable)
    else:  # Si está en un entorno de desarrollo (sin empaquetar)
        return os.path.dirname(os.path.abspath(__file__))


class DataHandler:
    def __init__(self, data_dir="app_data"):
        base_path = get_app_path()
        self.data_dir = os.path.join(base_path, data_dir)

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save_config(self, time_input, notes_text):
        config_path = os.path.join(self.data_dir, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                try:
                    config_data = json.load(config_file)
                except json.JSONDecodeError:
                    config_data = {}
        else:
            config_data = {}

        config_data["last_time"] = time_input
        config_data["notes"] = notes_text

        with open(config_path, "w") as config_file:
            json.dump(config_data, config_file, indent=4)

    def load_last_data(self):
        config_path = os.path.join(self.data_dir, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    pass

        # Configuración por defecto si no existe o está corrupto
        default_data = {
            "last_time": "",
            "notes": "",
            "reminders": [
                {"time": "10:00", "message": "Toma agüita, es importante estar hidratado."},
                {"time": "11:00", "message": "Estiramientos para el cuerpo."},
                {"time": "12:00", "message": "Toma agüita, es importante estar hidratado."},
                {"time": "15:00", "message": "Toma agüita, es importante estar hidratado."},
                {"time": "16:00", "message": "Estiramientos para el cuerpo."},
                {"time": "17:00", "message": "Toma agüita, es importante estar hidratado."},
            ],
        }

        # Guardar el archivo con la configuración por defecto
        with open(config_path, "w") as file:
            json.dump(default_data, file, indent=4)

        return default_data

    def save_activity(self, elapsed_time, notes):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        activity_file = os.path.join(self.data_dir, f"{current_date}.json")
        activity_data = {}

        if os.path.exists(activity_file):
            with open(activity_file, "r") as activity_file_content:
                try:
                    activity_data = json.load(activity_file_content)
                except json.JSONDecodeError:
                    activity_data = {}

        activity_data[current_time] = f"{elapsed_time} {notes}"

        with open(activity_file, "w") as activity_file_content:
            json.dump(activity_data, activity_file_content, indent=4)
