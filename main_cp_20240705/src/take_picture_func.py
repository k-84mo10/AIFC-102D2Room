# src/take_picture_func.py


def take_picture_function(camera: Camera) -> None:
    """
    Takes a picture at regular intervals.

    Args:
        camera (Camera): The camera object.
    """
    while True:
        timestamp = get_time()
        camera.capture_image(timestamp, 95)

        if is_manual:
            state = state_from_serial
            if state != "":
                source_picture_name = (
                    f"main_cp_20240705/data/image/raw/{start_time}/{timestamp}.jpg"
                )
                copied_picture_name = f"main_cp_20240705/data/image/train/{start_time}/{timestamp}_{state}.jpg"
                shutil.copy(source_picture_name, copied_picture_name)
