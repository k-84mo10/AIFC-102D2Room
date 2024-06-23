import threading
import os
from datetime import datetime

from pythonlibs.camera import Camera
from pythonlibs.photonamemanage import PhotoNameManeger
from pythonlibs.serialcommunication import SerialCommunication
from pythonlibs.readstatemanagement import ReadStateManagement
from pythonlibs.writestatemanagement import WriteStateManagement
from pythonlibs.machinelearning import MachineLearning
        
class Main:
    def __init__(self):
        self.serial_communication = SerialCommunication('/dev/ttyACM0', 9600)
        self.read_state_management = ReadStateManagement()
        self.write_state_management = WriteStateManagement()
        self.camera = Camera()
        self.machine_learning = MachineLearning()

        self.serial_communication.start()
        self.delete_all_files_in_directory("train")
        self.delete_all_files_in_directory("test")

    def get_time(self):
        now = datetime.now()
        formatted_now = now.strftime('%Y%m%dT%H%M%S')
        return formatted_now

    def is_10second(self, timestamp):
        seconds = int(timestamp[-2:])
        if seconds % 10 == 0:
            return True
        else:
            return False

    def delete_all_files_in_directory(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    def state_acquire(self):
        try:
            while True:
                data = self.serial_communication.read()
                self.read_state_management.record_state(data)
        except KeyboardInterrupt:
            print("Exiting state acquisition")
    
    def take_picture(self):
        try:
            while True:
                timestamp = self.get_time()
                if self.read_state_management.is_manual():
                   self.camera.capture_train_image(timestamp, 95) 
                   self.photo_name_maneger = PhotoNameManeger(timestamp)
                   self.photo_name_maneger.change_photoname(self.read_state_management.get_state())
                else:
                    if self.is_10second(timestamp):
                        self.delete_all_files_in_directory("test")
                        self.camera.capture_test_image(timestamp, 95)                   
        except KeyboardInterrupt:
            print("Exiting take picture")

    def test_picture(self):
        try:
            while True:
                if self.read_state_management.is_manual() == False:
                    latest_image_path = self.machine_learning.get_latest_image_path()
                    if latest_image_path != -1:
                        tmp_state = self.machine_learning.test_image(latest_image_path)
                        if tmp_state != -1:
                            self.write_state_management.write_state(tmp_state)
        except KeyboardInterrupt:
            print("Exiting train")

    def send_state(self):
        try:
            pasttimestamp = self.get_time()
            while True:
                timestamp = self.get_time()
                state = self.write_state_management.get_state()
                if state != -1 and timestamp != pasttimestamp:
                    self.serial_communication.write(state)
                    print(state)
                pasttimestamp = timestamp 
        except KeyboardInterrupt:
            print("Exiting send state")

    def run(self):
        read_serial_thread = threading.Thread(target=self.state_acquire)
        read_serial_thread.daemon = True
        read_serial_thread.start()

        take_picture_thread = threading.Thread(target=self.take_picture)
        take_picture_thread.daemon = True
        take_picture_thread.start()

        send_serial_thread = threading.Thread(target=self.send_state)
        send_serial_thread.daemon = True
        send_serial_thread.start()

        test_picture_thread = threading.Thread(target=self.test_picture)
        test_picture_thread.daemon = True
        test_picture_thread.start()
        
        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.camera.release()
            self.serial_communication.stop()
            print("Exiting main thread")

if __name__ == '__main__':
    main = Main()
    main.run()
