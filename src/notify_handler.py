from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer, QTime, QDateTime


class NotifyHandler:
    def __init__(self, parent, timer, audio_handler, data_handler):
        self.parent = parent
        self.timer = timer
        self.audio_handler = audio_handler
        self.data_handler = data_handler
        self.reminders = [
            {"time": "10:00", "message": "Toma agüita, es importante estar hidratado."},
            {"time": "11:30", "message": "Estiramientos para el cuerpo."},
            {"time": "13:00", "message": "Toma agüita, es importante estar hidratado."},
            {"time": "11:53", "message": "Toma agüita, es importante estar hidratado."},
        ]

        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.check_reminders)
        self.notification_timer.start(60000)

        self.pause_start_time = None
        self.was_timer_active = False

    def check_reminders(self):
        current_time = QTime.currentTime().toString("hh:mm")
        for reminder in self.reminders:
            if reminder["time"] == current_time:
                self.handle_reminder(reminder["message"])

    def handle_reminder(self, message):
        self.pause_start_time = QDateTime.currentDateTime()
        self.was_timer_active = self.timer.isActive()
        if self.was_timer_active:
            self.timer.stop()

        self.audio_handler.play_audio()

        notification = QMessageBox(self.parent)
        notification.setWindowTitle("Recordatorio")
        notification.setText(message)
        notification.setIcon(QMessageBox.Information)
        notification.setStandardButtons(QMessageBox.Ok)

        # Al cerrar el cuadro de diálogo, registrar la pausa
        notification.buttonClicked.connect(lambda: self.resume_timer(message))
        notification.exec_()

    def resume_timer(self, message):
        pause_end_time = QDateTime.currentDateTime()
        pause_duration = (
            pause_end_time.toSecsSinceEpoch() - self.pause_start_time.toSecsSinceEpoch()
        )
        elapsed_time = QTime(0, 0).addSecs(pause_duration).toString("hh:mm:ss")

        self.data_handler.save_activity(elapsed_time, f"Pausa: {message}")

        if self.was_timer_active:
            self.timer.start(1000)
