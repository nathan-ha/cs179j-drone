from pymavlink import mavutil
import time

# Connection string (adjust as needed)
master = mavutil.mavlink_connection('/dev/ttyACM0')

# Wait for heartbeat
master.wait_heartbeat()
print("Connected to system:", master.target_system)

motor_number = [1, 2, 3, 4]
throttle1 = 80.0      # percent
throttle2 = 0.0
duration = 5.0       # seconds

def spin_motor(motor, throttle_percent, seconds):
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_MOTOR_TEST,
        0,
        motor,      # param1: motor instance
        0,          # param2: throttle type (0 = percent)
        throttle_percent,
        seconds,
        0, 0, 0
    )

try:
    for i in [0, 1]:
        print(f"Spinning motor {motor_number[i]} at {throttle1}%")
        spin_motor(motor_number[i], throttle1, duration)

    for i in [2, 3]:
        print(f"Spinning motor {motor_number[i]} at {throttle2}%")
        spin_motor(motor_number[i], throttle2, duration)

    start = time.time()
    while time.time() - start < duration:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nKeyboard interrupt received. Stopping motor.")

finally:
    # Send stop command (0 throttle)
    spin_motor(motor_number, 0, 1)
    print("Motor stopped. Exiting safely.")
