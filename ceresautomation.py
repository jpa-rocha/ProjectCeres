import RPi.GPIO as GPIO
from datetime import datetime
import devices as dev
# ceresautomation.py is turned into the ceresautomation executable and will
# be in charge of automating the pump according to water level and the light
# according to time.

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

toggleCheck = True

while True:
    if dev.level() == 0:
        if toggleCheck:
            dev.pump('off', 0)
            toggleCheck =  not toggleCheck
    else:
        if not toggleCheck:
            dev.pump('on', 0)
            toggleCheck = not toggleCheck
        
    time = datetime.now()
    timestring = time.strftime("%H:%M:%S")
    if timestring == "18:00:00":
        dev.light('off', 0)
    if timestring == "06:00:00":
        dev.light('on', 0)
