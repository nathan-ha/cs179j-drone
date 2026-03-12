import RPi.GPIO as GPIO
import time
import tracking as tracking

STEPPER_PINS = [17, 18, 27, 22] # BCM numbering
#               11, 12, 13, 15  <-- Physical rpi pins

STEP_SEQUENCE = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]

STEP_FULL_ROTATION = 2048

def step_motor(steps, stopFlag, delay=0.0005):
    for i in range(steps):
        if stopFlag.is_set():
            return
        for step in STEP_SEQUENCE:
            for pin, val in zip(STEPPER_PINS, step):
                GPIO.output(pin, val)
            time.sleep(delay)


def stepper_thread(stopFlag):
    isShot = False
    
    GPIO.setmode(GPIO.BCM)
    for pin in STEPPER_PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    while not stopFlag.is_set() and not isShot: 
        if tracking.CV_RESULT == "CENTERED":
            time.sleep(1)
            if tracking.CV_RESULT == "CENTERED":
                print("Activating stepper motor...")
                step_motor(STEP_FULL_ROTATION, stopFlag)
                isShot = True
        else:
            time.sleep(0.1)
    GPIO.cleanup()
