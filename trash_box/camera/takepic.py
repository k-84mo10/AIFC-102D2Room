# -*- coding: utf-8 -*-

import cv2

def capture_image(i):
    # カメラを起動
    cap = cv2.VideoCapture(0)  # 0は内蔵カメラを表します。複数のカメラが接続されている場合は、1、2、3などを試してください。

    # カメラが正しく起動されたかを確認
    if not cap.isOpened():
        print("Unable to access camera")
        return

    # カメラから画像を取得
    ret, frame = cap.read()

    # 画像の取得が成功したかを確認
    if not ret:
        print("Failed to capture image")
        return

    # 画像を保存するファイル名を指定
    filename = "photo/captured_image_{}.jpg".format(i)

    # 画像を保存
    cv2.imwrite(filename, frame)

    print("Image saved as:", filename)

    # カメラを解放
    cap.release()

if __name__ == "__main__":
    input("Press Enter to capture image from webcam...")
    capture_image(1)
