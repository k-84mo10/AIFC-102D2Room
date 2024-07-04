import serial
import re


class SerialCommunication:
    """Class for serial communication to obtain and record status."""

    def __init__(self, port: str, baudrate: int, start_time: int) -> None:
        """Initializes serial communication parameters and file paths.

        Args:
            port (str): The serial port to use.
            baudrate (int): The baud rate for serial communication.
            start_time (str): The start time to generate file paths.
        """
        self.port = port
        self.baudrate = baudrate
        self.readfile = f"main_cp_20240702/data/csv/{start_time}/read_state.csv"
        self.writefile = f"main_cp_20240702/data/csv/{start_time}/write_state.csv"

    def start(self):
        """Starts serial communication."""
        self.ser = serial.Serial(self.port, self.baudrate)

    def read_serial(self):
        """Reads data from the serial port.

        Returns:
            str: The read data if available.
        """
        if self.ser.in_waiting > 0:
            read_data = self.ser.readline().decode().strip()
            return read_data

    def record_read_state(self, read_data):
        """Records the read data to a file if it matches the valid format.

        Args:
            read_data (str): The data read from the serial port.
        """
        if self.is_valid_format(read_data):
            with open(self.readfile, "a") as file:
                file.write(read_data + "\n")

    def is_valid_format(self, read_data):
        """Checks if the read data has a valid format.

        Args:
            read_data (str): The data to check.

        Returns:
            bool: True if the format is valid, False otherwise.
        """
        pattern = r"^S\d{7}"
        return re.match(pattern, str(read_data)) is not None

    def get_state(self):
        """Gets the latest state from the recorded read data.

        Returns:
            str: The latest state.
        """
        with open(self.readfile, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                latest_line = lines[-1].strip()
                state = latest_line[1:5]
            else:
                state = "----"
        return state

    def is_manual(self):
        """Checks if the latest state is manual or automatic.

        Returns:
            bool: True if the state is manual, False otherwise.
        """
        with open(self.readfile, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                latest_line = lines[-1].strip()
                return latest_line[5] == "0"
            return False

    def record_write_state(self, write_data: str) -> None:
        """Records the inferred data to a write file.

        Args:
            write_data (str): The data to write.
        """
        with open(self.writefile, "a") as file:
            file.write(write_data + "\n")

    def write_serial(self):
        """Writes the latest inferred data to the serial port."""
        with open(self.writefile, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                latest_line = lines[-1].strip()
                self.ser.write(("C" + latest_line + "0").encode() + b"\r\n")

    def stop(self):
        """Stops serial communication."""
        self.ser.close()
