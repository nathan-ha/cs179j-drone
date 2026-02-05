
from pymavlink import mavutil
from drone import Drone
import time

drone = Drone()
drone.connect()

drone.set_mode("GUIDED")

drone.arm()
drone.takeoff(2)
while True:
    drone.move(5, 0, -2)
    time.sleep(4)
    drone.move(5, 5, -2)
    time.sleep(4)
    drone.move(0, 5, -2)
    time.sleep(4)
    drone.move(0, 0, -2)
    time.sleep(4)
