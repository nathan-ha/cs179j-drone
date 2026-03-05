from pymavlink import mavutil
import time

# 1. Connection
connection = mavutil.mavlink_connection('/dev/ttyACM0', baud=115200)
connection.wait_heartbeat()
print("Connected to Vehicle!")

def set_mode(mode):
    if mode not in connection.mode_mapping():
        print(f"Unknown mode : {mode}")
        return
    mode_id = connection.mode_mapping()[mode]
    connection.mav.set_mode_send(
        connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)

def arm():
    connection.mav.command_long_send(
        connection.target_system, connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    print("Arming...")

def move_body(vx, vy, vz, yaw_rate=0):
    """
    Moves relative to the front of the drone (Body Frame).
    vx: m/s forward(+) / back(-)
    vy: m/s right(+) / left(-)
    vz: m/s down(+) / up(-)
    yaw_rate: degrees/sec clockwise(+)
    """
    connection.mav.set_position_target_local_ned_send(
        0, connection.target_system, connection.target_component,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 
        0b0000011111000111, # Ignore pos, acc; use vel + yaw rate
        0, 0, 0,            # Position (ignored)
        vx, vy, vz,         # Velocity in m/s
        0, 0, 0,            # Acceleration (ignored)
        0, yaw_rate)        # Yaw rate

# --- EXECUTION FLOW ---

# Switch to GUIDED_NOGPS
set_mode('GUIDED_NOGPS')
time.sleep(1)
arm()

# Simple Takeoff Simulation (Velocity Up)
print("Taking off (increasing altitude)...")
for _ in range(10):
    move_body(0, 0, -0.5) # Move UP at 0.5m/s
    time.sleep(0.5)

# Hover (Zero velocity)
print("Hovering...")
for _ in range(10):
    move_body(0, 0, 0) 
    time.sleep(0.5)

# Move Forward
print("Moving Forward...")
for _ in range(6):
    move_body(0.5, 0, 0) # 0.5 m/s forward
    time.sleep(0.5)

# Rotate 45 degrees/sec
print("Rotating...")
for _ in range(10):
    move_body(0, 0, 0, yaw_rate=45)
    time.sleep(0.2)

print("Landing Sequence...")
set_mode('LAND')
