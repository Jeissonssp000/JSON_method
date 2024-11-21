from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import QTimer, QTime, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import json
import sys
import os


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Temporizador")
        self.setGeometry(100, 100, 300, 200)

        # Hacer que la ventana sea flotante
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = QTime(0, 0, 0)

        # Cargar último tiempo guardado
        last_time = self.load_last_time()

        # Input
        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Tiempo en formato hh:mm:ss, mm:ss o ss")
        self.time_input.setText(last_time)

        # Botón de iniciar/detener
        self.start_stop_button = QPushButton("Iniciar", self)
        self.start_stop_button.clicked.connect(self.start_stop_timer)

        # Label de tiempo restante
        self.remaining_label = QLabel("00:00:00", self)
        self.remaining_label.setAlignment(Qt.AlignCenter)
        self.remaining_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout para input y botón
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.time_input)
        input_layout.addWidget(self.start_stop_button)

        # Añadir widgets al layout principal
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.remaining_label)

        self.setLayout(main_layout)

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
        else:
            self.remaining_time = self.parse_input_time()
            self.update_remaining_label()
            self.save_last_time(self.time_input.text().strip())
            self.timer.start(1000)
            self.start_stop_button.setText("Detener")

    def update_timer(self):
        if self.remaining_time == QTime(0, 0, 0):
            self.timer.stop()
            self.start_stop_button.setText("Iniciar")
            self.play_sound()
        else:
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.update_remaining_label()

    def update_remaining_label(self):
        self.remaining_label.setText(f"{self.remaining_time.toString('hh:mm:ss')}")

    def play_sound(self):
        file_path = os.path.abspath("soft.wav")
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.player.stateChanged.connect(self.handle_state_change)
        self.play_count = 0
        self.player.play()

    def handle_state_change(self, state):
        if state == QMediaPlayer.StoppedState:
            self.play_count += 1
            if self.play_count < 2:
                self.player.play()

    def save_last_time(self, time_str):
        data = {"last_time": time_str}
        with open("config.json", "w") as file:
            json.dump(data, file)

    def load_last_time(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                data = json.load(file)
                return data.get("last_time", "")
        return ""


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
