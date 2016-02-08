import time
import datetime
import subprocess
import serial

def wait_until(execute_it_now):
    while True:
        diff = (execute_it_now - datetime.now()).total_seconds()
        if diff <= 0:
            return
        elif diff <= 0.1:
            time.sleep(0.001)
        elif diff <= 0.5:
            time.sleep(0.01)
        elif diff <= 1.5:
            time.sleep(0.1)
        else:
            time.sleep(1)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115200, timeout=1)

def stereoInUse():
    ser.flushInput()
    ser.write("get_display!")
    text = ser.read(8)
    if text == "display=":
        print "Got display data. Reading input source"
        length = ser.read(3)
        ser.read()

def sendCommands(cmds):
    for cmd in cmds:
        ser.write(cmd)

targetTime = 8 # 8 in the morning

while (True):
    t = datetime.datetime.today()
    if t.hour > targetTime: 
        t += datetime.timedelta(days=1)
        t.hour = 8
        wait_until(t)
    else:
        wait_until(datetime.datetime(t.year,t.month,t.day,targetTime,0))

    print "Turning stereo on"
    print "Switching to AUX2"

    print "Starting radio"
    subprocess.call("mpc play", shell=True)

    print "Turning off if not in use"
    while (True):
        time.sleep(60*5)
        print "Checking if radio is in use"
        inUse = True
        if inUse:
            print "Leaving radio on"
        else:
            print "Turning radio off"
            subprocess.call("mpc stop", shell=True)
