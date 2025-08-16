from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox, QPushButton
from PySide6.QtCore import Signal

class ModbusControls(QWidget):
    log_signal = Signal(str)

    def __init__(self, modbus_manager):
        super().__init__()
        self.modbus_manager = modbus_manager
        layout = QHBoxLayout()

        self.unit_id = QSpinBox(); self.unit_id.setRange(1, 247)
        self.address = QSpinBox(); self.address.setRange(0, 9999)
        self.count = QSpinBox(); self.count.setRange(1, 125)
        self.value = QSpinBox(); self.value.setRange(0, 65535)

        self.read_btn = QPushButton("Read Registers")
        self.write_btn = QPushButton("Write Register")

        self.read_btn.clicked.connect(self.read_registers)
        self.write_btn.clicked.connect(self.write_register)

        layout.addWidget(QLabel("Unit:")); layout.addWidget(self.unit_id)
        layout.addWidget(QLabel("Addr:")); layout.addWidget(self.address)
        layout.addWidget(QLabel("Count:")); layout.addWidget(self.count)
        layout.addWidget(QLabel("Value:")); layout.addWidget(self.value)
        layout.addWidget(self.read_btn)
        layout.addWidget(self.write_btn)

        self.setLayout(layout)

    def read_registers(self):
        regs = self.modbus_manager.read_holding_registers(self.unit_id.value(), self.address.value(), self.count.value())
        if regs is not None:
            self.log_signal.emit(f"[MODBUS RSP] {regs}")
        else:
            self.log_signal.emit("[MODBUS ERR] Failed to read")

    def write_register(self):
        ok = self.modbus_manager.write_single_register(self.unit_id.value(), self.address.value(), self.value.value())
        self.log_signal.emit("Write OK" if ok else "Write Failed")