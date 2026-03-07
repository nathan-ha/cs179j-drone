
from pymavlink import mavutil
from drone import Drone
import time

drone = Drone()
drone.connect()
drone.set_mode("NOGPS") #its 20 rn so its nogps mode
drone.arm()


try:
    drone.set_mode("LAND")
    drone.dearm()
except KeyboardInterrupt:
    drone.set_mode("LAND")
    drone.dearm()

