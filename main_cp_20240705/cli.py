# cli.py
import ast
import configparser
import os
import threading

from main_cp_20240705 import *


def main():
    """Reads config, sets necessary variables, and starts threads.

    This function performs the following steps:
    1. Reads configuration settings from 'config.ini'.
    2. Sets up necessary directories for storing images and CSV files.
    3. Initializes machine learning, serial communication, and camera modules.
    4. Starts threads for reading serial data, taking pictures, performing inference, and writing serial data.

    Raises:
        KeyboardInterrupt: If the program is interrupted by the user.
    """
    # Load configuration settings
    config_path = os.path.join(os.path.dirname(__file__), "configs", "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)

    # Extract configuration values
    camera_id = config.getint("device", "camera_id")
    serial_port = config.get("serial", "serial_port")
    serial_baudrate = config.getint("serial", "serial_baudrate")
    model_path = config.get("machine_learning", "model_path")
    model_type = config.get("machine_learning", "model_type")
    state_list = ast.literal_eval(config.get("machine_learning", "state_list"))

    # Get the start time for directory naming
    start_time = get_time()

    # Create necessary directories
    os.makedirs(f"main_cp_20240705/data/image/raw/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240705/data/image/train/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240705/data/image/result/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240705/data/csv/{start_time}", exist_ok=True)

    # Initialize file management for CSV files
    take_image_time_file = FileManage(
        f"main_cp_20240705/data/csv/{start_time}/take_image_time.csv"
    )
    read_serial_file = FileManage(
        f"main_cp_20240705/data/csv/{start_time}/read_serial.csv"
    )
    write_serial_file = FileManage(
        f"main_cp_20240705/data/csv/{start_time}/write_serial.csv"
    )

    # Initialize machine learning, serial communication, and camera modules
    machine_learning = MachineLearning(model_path, model_type)
    serial_communication = SerialCommunication(serial_port, serial_baudrate)
    camera = Camera(camera_id, start_time)

    # Start thread for reading serial data
    read_serial_thread = threading.Thread(
        target=read_serial_function,
        args=(serial_communication, read_serial_file),
    )
    read_serial_thread.daemon = True
    read_serial_thread.start()

    # Start thread for taking pictures
    take_picture_thread = threading.Thread(
        target=take_picture_function,
        args=(camera, read_serial_file, take_image_time_file, start_time),
    )
    take_picture_thread.daemon = True
    take_picture_thread.start()

    # Start thread for performing inference
    inference_thread = threading.Thread(
        target=inference_function,
        args=(machine_learning, start_time, state_list, take_image_time_file, write_serial_file, read_serial_file),
    )
    inference_thread.daemon = True
    inference_thread.start()

    # Start thread for writing serial data
    write_serial_thread = threading.Thread(
        target=write_serial_function,
        args=(serial_communication, write_serial_file),
    )
    write_serial_thread.daemon = True
    write_serial_thread.start()

    # Main thread loop to keep the program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        serial_communication.close()
        camera.release()
        print("Exiting main thread")


if __name__ == "__main__":
    main()
