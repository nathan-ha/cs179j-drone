import threading
import time
import motor as motor
import tracking as tracking
import stepper as stepper

stop_event = threading.Event()
    
t_color = threading.Thread(
    target=tracking.tracking_thread,
    args=(stop_event,)
)

t_motor = threading.Thread(
    target=motor.motor_thread,
    args=(stop_event,)
)

t_stepper = threading.Thread(
    target=stepper.stepper_thread,
    args=(stop_event,)
)

print("Starting target tracking thread...")
t_color.start()
print("Starting motor thread...")
t_motor.start()
print("Starting stepper motor thread...")
t_stepper.start()

try:
    while not stop_event.is_set(): # check stop event every 0.1s
      time.sleep(0.1)
except KeyboardInterrupt:
    print("\n***Keyboard interrupt received. Shutting down...")
finally:
    stop_event.set()
    t_color.join()
    t_motor.join()
    t_stepper.join()
    print("All threads stopped.")
