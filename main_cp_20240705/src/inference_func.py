# src/inference.py
from main_cp_20240705.lib import MachineLearning, FileManage
import shutil
import os


def inference_function(
    machine_learning: MachineLearning,
    start_time: str,
    state_list: list,
    take_image_time_file: FileManage,
    write_serial_file: FileManage,
    read_serial_file: FileManage,
) -> None:
    """
    Infers the state of the object in the image.

    Args:
        machine_learning (MachineLearning): The machine learning object.
    """
    while True:
        state = read_serial_file.read_last_line()
        if state == "":
            continue

        is_manual = state[5] == "0"
        if is_manual:
            continue

        nowest_image_time = take_image_time_file.read_last_line()
        if nowest_image_time == "":
            continue

        try:
            image_path = (
                f"main_cp_20240705/data/image/raw/{start_time}/{nowest_image_time}.jpg"
            )

            output_list = machine_learning.inference(image_path)

            os.system('cls' if os.name == 'nt' else 'clear')
            print(nowest_image_time)

            max_value = 0
            second_max_value = 0
            max_index = 0
            second_max_index = 0
            print("==========================================")
            for i in range(0, len(output_list)):
                num = output_list[i]
                if i < len(state_list):
                    print(f"{state_list[i]}: {round(num, 2)}")
                if max_value < num:
                    second_max_value = max_value
                    max_value = num
                    max_index = i
                elif second_max_value < num:
                    second_max_value = num 
            print("==========================================")

            if max_value - second_max_value < 2:
                print(f"{state_list[max_index]} and {state_list[second_max_index]} is stalemated !!")
                continue    

            inference_state = state_list[max_index]
            print(f"Current inference state is {inference_state}")

            source_picture_name = (
                f"main_cp_20240705/data/image/raw/{start_time}/{nowest_image_time}.jpg"
            )
            copied_picture_name = f"main_cp_20240705/data/image/result/{start_time}/{nowest_image_time}_{inference_state}.jpg"
            shutil.copy(source_picture_name, copied_picture_name)

            write_serial_file.write_file(inference_state)
        except Exception as e:
            pass
