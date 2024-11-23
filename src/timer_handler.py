from PyQt5.QtCore import QTimer, QTime


class TimerHandler:
    def __init__(self, parent, callback_update_label, callback_timer_end):
        self.parent = parent
        self.timer = QTimer(parent)
        self.remaining_time = QTime(0, 0, 0)
        self.initial_time = QTime(0, 0, 0)

        # Conectar señales
        self.timer.timeout.connect(self.update_timer)

        # Callbacks
        self.callback_update_label = callback_update_label
        self.callback_timer_end = callback_timer_end

    def parse_input_time(self, input_time):
        hours, minutes, seconds = 0, 0, 0
        try:
            if ":" in input_time:
                parts = input_time.split(":")
                if len(parts) == 3:
                    hours = int(parts[0]) if parts[0] else 0
                    minutes = int(parts[1]) if parts[1] else 0
                    seconds = int(parts[2]) if parts[2] else 0
                elif len(parts) == 2:
                    minutes = int(parts[0]) if parts[0] else 0
                    seconds = int(parts[1]) if parts[1] else 0
            else:
                total_seconds = int(input_time)
                minutes, seconds = divmod(total_seconds, 60)

            while seconds >= 60:
                minutes += 1
                seconds -= 60
            while minutes >= 60:
                hours += 1
                minutes -= 60
        except ValueError:
            hours, minutes, seconds = 0, 0, 0

        return QTime(hours, minutes, seconds)

    def start_timer(self, input_time):
        self.initial_time = self.parse_input_time(input_time)
        self.remaining_time = self.initial_time
        self.callback_update_label(self.remaining_time)
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def update_timer(self):
        if self.remaining_time <= QTime(0, 0, 1):
            self.stop_timer()
            self.remaining_time = QTime(0, 0, 0)
            self.callback_update_label(self.remaining_time)
            self.callback_timer_end()
        else:
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.callback_update_label(self.remaining_time)

    def add_time(self, input_time):
        additional_time = self.parse_input_time(input_time)
        self.remaining_time = self.remaining_time.addSecs(
            additional_time.hour() * 3600
            + additional_time.minute() * 60
            + additional_time.second()
        )
        self.callback_update_label(self.remaining_time)

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
