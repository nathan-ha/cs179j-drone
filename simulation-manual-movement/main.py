
from pymavlink import mavutil
from drone import Drone

drone = Drone()
drone.connect()
drone.arm()
drone.set_mode("GUIDED")
drone.takeoff(2)
drone.move()