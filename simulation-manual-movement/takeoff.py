from pymavlink import mavutil

# Start a connection listening on a UDP port

# MIGHT NEED TO CHANGE THIS FOR YOUR OWN DEVICE
the_connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')


# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

print("ARM")

# Target_system is the vehicle (drone in this case)
# Target components are peripherals
# The third param is the command to send to the drone
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)

print("TAKEOFF")

the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 5)

msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)
