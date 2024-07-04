# src/inference.py


def incerence_function(
    machine_learning: MachineLearning, start_time: str, state_list: list
) -> None:
    """
    Infers the state of the object in the image.

    Args:
        machine_learning (MachineLearning): The machine learning object.
    """
    while True:
        image_path = (
            f"main_cp_20240705/data/image/raw/{start_time}/{nowest_image_time}.jpg"
        )
        state_value = machine_learning.inference(image_path)
        state_to_serial = state_list[state_value]
        if state_to_serial != "":
            source_picture_name = f"main_cp_20240705/data/image/result/{start_time}/{nowest_image_time}.jpg"
            copied_picture_name = f"main_cp_20240705/data/image/train/{start_time}/{nowest_image_time}_{state_to_serial}.jpg"
            shutil.copy(source_picture_name, copied_picture_name)
