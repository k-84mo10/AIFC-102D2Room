# src/read_serial_func.py
from main_cp_20240705.lib import SerialCommunication
import re

def read_serial_function(serial_communication: SerialCommunication) -> None:
    """
    Reads the serial port and updates the state.

    Args:
        serial_communication (SerialCommunication): The serial communication object.
    """
    while True:
        read_data = serial_communication.read_serial()
        pattern = r"^S\d{7}"
        if re.match(pattern, str(read_data)) is not None:
            with open(f"main_cp_20240705/data/csv/{start_time}/read_serial.csv", "a") as file:
                file.write(f"{read_data[1:6]}\n")            