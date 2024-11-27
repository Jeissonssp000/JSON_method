import os
import json
from datetime import timedelta, datetime
import pandas as pd
import webbrowser
import tempfile


class MetricsHandler:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def generate_metrics(self):
        summary = []
        validation_messages = []

        for file_name in os.listdir(self.data_dir):
            if file_name == "config.json" or not file_name.endswith(".json"):
                continue

            with open(os.path.join(self.data_dir, file_name), "r", encoding="utf-8") as file:
                data = json.load(file)

            total_time = timedelta()
            pause_time = timedelta()
            longest_task = {"name": "", "duration": timedelta(seconds=0)}
            shortest_task = {"name": "", "duration": timedelta.max}
            previous_end_time = None

            for end_time, details in sorted(data.items()):
                try:
                    duration, task_name = details.split(" ", 1)
                    h, m, s = map(int, duration.split(":"))
                    task_duration = timedelta(hours=h, minutes=m, seconds=s)

                    current_end_time = datetime.strptime(end_time, "%H:%M:%S")
                    current_start_time = current_end_time - task_duration

                    if "Pausa" not in task_name:
                        if previous_end_time and current_start_time < previous_end_time:
                            validation_messages.append(
                                f"Archivo '{file_name}': Tarea '{task_name}', fin: {current_end_time.time()}"
                            )

                        previous_end_time = current_end_time

                    total_time += task_duration

                    if "Pausa" in task_name:
                        pause_time += task_duration
                    else:
                        if task_duration > longest_task["duration"]:
                            longest_task = {"name": task_name, "duration": task_duration}
                        if task_duration < shortest_task["duration"]:
                            shortest_task = {"name": task_name, "duration": task_duration}

                except ValueError as e:
                    validation_messages.append(
                        f"Error al procesar la tarea: {details} en el archivo {file_name}. Error: {e}"
                    )
                    continue

            try:
                file_date = datetime.strptime(file_name.split(".")[0], "%Y-%m-%d").date()
            except ValueError:
                file_date = None

            summary.append(
                {
                    "Fecha": file_date,
                    "Horas": total_time,
                    "Pausas": pause_time,
                    "Tarea larga": longest_task,
                    "Tarea corta": (
                        shortest_task
                        if shortest_task["duration"] != timedelta.max
                        else {"name": "N/A", "duration": timedelta(0)}
                    ),
                }
            )

        df_summary = pd.DataFrame(
            {
                "Fecha": [day["Fecha"] for day in summary],
                "Horas": [str(day["Horas"]) for day in summary],
                "Pausas": [str(day["Pausas"]) for day in summary],
                "Tarea larga": [f"{day['Tarea larga']['duration']}" for day in summary],
                "Tarea corta": [f"{day['Tarea corta']['duration']}" for day in summary],
            }
        )

        df_summary = df_summary.sort_values(by="Fecha", ascending=False)

        # Crear contenido HTML con los mensajes y la tabla
        html_header = "<h1>Resumen de métricas</h1>"
        html_validations = (
            "<h2>Validaciones:</h2><ul>"
            + "".join([f"<li>{msg}</li>" for msg in validation_messages])
            + "</ul>"
            if validation_messages
            else "<h2>No se encontraron problemas de validación.</h2>"
        )
        html_styles = """
        <style>
            table {
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 6px;
                text-align: left;
            }
        </style>
        """
        html_table = df_summary.to_html(index=False, justify="center")
        html_content = f"{html_styles}{html_header}{html_validations}{html_table}"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            tmp_file.write(html_content.encode("utf-8"))
            tmp_file_path = tmp_file.name

        webbrowser.open(f"file://{tmp_file_path}")
