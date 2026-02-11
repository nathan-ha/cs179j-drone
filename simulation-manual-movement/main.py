
from pymavlink import mavutil
from drone import Drone
import time

drone = Drone()
drone.connect()

drone.set_mode("GUIDED")

drone.arm()
drone.takeoff(5)


while True:
    i = input()
    if i == "w":
        drone.up()
    elif i == "s":
        drone.down()