#!/usr/bin/env python3
import serial
import time
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    time.sleep(5)
    while True:
	print(" ")
        ser.write(b"a")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
	ser.write(b"b")
	line = ser.readline().decode('utf-8').rstrip()
        print(line)
	ser.write(b"c")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
	ser.write(b"d")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(10)

#import serial
#import time
# 
#s = serial.Serial('/dev/ttyUSB0', 9600) # Namen ggf. anpassen
#s.isOpen()
#time.sleep(5) # der Arduino resettet nach einer Seriellen Verbindung, daher muss kurz gewartet werden
#while True:
#    response = s.readline()
#    print(response)
