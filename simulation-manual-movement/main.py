
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
    elif i == "q":
        drone.forward()
    elif i == "e":
        drone.backward()
    elif i == "a":
        drone.left()
    elif i == "d":
        drone.right()
    elif i == "r":
        drone.reset_to_center()