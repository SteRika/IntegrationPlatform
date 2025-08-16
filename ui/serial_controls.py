from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
from PySide6.QtCore import Signal
import serial.tools.list_ports

class SerialControls(QWidget):
    log_signal = Signal(str)

    def __init__(self, serial_manager):
        super().__init__()
        self.serial_manager = serial_manager
        layout = QHBoxLayout()

        self.port_combo = QComboBox()
        self.refresh_ports()
        self.baud_combo = QComboBox()
        for b in [9600, 19200, 38400, 57600, 115200]:
            self.baud_combo.addItem(str(b))

        self.connect_btn = QPushButton("Connect")
        self.disconnect_btn = QPushButton("Disconnect")

        self.connect_btn.clicked.connect(self.connect_serial)
        self.disconnect_btn.clicked.connect(self.disconnect_serial)

        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_combo)
        layout.addWidget(QLabel("Baud:"))
        layout.addWidget(self.baud_combo)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.disconnect_btn)
        self.setLayout(layout)

    def refresh_ports(self):
        self.port_combo.clear()
        for port in serial.tools.list_ports.comports():
            self.port_combo.addItem(port.device)

    def connect_serial(self):
        port = self.port_combo.currentText()
        baud = int(self.baud_combo.currentText())
        if self.serial_manager.connect(port, baud):
            self.log_signal.emit(f"Connected to {port} @ {baud}")
        else:
            QMessageBox.critical(self, "Error", "Failed to connect to serial port")

    def disconnect_serial(self):
        self.serial_manager.disconnect()
        self.log_signal.emit("Serial disconnected")