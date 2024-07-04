# src/write_serial_func.py


def write_serial_function(serial_communication: SerialCommunication) -> None:
    """
    Writes the state to the serial port.

    Args:
        serial_communication (SerialCommunication): The serial communication object.
    """
    while True:
        serial_communication.write_serial(state_to_serial)
