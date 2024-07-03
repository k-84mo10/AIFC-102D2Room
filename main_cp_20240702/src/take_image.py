import cv2
import shutil


class TakeImage:
    """Class to capture and save images."""

    def __init__(self, start_time, camera_id):
        """Initializes the camera and file paths.

        Args:
            start_time (str): The start time to generate file paths.
            camera_id (int): The ID of the camera to use.
        """
        self.cap = cv2.VideoCapture(camera_id)
        self.start_time = start_time
        if not self.cap.isOpened():
            print("Unable to access camera")
            return
        self.image_timefile = f"main_cp_20240702/data/csv/{start_time}/image_time.csv"

    def capture_image(self, timestamp, quality):
        """Captures and saves an image.

        Args:
            timestamp (str): The timestamp to use in the filename.
            quality (int): The quality of the saved image.
        """
        ret, frame = self.cap.read()
        if not ret:
            # print("Failed to capture image")
            return
        filename = f"main_cp_20240702/data/image/raw/{self.start_time}/{timestamp}.jpg"
        cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        with open(self.image_timefile, "a") as file:
            file.write(f"{timestamp}\n")

    def copy_image_to_other_directory(self, timestamp, state, directory_name):
        """Copies the image to another directory with a new name.

        Args:
            timestamp (str): The timestamp to use in the filename.
            state (str): The state to append to the filename.
            directory_name (str): The directory to copy the image to.
        """
        source_picture_name = (
            f"main_cp_20240702/data/image/raw/{self.start_time}/{timestamp}.jpg"
        )
        copied_picture_name = f"main_cp_20240702/data/image/{directory_name}/{self.start_time}/{timestamp}_{state}.jpg"
        shutil.copy(source_picture_name, copied_picture_name)

    def get_image_time(self):
        """Gets the time of the latest captured image.

        Returns:
            str: The timestamp of the latest image.
        """
        with open(self.image_timefile, "r") as file:
            lines = file.readlines()
            latest_line = lines[-1].strip() if lines else ""
        return latest_line

    def release(self):
        """Releases the camera."""
        self.cap.release()
