
from pymavlink import mavutil
from drone import Drone
import time

drone = Drone()
drone.connect()

drone.set_mode("GUIDED")

try:
    drone.arm()
    drone.takeoff(2)
    time.sleep(15)
    drone.set_mode("LAND")
    drone.dearm()
except KeyboardInterrupt:
    drone.set_mode("LAND")
    drone.dearm()
# while True:
#     i = input("Enter an input:\n")
#     if i == "w":
#         drone.up()
#     elif i == "s":
#         drone.down()
#     elif i == "q":
#         drone.forward()
#     elif i == "e":
#         drone.backward()
#     elif i == "a":
#         drone.left()
#     elif i == "d":
#         drone.right()
#     elif i == "r":
#         drone.reset_to_center()
