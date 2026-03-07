import threading
import time
import src.motor as motor
import src.tracking as tracking

stop_event = threading.Event()

t_color = threading.Thread(
    target=tracking.tracking_thread,
    args=(stop_event,)
)

t_motor = threading.Thread(
    target=motor.motor_thread,
    args=(stop_event,)
)

t_color.start()
t_motor.start()

try:
    while not stop_event.is_set(): # check stop event every 0.1s
      time.sleep(0.1)
except KeyboardInterrupt:
    print("***Keyboard interrupt received. Shutting down...")
finally:
    stop_event.set()
    t_color.join()
    t_motor.join()
    print("All threads stopped.")