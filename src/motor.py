from pymavlink import mavutil
import tracking as tracking
import time
MOTOR_NUMBER = [1, 2, 3, 4]
THROTTLE_ON = 70.0      # percent
THROTTLE_OFF = 0.0
THROTTLE_TIME = 0.8 # seconds

def motor_thread(stopFlag):
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
            motor,      # param1: motor instance
            0,          # param2: throttle type (0 = percent)
            throttle_percent,
            seconds,
            0, 0, 0
        )

    while not stopFlag.is_set():
        if tracking.CV_RESULT == "RIGHT":
            for i in [0,1]:
                spin_motor(MOTOR_NUMBER[i], THROTTLE_ON, THROTTLE_TIME)
            for i in [2,3]:
                spin_motor(MOTOR_NUMBER[i], THROTTLE_OFF, THROTTLE_TIME)

        elif tracking.CV_RESULT == "LEFT":
            for i in [0,1]:
                spin_motor(MOTOR_NUMBER[i], THROTTLE_OFF, THROTTLE_TIME)
            for i in [2,3]:
                spin_motor(MOTOR_NUMBER[i], THROTTLE_ON, THROTTLE_TIME)

        else:
            for m in MOTOR_NUMBER:
                spin_motor(m, THROTTLE_OFF, THROTTLE_TIME)
        time.sleep(0.1)

    # stop all motors
    for m in MOTOR_NUMBER:
                spin_motor(m, THROTTLE_OFF, THROTTLE_TIME)
    print("All motors stopped")
