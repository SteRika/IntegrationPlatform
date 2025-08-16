import serial
import serial.tools.list_ports

class SerialManager:
    def __init__(self):
        self.ser = None

    def list_available_ports(self):
        """Return a list of available COM ports on the system."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port, baudrate=9600, timeout=1):
        """Connect to the specified serial port."""
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {port}: {e}")
            return False

    def disconnect(self):
        """Close the serial connection."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            return True

    def send_data(self, data):
        """Send data to the connected serial device."""
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode())
