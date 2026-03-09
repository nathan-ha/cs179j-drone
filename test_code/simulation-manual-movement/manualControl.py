import sys
import select
import termios
import atexit
import time
import threading
from pymavlink import mavutil

MOTOR_NUMBER = [1, 2, 3, 4]
THROTTLE_ON = 80.0      # percent
THROTTLE_OFF = 0.0
THROTTLE_TIME = 0.8     # seconds

# ── Terminal raw mode ────────────────────────────────────────────────────────
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def restore_terminal():
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

atexit.register(restore_terminal)

new_settings = termios.tcgetattr(fd)
new_settings[3] = new_settings[3] & ~(termios.ICANON | termios.ECHO)
termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

def get_key():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None

# ── Shared state ─────────────────────────────────────────────────────────────
current_direction = "NONE"   # "LEFT" | "RIGHT" | "NONE"
stop_flag = threading.Event()

# ── Motor thread ─────────────────────────────────────────────────────────────
def motor_thread():
    master = mavutil.mavlink_connection('/dev/ttyACM0')
    print("Waiting for heartbeat...")
    master.wait_heartbeat()
    print("Connected to system:", master.target_system)

    def spin_motor(motor, throttle_percent, seconds):
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,
            0,
            motor,
            0,              # throttle type: 0 = percent
            throttle_percent,
            seconds,
            0, 0, 0
        )

   
    while not stop_flag.is_set():
        direction = current_direction

        if direction == "RIGHT":
            for i in [0, 1]:
                spin_motor(MOTOR_NUMBER[i], THROTTLE_ON,  THROTTLE_TIME)
            for i in [2, 3]:
                spin_motor(MOTOR_NUMBER[i], THROTTLE_OFF, THROTTLE_TIME)

        elif direction == "LEFT":
            for i in [0, 1]:
                spin_motor(MOTOR_NUMBER[i], THROTTLE_OFF, THROTTLE_TIME)
            for i in [2, 3]:
                spin_motor(MOTOR_NUMBER[i], THROTTLE_ON,  THROTTLE_TIME)

        else:
            for m in MOTOR_NUMBER:
                spin_motor(m, THROTTLE_OFF, THROTTLE_TIME)

        time.sleep(0.1)

    # Safe stop on exit
    for m in MOTOR_NUMBER:
        spin_motor(m, THROTTLE_OFF, THROTTLE_TIME)
    print("All motors stopped.")

# ── Main: keyboard loop ───────────────────────────────────────────────────────
t = threading.Thread(target=motor_thread, daemon=True)
t.start()

print("Hold 'a' = LEFT  |  Hold 'd' = RIGHT  |  Ctrl-C to quit")

try:
    while True:
        key = get_key()

        if key == 'a':
            current_direction = "LEFT"
            print("LEFT ", end='\r')
        elif key == 'd':
            current_direction = "RIGHT"
            print("RIGHT", end='\r')
        else:
            # No key held → stop motors
            current_direction = "NONE"
        print(f"{current_direction}", end='\r')

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    stop_flag.set()
    t.join(timeout=2)
