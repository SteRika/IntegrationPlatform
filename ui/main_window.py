from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QTextEdit, QHBoxLayout
)
from core.serial_manager import SerialManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PLC Integration UI")
        self.resize(600, 400)

        # Serial Manager instance
        self.serial_manager = SerialManager()

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # COM Port selection
        port_layout = QHBoxLayout()
        self.port_label = QLabel("Select COM Port:")
        self.port_dropdown = QComboBox()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.populate_ports)

        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_dropdown)
        port_layout.addWidget(self.refresh_button)
        layout.addLayout(port_layout)

        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_serial)
        layout.addWidget(self.connect_button)

        self.connect_button = QPushButton("Disconnect")
        self.connect_button.clicked.connect(self.disconnect_serial)
        layout.addWidget(self.connect_button)

        # Log Viewer
        self.log_viewer = QTextEdit()
        self.log_viewer.setObjectName("logViewer")
        self.log_viewer.setReadOnly(True)
        layout.addWidget(self.log_viewer)

        # Populate ports on startup
        self.populate_ports()

        # Load Stylesheet
        with open("ui/style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def populate_ports(self):
        """Populate COM port dropdown with detected ports."""
        self.port_dropdown.clear()
        ports = self.serial_manager.list_available_ports()
        if ports:
            self.port_dropdown.addItems(ports)
        else:
            self.port_dropdown.addItem("No ports found")

    def connect_serial(self):
        """Attempt to connect to selected serial port."""
        port = self.port_dropdown.currentText()
        if "No ports" in port:
            self.log_viewer.append("No COM port available.")
            return

        if self.serial_manager.connect(port):
            self.log_viewer.append(f"Connected to {port}")
        else:
            self.log_viewer.append(f"Failed to connect to {port}")


    def disconnect_serial(self):
        """Attempt to connect to selected serial port."""
        port = self.port_dropdown.currentText()
        if "No ports" in port:
            self.log_viewer.append("No COM port available.")
            return

        if self.serial_manager.disconnect():
            self.log_viewer.append(f"Port {port} disconnected")
        else:
            self.log_viewer.append(f"Failed to connect to {port}")
