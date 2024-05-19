from datetime import datetime
import cv2
import serial
import re

port = '/dev/ttyACM0'
baudrate = 9600
ser = serial.Serial(port, baudrate)

def get_now_time():
    now = datetime.now()
    formatted_now = now.strftime('%Y%m%dT%H%M%S')
    return formatted_now

def capture_image(timestamp, lightstate):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Unable to access camera")
        return
    
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image")
        return
    
    filename = "raw/{}_{}.jpg".format(timestamp, lightstate)
    cv2.imwrite(filename, frame)
    cap.release()

def read_serial():
    if ser.in_waiting > 0:
        # データを読み取り
        data = ser.readline().decode().strip()
        return data

def is_valid_format(data):
    pattern = r'^S\d{7}$'
    if re.match(pattern, str(data)):
        return True
    else:
        return False

if __name__=="__main__":
    try:
        while True:
            state = read_serial()
            if is_valid_format(state) == True:
                timestamp = get_now_time()
                lightstate = state[1:5]
                capture_image(timestamp, lightstate)
    except KeyboardInterrupt:
        print("Exiting read thread")
    