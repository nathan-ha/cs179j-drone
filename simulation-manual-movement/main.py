
from pymavlink import mavutil
from connection import start_connection, print_ack
from arm import arm, dearm
from takeoff import takeoff, set_mode

cnt = start_connection()

set_mode(cnt, "GUIDED")

arm(cnt)

takeoff(cnt, 2)