import os
import evdev
from evdev import InputDevice, categorize, ecodes

device = None
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for d in devices:
    if d.name == "Nintendo Wii Remote":
        device = d
        break

if device is not None:
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            #button A
            if event.code == 304 and event.value == 1:
                os.system("xdotool click 1")

            #button B
            if event.code == 305 and event.value == 1:
                os.system("xdotool click 3")
