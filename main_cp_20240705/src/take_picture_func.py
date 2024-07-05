# src/take_picture_func.py
from main_cp_20240705.lib import Camera
from main_cp_20240705.src import get_time

def take_picture_function(camera: Camera, lock) -> None:
    """
    Takes a picture at regular intervals.

    Args:
        camera (Camera): The camera object.
    """
    while True:
        timestamp = get_time()
        camera.capture_image(timestamp, 95)
        with open(f"main_cp_20240705/data/csv/{start_time}/take_image_time.csv", "a") as file:
            file.write(f"{timestamp}\n")         

        if is_manual:
            state = state_from_serial
            if state != "":
                source_picture_name = (
                    f"main_cp_20240705/data/image/raw/{start_time}/{timestamp}.jpg"
                )
                copied_picture_name = f"main_cp_20240705/data/image/train/{start_time}/{timestamp}_{state}.jpg"
                shutil.copy(source_picture_name, copied_picture_name)
