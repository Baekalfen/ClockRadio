import time
import datetime
import subprocess
import serial

def wait_until(execute_it_now):
    while True:
        diff = (execute_it_now - datetime.datetime.today()).total_seconds()
        if diff < 30:
            return
        else:
            print "Waiting for %s seconds" % (diff/2)
            time.sleep(diff/2)

        # elif diff <= 1:
        #     time.sleep(0.5)
        # elif diff <= 4:
        #     time.sleep(1)
        # elif diff <= 30:
        #     time.sleep(5)

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115280, timeout=1)
    
def sendCommand(cmd):
    ser.write(cmd)
    return ser.read(512) # It's overkill, but we really want everything


targetTime = 8 # 8 in the morning

while (True):
    t = datetime.datetime.today()
    print "Checking time"
    if t.hour > targetTime and t.minute > 1: 
        t = datetime.datetime(t.year, t.month, t.day+1, targetTime)
        # t = datetime.datetime(2016,2,8,22)
        print "Waiting until %s" % str(t)
        wait_until(t)
    else:
        t = datetime.datetime(t.year,t.month,t.day,targetTime)
        print "Waiting until %s" % str(t)
        wait_until(t)

    print "Checking if stereo is already on"
    if not sendCommand("get_display!") == '' and\
       not sendCommand("get_display!") == '': # Checking twice because it is a bit unstable
        print "Already on, waiting for tommorow"
        continue

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
    print "Turning up in %s seconds" % delay
    time.sleep(delay)
    sendCommand("volume_50!")

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
