# src/take_picture_func.py
from main_cp_20240705.lib import Camera, FileManage
from main_cp_20240705.src import get_time
import shutil


def take_picture_function(
    camera: Camera,
    read_serial_file: FileManage,
    take_image_time_file: FileManage,
    start_time: str,
) -> None:
    """
    Takes a picture at regular intervals.

    Args:
        camera (Camera): The camera object.
    """
    while True:
        timestamp = get_time()
        camera.capture_image(timestamp, 95)
        take_image_time_file.write_file(timestamp)

        state = read_serial_file.read_last_line()
        is_manual = state[5] == "0"
        if is_manual:
            source_picture_name = (
                f"main_cp_20240705/data/image/raw/{start_time}/{timestamp}.jpg"
            )
            copied_picture_name = f"main_cp_20240705/data/image/train/{start_time}/{timestamp}_{state[1:5]}.jpg"
            shutil.copy(source_picture_name, copied_picture_name)
