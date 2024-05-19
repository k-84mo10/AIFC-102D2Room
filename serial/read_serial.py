import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

try:
    while True:
        line = ser.readline().decode().strip()
        print("Received.", line)

except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed")