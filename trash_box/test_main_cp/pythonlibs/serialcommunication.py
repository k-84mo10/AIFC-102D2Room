import serial

class SerialCommunication:
    """
    シリアル通信を行うためのクラス
    """
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate

    def start(self):
        self.ser = serial.Serial(self.port, self.baudrate)

    def read(self):
        if self.ser.in_waiting > 0:
            read_data = self.ser.readline().decode().strip()
            return read_data

    def write(self, data):
        self.ser.write(data.encode() + b'\r\n')

    def stop(self):
        self.ser.close()