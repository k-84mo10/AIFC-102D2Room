import cv2

class Camera:
    """
    カメラを操作するためのクラス
    """
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Unable to access camera")

    def capture_train_image(self, timestamp, quality):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture image")
            return
        filename = "train/{}.jpg".format(timestamp)
        cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    
    def capture_test_image(self, timestamp, quality):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture image")
            return
        filename = "test/{}.jpg".format(timestamp)  
        cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])

    def release(self):
        self.cap.release()