from PySide6.QtWidgets import QTextEdit, QWidget, QVBoxLayout
import time

class LogPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)
        self.setLayout(layout)

    def add_log(self, message):
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        self.log_view.append(f"[{ts}] {message}")