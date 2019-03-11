import serial

ser = serial.Serial('/dev/ttyS4', 38400, timeout=1)


# distances are printed in millimeters
while 1==1:
    print (ser.readline())
