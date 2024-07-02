import serial
import re


class SerialCommunication:
    """
    シリアル通信を行い状況を取得するためのクラス
    """

    def __init__(self, port, baudrate, start_time):
        self.port = port
        self.baudrate = baudrate
        self.readfile = "data/csv/{}/read_state.csv".format(start_time)

    # シリアル通信の開始
    def start(self):
        self.ser = serial.Serial(self.port, self.baudrate)

    # シリアル通信の読み込み
    def read(self):
        if self.ser.in_waiting > 0:
            read_data = self.ser.readline().decode().strip()
            return read_data

    # 読み込んだデータをファイルに保存
    def record_read_state(self, read_data):
        if self.is_valid_format(read_data):
            with open(self.readfile, "a") as file:
                file.write(read_data + "\n")

    # 読み込んだデータのフォーマットが正しいか確認
    def is_valid_format(self, read_data):
        pattern = r"^S\d{7}"
        if re.match(pattern, str(read_data)):
            return True
        else:
            return False

    # 保存されたデータから最新の状態を取得
    def get_state(self):
        with open(self.readfile, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                latest_line = lines[-1].strip()
                state = latest_line[1:5]
            else:
                state = "----"
        return state

    # 保存されたデータから最新の状態が手動か自動かを取得
    def is_manual(self):
        with open(self.readfile, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                latest_line = lines[-1].strip()
                if latest_line[5] == "0":
                    return True
                else:
                    return False
            else:
                return False

    # シリアル通信の書き込み
    def write(self, write_data):
        self.ser.write(("C" + write_data + "0\n").encode() + b"\r\n")

    # シリアル通信の終了
    def stop(self):
        self.ser.close()
