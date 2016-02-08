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

ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=115280, timeout=3)
    
def sendCommand(cmd):
    ser.write(cmd)
    return ser.read(128)


targetTime = 8 # 8 in the morning

while (True):
    t = datetime.datetime.today()
    print "Checking time"
    if t.hour > targetTime: 
        t += datetime.timedelta(days=1)
        t += datetime.timedelta(hours=-t.hour+targetTime)
        print "Waiting until %s" % str(t)
        wait_until(t)
    else:
        print "Waiting until %s" % str(t)
        wait_until(datetime.datetime(t.year,t.month,t.day,targetTime,0))

    print "Checking if stereo is already on"
    if not sendCommand("get_display!") == '':
        print "Already on, waiting for tommorow"
        continue

    print "Turning stereo on"
    sendCommand("power_on!")

    print "Switching to AUX2"
    sendCommand("aux2!")

    print "Starting radio"
    subprocess.call("mpc play", shell=True)
    subprocess.call("mpc volume 100", shell=True)

    print "Turning off if not in use"
    while (True):
        time.sleep(60*5)
        print "Checking if radio is in use"
        if not sendCommand("get_display!") == '':
            print "Leaving radio on"
        else:
            print "Turning radio off"
            subprocess.call("mpc stop", shell=True)
            break
