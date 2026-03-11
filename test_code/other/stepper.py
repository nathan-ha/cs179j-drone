import RPi.GPIO as GPIO
import time

# GPIO pins connected to IN1-IN4 on the stepper driver
pins = [17, 18, 27, 22]
#       11, 12, 13, 15  <-- Physical rpi pins

# Step sequence for 4-phase stepper (full-step)
seq = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1]
]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

def step_motor(steps, delay=0.001):
    """Spin stepper motor a given number of steps"""
    for i in range(steps):
        for step in seq:
            for pin, val in zip(pins, step):
                GPIO.output(pin, val)
            time.sleep(delay)

try:
    print("Rotating stepper motor")
    step_motor(2048)  # one full rotation for 28BYJ-48 stepper
except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    # Turn off all pins
    for pin in pins:
        GPIO.output(pin, 0)
    GPIO.cleanup()
    print("GPIO cleaned up")
