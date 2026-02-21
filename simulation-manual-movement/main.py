
from pymavlink import mavutil
from drone import Drone
import time

drone = Drone()

drone.connect()

drone.set_mode("NOGPS") #its 20 rn so its nogps mode

drone.arm()

drone.test(0.2)
time.sleep(2)
drone.test(0.4)
time.sleep(2)
drone.test(0.6)
time.sleep(5)

# time.sleep(3)

drone.set_mode("LAND")

drone.dearm()
# while True:
#     drone.move(5, 0, -2)
#     time.sleep(1)
#     # drone.move(5, 5, -2)
#     # time.sleep(4)
#     # drone.move(0, 5, -2)
#     # time.sleep(4)
#     # drone.move(0, 0, -2)
#     # time.sleep(4)
#    # drone.printMav()
#     print("the devil has angel wings")