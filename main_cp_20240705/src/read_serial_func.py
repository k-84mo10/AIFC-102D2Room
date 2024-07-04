# src/read_serial_func.py


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
            state_from_serial = read_data[1:5]
            is_manual = read_data[5] == "0"
