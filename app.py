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
from PyQt5.QtCore import Qt
import sys
from src.audio_handler import AudioHandler
from src.data_handler import DataHandler
from src.flash_handler import FlashHandler
from src.notify_handler import NotifyHandler
from src.timer_handler import TimerHandler


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_handler = AudioHandler()
        self.data_handler = DataHandler()
        self.timer_handler = TimerHandler(
            self, self.update_remaining_label, self.on_timer_end
        )
        self.flash_handler = FlashHandler(self)
        self.notify_handler = NotifyHandler(
            self, self.timer_handler.timer, self.audio_handler, self.data_handler
        )
        self.initUI()

    def initUI(self):
        self.setWindowTitle("JSON_method")
        self.setGeometry(100, 100, 210, 200)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Input
        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("hh:mm:ss, mm:ss o ss")
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
        if source == self.time_input and event.type() == event.KeyPress:
            if event.key() in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter):
                self.start_stop_timer()
                return True
        return super().eventFilter(source, event)

    def start_stop_timer(self):
        if self.timer_handler.timer.isActive():
            self.timer_handler.stop_timer()
            self.start_stop_button.setText("Iniciar")
            self.save_activity()
        else:
            self.timer_handler.start_timer(self.time_input.text().strip())
            self.start_stop_button.setText("Detener")

    def update_remaining_label(self, time):
        self.remaining_label.setText(time.toString("hh:mm:ss"))

    def on_timer_end(self):
        self.start_stop_button.setText("Iniciar")
        self.save_activity()
        self.audio_handler.play_audio()
        self.flash_handler.start_flash()

    def save_activity(self):
        elapsed_time = self.timer_handler.calculate_elapsed_time()
        notes = self.notes_text.toPlainText()
        self.data_handler.save_activity(elapsed_time, notes)

    def load_last_data(self):
        data = self.data_handler.load_last_data()
        self.time_input.setText(data.get("last_time", ""))
        self.notes_text.setPlainText(data.get("notes", ""))

    def closeEvent(self, event):
        self.data_handler.save_config(
            self.time_input.text(), self.notes_text.toPlainText()
        )
        if self.timer_handler.timer.isActive():
            self.save_activity()
        self.audio_handler.cleanup()
        event.accept()


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
