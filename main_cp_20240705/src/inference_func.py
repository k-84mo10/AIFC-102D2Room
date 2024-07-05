# src/inference.py
from main_cp_20240705.lib import MachineLearning

def inference_function(
    machine_learning: MachineLearning, start_time: str, state_list: list, lock
) -> None:
    """
    Infers the state of the object in the image.

    Args:
        machine_learning (MachineLearning): The machine learning object.
    """
    while True:
        with open(f"main_cp_20240705/data/csv/{start_time}/take_image_time.csv", "r") as file:
            lines = file.readlines()
            latest_line = lines[-1].strip() if lines else ""

        nowest_image_time = latest_line
        if nowest_image_time != "":
            image_path = (
                f"main_cp_20240705/data/image/raw/{start_time}/{nowest_image_time}.jpg"
            )
            state_value = machine_learning.inference(image_path)
            inference_state = state_list[state_value]
            if inference_state != "":
                source_picture_name = f"main_cp_20240705/data/image/result/{start_time}/{nowest_image_time}.jpg"
                copied_picture_name = f"main_cp_20240705/data/image/train/{start_time}/{nowest_image_time}_{inference_state}.jpg"
                shutil.copy(source_picture_name, copied_picture_name)

                with open(f"main_cp_20240705/data/csv/{start_time}/write_serial.csv", "a") as file:
                    file.write(f"{inference_state}\n")
