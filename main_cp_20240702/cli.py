from main_cp_20240702 import SerialCommunication, TakeImage, MachineLearning
import configparser
import os
import threading
import ast
from datetime import datetime


def get_time():
    """Gets the current time formatted as a string.

    Returns:
        str: The current time formatted as 'YYYYMMDDTHHMMSS'.
    """
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%dT%H%M%S")
    return formatted_now


def read_serial(serial_communication):
    """Reads data from the serial communication.

    Args:
        serial_communication (SerialCommunication): The serial communication instance.
    """
    while True:
        read_data = serial_communication.read()
        if read_data:
            serial_communication.record_read_state(read_data)


def take_picture(take_image, serial_communication):
    """Captures and saves images periodically.

    Args:
        take_image (TakeImage): The instance to capture images.
        serial_communication (SerialCommunication): The serial communication instance.
    """
    while True:
        timestamp = get_time()
        take_image.capture_image(timestamp, 95)

        if serial_communication.is_manual():
            state = serial_communication.get_state()
            if state != "----":
                take_image.copy_image_to_other_directory(timestamp, state, "train")


def inference(machine_learning, state_list, take_image, start_time):
    """Performs inference on the latest captured image.

    Args:
        machine_learning (MachineLearning): The machine learning instance.
        state_list (list): The list of possible states.
        take_image (TakeImage): The instance to capture images.
        start_time (str): The start time used to generate file paths.
    """
    while True:
        latest_image_time = take_image.get_image_time()

        if latest_image_time:
            image_path = (
                f"main_cp_20240702/data/image/raw/{start_time}/{latest_image_time}.jpg"
            )
            try:
                state = state_list[machine_learning.inference(image_path)]
                take_image.copy_image_to_other_directory(
                    latest_image_time, state, "result"
                )
                with open(
                    f"main_cp_20240702/data/csv/{start_time}/write_state.csv", "a"
                ) as file:
                    file.write(state + "\n")
            except OSError:
                pass


def write_serial(serial_communication):
    """Writes data to the serial communication periodically.

    Args:
        serial_communication (SerialCommunication): The serial communication instance.
    """
    previous_time = get_time()
    while True:
        current_time = get_time()
        if current_time != previous_time:
            serial_communication.write()
            previous_time = current_time


def main():
    """Main function to initialize and start the threads."""
    config_path = os.path.join(os.path.dirname(__file__), "configs", "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)

    camera_id = config.getint("device", "camera_id")
    serial_port = config.get("serial", "serial_port")
    serial_baudrate = config.getint("serial", "serial_baudrate")
    model_path = config.get("machine_learning", "model_path")
    model_type = config.get("machine_learning", "model_type")
    state_list = ast.literal_eval(config.get("machine_learning", "state_list"))

    start_time = get_time()

    os.makedirs(f"main_cp_20240702/data/image/raw/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240702/data/image/train/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240702/data/image/result/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240702/data/csv/{start_time}", exist_ok=True)

    with open(f"main_cp_20240702/data/csv/{start_time}/read_state.csv", "w"):
        pass
    with open(f"main_cp_20240702/data/csv/{start_time}/write_state.csv", "w"):
        pass
    with open(f"main_cp_20240702/data/csv/{start_time}/image_time.csv", "w"):
        pass

    serial_communication = SerialCommunication(serial_port, serial_baudrate, start_time)
    take_image = TakeImage(start_time, camera_id)
    machine_learning = MachineLearning(model_path, model_type)

    serial_communication.start()

    read_serial_thread = threading.Thread(
        target=read_serial, args=(serial_communication,)
    )
    read_serial_thread.daemon = True
    read_serial_thread.start()

    take_picture_thread = threading.Thread(
        target=take_picture, args=(take_image, serial_communication)
    )
    take_picture_thread.daemon = True
    take_picture_thread.start()

    inference_thread = threading.Thread(
        target=inference,
        args=(machine_learning, state_list, take_image, start_time),
    )
    inference_thread.daemon = True
    inference_thread.start()

    write_serial_thread = threading.Thread(
        target=write_serial, args=(serial_communication,)
    )
    write_serial_thread.daemon = True
    write_serial_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        take_image.release()
        serial_communication.stop()
        print("Exiting main thread")
