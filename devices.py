import RPi.GPIO as GPIO

# devices.py holds the functions that control the different devices
# that operate the hydroponics system

# The pump function takes in an operation and controls the function
# of the pump accordingly. Valid operations are: on, off, status.
# printout == 1 makes the function print the status on when it turns
# on or off.
def pump(operation, printout):
    PUMP = 8 # Orange Cable - IN 1
    GPIO.setup(PUMP, GPIO.OUT)
    if operation == 'on':
        GPIO.output(PUMP, GPIO.HIGH)
        if printout == 1:
            print ("Pump is on.")
    elif operation == 'off':
        GPIO.output(PUMP, GPIO.LOW)
        if printout == 1:
            print ("Pump is off.")
    elif operation == 'status':
        status = GPIO.input(PUMP)
        if status == 1:
            print ("Pump is on.")
        else:
            print ("Pump is off.")
        return status
    
# The light function takes in an operation and controls the function
# of the light accordingly. Valid operations are: on, off, status.
# printout == 1 makes the function print the status on when it turns
# on or off.
def light(operation, printout):
    LIGHT = 10 # White Cable - IN 2
    GPIO.setup(LIGHT, GPIO.OUT)
    if operation == 'on':
        GPIO.output(LIGHT, GPIO.HIGH)
        if printout == 1:
            print ("Light is on.")
    elif operation == 'off':
        GPIO.output(LIGHT, GPIO.LOW)
        if printout == 1:
            print ("Light is off.")
    elif operation == 'status':
        status = GPIO.input(LIGHT)
        if status == 1:
            print ("Light is on.")
        else:
            print ("Light is off.")
        return status
# The level functions returns 1 if the water level is high enough
# and 0 in case it is not.
def level():
    LEVEL = 12 # Black Cable
    GPIO.setup(LEVEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    status = GPIO.input(LEVEL)
    return status
