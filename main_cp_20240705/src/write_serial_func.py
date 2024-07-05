# src/write_serial_func.py
from main_cp_20240705.lib import SerialCommunication, FileManage


def write_serial_function(
    serial_communication: SerialCommunication, write_serial_file: FileManage
) -> None:
    """
    Writes the state to the serial port.

    Args:
        serial_communication (SerialCommunication): The serial communication object.
    """
    while True:
        state = write_serial_file.read_last_line()
        serial_communication.write_serial(("C" + state + "0").encode() + b"\r\n")
