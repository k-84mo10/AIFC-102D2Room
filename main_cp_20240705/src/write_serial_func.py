# src/write_serial_func.py
from main_cp_20240705.lib import SerialCommunication

def write_serial_function(serial_communication: SerialCommunication) -> None:
    """
    Writes the state to the serial port.

    Args:
        serial_communication (SerialCommunication): The serial communication object.
    """
    while True:
        global state_to_serial
        state = state_to_serial
        serial_communication.write_serial(("C" + state+ "0").encode() + b"\r\n")
