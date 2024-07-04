# lib/camera.py

import cv2


class Camera:
    def __init__(self, camera_id: int, start_time: str) -> None:
        """
        Initializes the camera with the specified camera ID.

        Args:
            camera_id (int): The ID of the camera to use.
        """
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise ValueError("Unable to access camera")
        self.start_time = start_time

    def capture_image(self, timestamp: str, quality: int) -> None:
        """
        Captures and saves an image.

        Args:
            timestamp (str): The timestamp to use in the filename.
            quality (int): The quality of the saved image.
        """
        ret, frame = self.cap.read()
        if not ret:
            return

        filename = f"main_cp_20240703/data/image/raw/{self.start_time}/{timestamp}.jpg"
        cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])

    def release(self) -> None:
        """
        Releases the camera.
        """
        self.cap.release()
