# src/write_serial_func.py
from main_cp_20240705.lib import SerialCommunication, FileManage
from main_cp_20240705.src import get_time
from datetime import datetime, timedelta

def write_serial_function(
    serial_communication: SerialCommunication, write_serial_file: FileManage
) -> None:
    """
    Writes the state to the serial port.

    Args:
        serial_communication (SerialCommunication): The serial communication object.
    """
    last_state_changed_time = None
    previous_state = "0000"

    while True:
        current_time = datetime.now()

        if last_state_changed_time is not None:
            elapsed_time = current_time - last_state_changed_time
            if elapsed_time < timedelta(seconds=5):
                continue

        state = write_serial_file.read_last_line()
        if previous_state != state:
            last_state_changed_time = current_time
            previous_state = state

        serial_communication.write_serial("C" + state + "0")
