from PyQt5.QtCore import QTimer


class FlashHandler:
    def __init__(self, widget, flash_color="#5b83a7", duration=300, flash_cycles=3):
        self.widget = widget
        self.flash_color = flash_color
        self.duration = duration
        self.flash_cycles = flash_cycles
        self.flash_timer = QTimer()
        self.flash_timer.timeout.connect(self._flash_background)
        self.flash_count = 0
        self.is_flash_on = False

    def start_flash(self):
        """Inicia el parpadeo del fondo."""
        self.flash_count = 0
        self.is_flash_on = False
        self.flash_timer.start(self.duration)

    def _flash_background(self):
        if self.flash_count >= self.flash_cycles * 2:
            self.flash_timer.stop()
            self.widget.setStyleSheet("")
        else:
            if self.is_flash_on:
                self.widget.setStyleSheet("")
            else:
                self.widget.setStyleSheet(f"background-color: {self.flash_color};")

            self.is_flash_on = not self.is_flash_on
            self.flash_count += 1
