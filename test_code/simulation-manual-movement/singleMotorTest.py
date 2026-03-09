from pymavlink import mavutil
import time

# Connection string (adjust as needed)
master = mavutil.mavlink_connection('/dev/ttyACM0')

# Wait for heartbeat
master.wait_heartbeat()
print("Connected to system:", master.target_system)

motor_number = 1
throttle = 10      # percent
duration = 1       # seconds

def spin_motor(motor, throttle_percent, seconds):
    throttle = throttle_percent / 100.0

    # Build actuator values, -1 means "leave unchanged"
    actuators = [-1, -1, -1, -1, -1, -1]
    actuators[motor - 1] = throttle  # motor is 1-indexed

    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_ACTUATOR,
        0,
        *actuators
    )

    time.sleep(seconds)

    # Stop the motor
    actuators[motor - 1] = 0.0
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_ACTUATOR,
        0,
        *actuators
    )

try:
    print(f"Spinning motor {motor_number} at {throttle}%")

    spin_motor(motor_number, throttle, duration)

    start = time.time()
    while time.time() - start < duration:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nKeyboard interrupt received. Stopping motor.")

finally:
    # Send stop command (0 throttle)
    spin_motor(motor_number, 0, 1)
    print("Motor stopped. Exiting safely.")