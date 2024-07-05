# cli.py
from main_cp_20240705 import *
import configparser
import ast
import os
import threading


def main():
    "configを読み込み、必要な変数を設定し、スレッドを開始する"

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

    os.makedirs(f"main_cp_20240705/data/image/raw/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240705/data/image/train/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240705/data/image/result/{start_time}", exist_ok=True)
    os.makedirs(f"main_cp_20240705/data/csv/{start_time}", exist_ok=True)

    take_image_time_file = FileManage(
        f"main_cp_20240705/data/csv/{start_time}/take_image_time.csv"
    )
    read_serial_file = FileManage(
        f"main_cp_20240705/data/csv/{start_time}/read_serial.csv"
    )
    write_serial_file = FileManage(
        f"main_cp_20240705/data/csv/{start_time}/write_serial.csv"
    )

    machine_learning = MachineLearning(
        model_path, model_type, take_image_time_file, write_serial_file
    )
    serial_communication = SerialCommunication(
        serial_port, serial_baudrate, read_serial_file, write_serial_file
    )
    camera = Camera(camera_id, start_time)

    read_serial_thread = threading.Thread(
        target=read_serial_function,
        args=(serial_communication, read_serial_file),
    )
    read_serial_thread.daemon = True
    read_serial_thread.start()

    take_picture_thread = threading.Thread(
        target=take_picture_function,
        args=(
            camera,
            read_serial_file,
            take_image_time_file,
            start_time,
        ),
    )
    take_picture_thread.daemon = True
    take_picture_thread.start()

    inference_thread = threading.Thread(
        target=inference_function,
        args=(
            machine_learning,
            start_time,
            state_list,
            take_image_time_file,
            write_serial_file,
        ),
    )
    inference_thread.daemon = True
    inference_thread.start()

    write_serial_thread = threading.Thread(
        target=write_serial_function,
        args=(serial_communication, write_serial_file),
    )
    write_serial_thread.daemon = True
    write_serial_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        serial_communication.close()
        camera.release()
        print("Exiting main thread")
