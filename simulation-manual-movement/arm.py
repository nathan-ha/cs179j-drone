from pymavlink import mavutil
from connection import print_ack

def arm(the_connection):

    print("ARM")

    # Target_system is the vehicle (drone in this case)
    # Target components are peripherals
    # The third param is the command to send to the drone
    the_connection.mav.command_long_send(the_connection.target_system, 
    the_connection.target_component, 
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 
    0, 
    1, 
    0, 
    0, 0, 0, 0, 0)
    
    print_ack(the_connection)  


def dearm(the_connection):
    print("DEARM")
    the_connection.mav.command_long_send(the_connection.target_system, 
    the_connection.target_component, 
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 
    0, 
    0, 
    0, 
    0, 0, 0, 0, 0)
    print_ack(the_connection)  