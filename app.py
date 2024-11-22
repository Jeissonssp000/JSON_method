from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
)
from PyQt5.QtCore import QTimer, QTime, Qt
import datetime
import pygame
import json
import sys
import os


class App(QWidget):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        file_path = os.path.abspath("soft.wav")
        if not os.path.exists(file_path):
            print(f"Archivo de sonido no encontrado: {file_path}")
            return

        self.data_dir = "app_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.remaining_time = QTime(0, 0, 0)
        self.initial_time = QTime(0, 0, 0)
        pygame.mixer.music.load(file_path)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("JSON_method")
        self.setGeometry(100, 100, 210, 200)

        # Hacer que la ventana sea flotante
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = QTime(0, 0, 0)

        # Input
        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("hh:mm:ss, mm:ss o ss")

        # Conectar el evento keyPressEvent al QLineEdit
        self.time_input.installEventFilter(self)

        # Botón de iniciar/detener
        self.start_stop_button = QPushButton("Iniciar", self)
        self.start_stop_button.clicked.connect(self.start_stop_timer)

        # Label de tiempo restante
        self.remaining_label = QLabel("00:00:00", self)
        self.remaining_label.setAlignment(Qt.AlignCenter)
        self.remaining_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        # Área de anotaciones
        self.notes_text = QTextEdit(self)
        self.notes_text.setPlaceholderText("Escribe tus anotaciones aquí...")

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout para input y botón
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.time_input)
        input_layout.addWidget(self.start_stop_button)

        # Añadir widgets al layout principal
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.remaining_label)
        main_layout.addWidget(self.notes_text)

        self.setLayout(main_layout)

        # Cargar datos guardados
        self.load_last_data()

    def eventFilter(self, source, event):
        # Detectar si el foco está en el QLineEdit y se presiona espacio o enter
        if source == self.time_input and event.type() == event.KeyPress:
            if event.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
                self.start_stop_timer()
                return True
        return super().eventFilter(source, event)

    def parse_input_time(self):
        input_time = self.time_input.text().strip()
        hours, minutes, seconds = 0, 0, 0

        try:
            if ":" in input_time:
                parts = input_time.split(":")
                # Caso hh:mm:ss
                if len(parts) == 3:
                    hours = int(parts[0]) if parts[0] else 0
                    minutes = int(parts[1]) if parts[1] else 0
                    seconds = int(parts[2]) if parts[2] else 0
                # Caso mm:ss
                elif len(parts) == 2:
                    minutes = int(parts[0]) if parts[0] else 0
                    seconds = int(parts[1]) if parts[1] else 0
            else:
                # Caso ss
                total_seconds = int(input_time)
                minutes, seconds = divmod(total_seconds, 60)

            # Ajustar los valores al formato QTime
            while seconds >= 60:
                minutes += 1
                seconds -= 60
            while minutes >= 60:
                hours += 1
                minutes -= 60

        except ValueError:
            hours, minutes, seconds = 0, 0, 0

        return QTime(hours, minutes, seconds)

    def start_stop_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_stop_button.setText("Iniciar")
            self.save_activity()  # Guardar datos al detener
        else:
            self.initial_time = self.parse_input_time()
            self.remaining_time = self.initial_time
            self.update_remaining_label()
            self.timer.start(1000)
            self.start_stop_button.setText("Detener")

    def update_timer(self):
        if self.remaining_time <= QTime(0, 0, 1):
            self.timer.stop()
            self.start_stop_button.setText("Iniciar")
            self.remaining_time = QTime(0, 0, 0)
            self.update_remaining_label()
            self.save_activity()
            pygame.mixer.music.play()
        else:
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.update_remaining_label()

    def update_remaining_label(self):
        self.remaining_label.setText(self.remaining_time.toString("hh:mm:ss"))

    def calculate_elapsed_time(self):
        initial_seconds = (
            self.initial_time.hour() * 3600
            + self.initial_time.minute() * 60
            + self.initial_time.second()
        )
        remaining_seconds = (
            self.remaining_time.hour() * 3600
            + self.remaining_time.minute() * 60
            + self.remaining_time.second()
        )
        elapsed_seconds = initial_seconds - remaining_seconds
        return QTime(0, 0, 0).addSecs(elapsed_seconds).toString("hh:mm:ss")

    def save_config(self):
        config_data = {
            "last_time": self.time_input.text(),
            "notes": self.notes_text.toPlainText(),
        }

        with open("app_data/config.json", "w") as config_file:
            json.dump(config_data, config_file, indent=4)

    def save_activity(self):
        """
        Guarda el registro de actividades en un archivo diario.
        """
        # Obtener la fecha y hora actuales
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        elapsed_time = self.calculate_elapsed_time()
        notes = self.notes_text.toPlainText()

        # Archivo diario con el formato YYYY-MM-DD.json
        activity_file = f"app_data/{current_date}.json"
        activity_data = {}

        # Cargar datos existentes si el archivo ya existe
        if os.path.exists(activity_file):
            with open(activity_file, "r") as activity_file_content:
                try:
                    activity_data = json.load(activity_file_content)
                except json.JSONDecodeError:
                    activity_data = {}

        # Agregar la actividad con la hora como clave
        activity_data[current_time] = f"{elapsed_time} {notes}"

        # Guardar los datos en el archivo diario
        with open(activity_file, "w") as activity_file_content:
            json.dump(activity_data, activity_file_content, indent=4)

    def load_last_data(self):
        if os.path.exists("app_data/config.json"):
            with open("app_data/config.json", "r") as file:
                try:
                    data = json.load(file)
                    self.time_input.setText(data.get("last_time", ""))
                    self.notes_text.setPlainText(data.get("notes", ""))
                except json.JSONDecodeError:
                    pass

    def closeEvent(self, event):
        self.save_config()
        if self.timer.isActive():
            self.save_activity()
        event.accept()


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
