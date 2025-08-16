from pymodbus.client import ModbusSerialClient
from typing import Optional

class ModbusManager:
    def __init__(self):
        self._client: Optional[ModbusSerialClient] = None

    def connect(self, port: str, baudrate: int, timeout: float = 1.0) -> bool:
        self._client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, timeout=timeout)
        return self._client.connect()

    def disconnect(self):
        if self._client:
            self._client.close()
            self._client = None

    def read_holding_registers(self, unit: int, address: int, count: int):
        if not self._client:
            return None
        rr = self._client.read_holding_registers(address, count, unit=unit)
        return rr.registers if not rr.isError() else None

    def write_single_register(self, unit: int, address: int, value: int):
        if not self._client:
            return False
        wr = self._client.write_register(address, value, unit=unit)
        return not wr.isError()