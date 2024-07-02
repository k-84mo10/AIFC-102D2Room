import cv2
import shutil


class TakeImage:
    """
    写真を撮り画像を保存するためのクラス
    """

    def __init__(self, start_time, camera_id):
        self.cap = cv2.VideoCapture(camera_id)
        self.start_time = start_time
        if not self.cap.isOpened():
            print("Unable to access camera")
            return
        self.image_timefile = "main_cp_20240702/data/csv/{}/image_time.csv".format(
            start_time
        )

    # 画像を撮り保存する
    def capture_image(self, timestamp, quality):
        ret, frame = self.cap.read()
        if not ret:
            # print("Failed to capture image")
            return
        filename = "main_cp_20240702/data/image/raw/{}/{}.jpg".format(
            self.start_time, timestamp
        )
        cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
        with open(self.image_timefile, "a") as file:
            file.write(timestamp + "\n")

    # 画像を別のディレクトリにコピーする
    def copy_image_to_other_directory(self, timestamp, state, directory_name):
        source_picture_name = "main_cp_20240702/data/image/raw/{}/{}.jpg".format(
            self.start_time, timestamp
        )
        copied_picture_name = "main_cp_20240702/data/image/{}/{}/{}_{}.jpg".format(
            directory_name,
            self.start_time,
            timestamp,
            state,
        )
        shutil.copy(source_picture_name, copied_picture_name)

    # 最新の画像が取られた時刻を取得する
    def get_image_time(self):
        with open(self.image_timefile, "r") as file:
            lines = file.readlines()
            if lines:
                latest_line = lines[-1].strip()
            else:
                latest_line = ""
        return latest_line

    # カメラを終了する
    def release(self):
        self.cap.release()
