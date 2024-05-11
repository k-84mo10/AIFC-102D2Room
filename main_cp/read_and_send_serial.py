import serial
import threading

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
                print("Received:", data)
    except KeyboardInterrupt:
        print("Exiting read thread")

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

# 読み取りスレッドを開始
read_thread = threading.Thread(target=read_serial)
read_thread.daemon = True
read_thread.start()

# 送信スレッドを開始
send_thread = threading.Thread(target=send_serial)
send_thread.daemon = True
send_thread.start()

# Ctrl+C が押されるまでメインスレッドを続ける
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting main thread")
    ser.close()  # シリアルポートを閉じる
