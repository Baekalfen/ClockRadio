import time
import datetime
import subprocess
import serial
import sys

def wait_until(execute_it_now):
    while True:
        diff = (execute_it_now - datetime.datetime.today()).total_seconds()
        if diff < 30:
            return
        else:
            sec = datetime.timedelta(seconds=int(diff/2))
            d = datetime.datetime(1,1,1) + sec
            print "Waiting for %d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second)
            time.sleep(diff/2)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115280, timeout=1)
    
def sendCommand(cmd):
    ser.write(cmd)
    return ser.read(512) # It's overkill, but we really want everything


if len(sys.argv)>2:
    targetTime = int(sys.argv[1])
    targetMinute = int(sys.argv[2])
else:
    targetTime = 8 # 8 in the morning


print "Alarm set to", targetTime

while (True):
    t = datetime.datetime.today()
    print "Checking time %s" % str(t)
    if t.hour > targetTime or (t.hour == targetTime and t.minute >= 1+targetMinute):
        t = datetime.datetime(t.year, t.month, t.day+1, targetTime, targetMinute)
        print "Waiting until %s" % str(t)
        wait_until(t)
    else:
        t = datetime.datetime(t.year,t.month,t.day,targetTime, targetMinute)
        print "Waiting until %s" % str(t)
        wait_until(t)

#    print "Checking if stereo is already on"
#    if not sendCommand("get_display!") == '':
#        print "Already on, start over in 10 seconds"
#        time.sleep(10)
#        continue

    print "Turning stereo on"
    sendCommand("power_on!")

    print "Switching to AUX2"
    sendCommand("aux2!")

    print "Turning up the volume"
    sendCommand("volume_45!")

    print "Starting radio"
    subprocess.call("mpc play", shell=True)
    subprocess.call("mpc volume 100", shell=True)

    delay = 60*5
    # print "Turning up in %s seconds" % delay
    # time.sleep(delay)
    # sendCommand("volume_50!")

    print "Turning off if not in use"
    while (True):
        print "Checking in %s seconds if radio is in use" % delay
        time.sleep(delay)
        if not sendCommand("get_display!") == '':
            print "Leaving radio on"
        else:
            print "Turning radio off"
            subprocess.call("mpc stop", shell=True)
            break
