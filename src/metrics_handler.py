import os
import json
from datetime import timedelta, datetime
import pandas as pd
import webbrowser
import tempfile

folder_path = os.path.dirname(os.path.abspath(__file__))
summary = []

for file_name in os.listdir(folder_path):
    if file_name == "config.json" or not file_name.endswith(".json"):
        continue

    with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
        data = json.load(file)

    total_time = timedelta()
    pause_time = timedelta()
    longest_task = {"name": "", "duration": timedelta(seconds=0)}
    shortest_task = {"name": "", "duration": timedelta.max}
    previous_end_time = None  # Almacena el final de la última tarea no pausa

    for end_time, details in sorted(data.items()):  # Ordenar las tareas por hora
        try:
            duration, task_name = details.split(" ", 1)
            h, m, s = map(int, duration.split(":"))
            task_duration = timedelta(hours=h, minutes=m, seconds=s)

            # Calcular la hora de inicio de la tarea actual
            current_end_time = datetime.strptime(end_time, "%H:%M:%S")
            current_start_time = current_end_time - task_duration

            # Validar solapamientos si no es pausa
            if "Pausa" not in task_name:
                if previous_end_time and current_start_time < previous_end_time:
                    print(
                        f"Archivo '{file_name}': "
                        f"Tarea '{task_name}', fin: {current_end_time.time()} "
                    )

                # Actualizar el tiempo de finalización anterior solo para tareas no pausa
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
            print(
                f"Error al procesar la tarea: {details} en el archivo {file_name}. Error: {e}"
            )
            continue

    # Extraer fecha del nombre del archivo, asumir formato YYYY-MM-DD.json
    try:
        file_date = datetime.strptime(file_name.split(".")[0], "%Y-%m-%d").date()
    except ValueError:
        file_date = None  # Si no se puede parsear, usar None

    summary.append(
        {
            "Archivo": file_name,
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
        "Archivo": [day["Archivo"] for day in summary],
        "Fecha": [day["Fecha"] for day in summary],
        "Horas": [str(day["Horas"]) for day in summary],
        "Pausas": [str(day["Pausas"]) for day in summary],
        "Tarea larga": [
            f"{day['Tarea larga']['duration']}"
            for day in summary
        ],
        "Tarea corta": [
            f"{day['Tarea corta']['duration']}"
            for day in summary
        ],
    }
)

df_summary = df_summary.sort_values(by="Fecha", ascending=False)
html_content = df_summary.to_html(index=False, justify="center")
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    tmp_file.write(html_content.encode("utf-8"))
    tmp_file_path = tmp_file.name
webbrowser.open(f"file://{tmp_file_path}")
