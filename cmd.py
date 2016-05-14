import serial
import sys

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115280, timeout=1)
    
def sendCommand(cmd):
    ser.write(cmd)
    return ser.read(512) # It's overkill, but we really want everything

sendCommand(sys.argv[1])
