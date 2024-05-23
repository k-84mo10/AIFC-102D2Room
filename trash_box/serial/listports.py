import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)
    print(" device       :", p.device)
    print(" name         :", p.name)
    print(" description  :", p.description)
    print(" hwid         :", p.hwid)
    print(" vid          :", p.vid)
    print(" pid          :", p.pid)
    print(" serial_number:", p.serial_number)
    print(" location     :", p.location)
    print(" manufactuer  :", p.manufacturer)
    print(" product      :", p.product)
    print(" interface    :", p.interface)
    print("")