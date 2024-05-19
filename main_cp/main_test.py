import serial
import threading
import re
import cv2
from datetime import datetime
from collections import deque

# ポートとボーレートを設定
port = '/dev/ttyACM0'
baudrate = 9600

# シリアルポートをオープン
ser = serial.Serial(port, baudrate)

# データ読み取り用の関数
def read_serial():
    try:
        while True:
            # データが受信されるまで待機
            if ser.in_waiting > 0:
                # データを読み取り
                data = ser.readline().decode().strip()
                # print("Received:", data)
                if is_valid_format(data):
                    with open('state.csv', 'w') as file:
                        file.write(data + '\n')
    except KeyboardInterrupt:
        print("Exiting read thread")

def is_valid_format(data):
    pattern = r'^S\d{7}'
    if re.match(pattern, str(data)):
        return True
    else:
        return False

# データ送信用の関数
def send_serial():
    try:
        while True:
            # ユーザーからの入力を受け取る
            user_input = input("Enter data to send: ")
            # データをシリアルポートに書き込む
            ser.write(user_input.encode() + b'\r\n')
    except KeyboardInterrupt:
        print("Exiting send thread")

# 撮影用の関数
def capture_image(timestamp, state):
    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        print("Unable to access camera")
        return
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        return
    filename = "raw/{}_{}.jpg".format(timestamp, state)
    cv2.imwrite(filename, frame)
    cap.release()

def get_time():
    now = datetime.now()
    formatted_now = now.strftime('%Y%m%dT%H%M%S')
    return formatted_now

def take_picture():
    try:
        while True:
            timestamp = get_time()

            with open('state.csv', 'r', encoding='utf-8') as file:
                lines = file.readlines()
            if lines:
                latest_line = lines[-1].strip()
                state = latest_line[1:5]
                capture_image(timestamp, state)

    except KeyboardInterrupt:
        print("Exiting take picture thread")

with open('state.csv', 'w'):
    pass

# 読み取りスレッドを開始
read_thread = threading.Thread(target=read_serial)
read_thread.daemon = True
read_thread.start()

# 送信スレッドを開始
send_thread = threading.Thread(target=send_serial)
send_thread.daemon = True
send_thread.start()

# 撮影スレッドを開始
camera_thread = threading.Thread(target=take_picture)
camera_thread.daemon = True
camera_thread.start()

# Ctrl+C が押されるまでメインスレッドを続ける
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting main thread")
    ser.close()  # シリアルポートを閉じる
