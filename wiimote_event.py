#!/usr/bin/python

import os
import subprocess
import evdev
import time
import threading
import signal
from evdev import InputDevice, categorize, ecodes

device = None
control = threading.Condition()
kill = False

def exit_this(signum, frame):
    global kill
    kill = True


def find_device(cv, kill):
    while not kill:
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for d in devices:
            if d.name == "Nintendo Wii Remote":
                device = d
                break
        time.sleep(1)
        #print(device)
        if device is not None:
            with cv:
                cv.notify_all()
                time.sleep(1)
                cv.wait()


def run_device(cv, kill):
    while not kill:
        if device is not None:
            for event in device.read_loop():
                if event.type == ecodes.EV_KEY:
                    #print(event.code)
                    
                    #button A
                    if event.code == 304 and event.value == 1:
                        subprocess.Popen(["xdotool", "click", "1"])

                    #button B
                    if event.code == 305 and event.value == 1:
                        subprocess.Popen(["xdotool", "click", "3"])
                                
                    #button Home
                    if event.code == 316 and event.value == 1:
                        os.system("killall chromium")
                        subprocess.Popen(["chromium","--start-fullscreen",
                                    "/home/cadu/StreamCenter/welcome.html"])
        else:
            with cv:
                cv.notify_all()
                time.sleep(1)
                cv.wait()


find = threading.Thread(target=find_device, args=(control, kill,))
run  = threading.Thread(target=run_device, args=(control, kill,))
find.start()
run.start()
print("joining threads...")
find.join()
run.join()
print("exiting...")


