# src/read_serial_func.py
from main_cp_20240705.lib import SerialCommunication, FileManage
import re


def read_serial_function(
    serial_communication: SerialCommunication, read_serial_file: FileManage
) -> None:
    """
    Reads the serial port and updates the state.

    Args:
        serial_communication (SerialCommunication): The serial communication object.
    """
    while True:
        read_data = serial_communication.read_serial()
        pattern = r"^S\d{7}"
        if re.match(pattern, str(read_data)) is not None:
            read_serial_file.write_file(read_data)
