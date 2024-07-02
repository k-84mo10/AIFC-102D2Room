from main_cp_20240702 import SerialCommunication, TakeImage, MachineLearning
import configparser
import os
import re
import threading
import ast
from datetime import datetime


# 現在時刻の取得
def get_time():
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%dT%H%M%S")
    return formatted_now


# シリアル通信を読むスレッド
def read_serial(serial_communication):
    while True:
        read_data = serial_communication.read()
        if read_data:
            serial_communication.record_read_state(read_data)


# 画像を撮るスレッド
def take_picture(take_image, serial_communication):
    while True:
        timestamp = get_time()
        take_image.capture_image(timestamp, 95)
        if serial_communication.is_manual():
            state = serial_communication.get_state()
            if state != "----":
                take_image.copy_image_to_other_directory(timestamp, state, "train")


# 推論するスレッド
def inference(machine_learning, state_list, take_image, serial_communication, start_time):
    while True:
        files = os.scandir("main_cp_20240702/data/image/raw/{}".format(start_time))
        if files:
            last_file = max(files, key=lambda entry: entry.stat().st_mtime)
            image_path = last_file.path
            state = state_list[machine_learning.inference(image_path)]
            pattern = r"(\d{8}T\d{6})"
            match = re.search(pattern, image_path)
            if match:
                timestamp = match.group(1)
            take_image.copy_image_to_other_directory(timestamp, state, "result")
            serial_communication.write_state(state)


# シリアル通信を送るスレッド
def write_serial(serial_communication):
    previous_time = get_time()
    while True:
        current_time = get_time()
        if current_time != previous_time:
            serial_communication.write()
            previous_time = current_time


def main():
    """
    メインの処理
    """

    config_path = os.path.join(os.path.dirname(__file__), "configs", "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)

    camera_id = config.getint("device", "camera_id")
    serial_port = config.get("serial", "serial_port")
    sereal_baudrate = config.getint("serial", "serial_baudrate")
    model_path = config.get("machine_learning", "model_path")
    model_type = config.get("machine_learning", "model_type")
    state_list = ast.literal_eval(config.get("machine_learning", "state_list"))

    # 現在時刻の取得
    start_time = get_time()

    # ディレクトリ・ファイルの作成
    os.makedirs("main_cp_20240702/data/image/raw/{}".format(start_time), exist_ok=True)
    os.makedirs(
        "main_cp_20240702/data/image/train/{}".format(start_time), exist_ok=True
    )
    os.makedirs(
        "main_cp_20240702/data/image/result/{}".format(start_time), exist_ok=True
    )
    os.makedirs("main_cp_20240702/data/csv/{}".format(start_time), exist_ok=True)
    with open(
        "main_cp_20240702/data/csv/{}/read_state.csv".format(start_time), "w"
    ) as file:
        pass
    with open(
        "main_cp_20240702/data/csv/{}/write_state.csv".format(start_time), "w"
    ) as file:
        pass

    # クラスのインスタンス化
    serial_communication = SerialCommunication(serial_port, sereal_baudrate, start_time)
    take_image = TakeImage(start_time, camera_id)
    machine_learning = MachineLearning(model_path, model_type)

    # シリアル通信の開始
    serial_communication.start()

    # シリアル通信を読むスレッドの起動
    read_serial_thread = threading.Thread(
        target=read_serial, args=(serial_communication,)
    )
    read_serial_thread.daemon = True
    read_serial_thread.start()

    # 画像を撮るスレッド
    take_picture_thread = threading.Thread(
        target=take_picture, args=(take_image, serial_communication)
    )
    take_picture_thread.daemon = True
    take_picture_thread.start()

    # 推論するスレッド
    # inference_thread = threading.Thread(
    #     target=inference,
    #     args=(machine_learning, state_list, take_image, serial_communication, start_time),
    # )
    # inference_thread.daemon = True
    # inference_thread.start()

    # シリアル通信を送るスレッドの起動
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
