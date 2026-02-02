from pymavlink import mavutil
from connection import print_ack

def takeoff(the_connection, attitude):
    print("TAKEOFF")

    the_connection.mav.command_long_send(
        the_connection.target_system, 
        the_connection.target_component, 
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 
        0, 
        0, 0, 0, 0, 0, 0, 
        attitude)
    print_ack(the_connection)  

# | Mode             | ID |
# | ---------------- | -- |
# | **STABILIZE**    | 0  |
# | **ACRO**         | 1  |
# | **ALT_HOLD**     | 2  |
# | **AUTO**         | 3  |
# | **GUIDED**       | 4  |
# | **LOITER**       | 5  |
# | **RTL**          | 6  |
# | **CIRCLE**       | 7  |
# | **LAND**         | 9  |

modes = {
    "STABILIZE": 0,
    "ACRO": 1,
    "ALT_HOLD": 2,
    "AUTO": 3,
    "GUIDED": 4,
    "LOITER": 5,
    "RTL": 6,
    "CIRCLE": 7,
    "LAND": 9
}

# Bidirectional 
reverse_modes = {v: k for k, v in modes.items()}

# The mode either the ID or the string
def set_mode(the_connection, mode):
    if isinstance(mode, str):
        print("MODE:", mode)
        mode = modes[mode]
    else:
        print("MODE:", reverse_modes[mode])
    

    the_connection.mav.command_long_send(
    the_connection.target_system,
    the_connection.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode,                                               
    0, 0, 0, 0, 0
    )
    print_ack(the_connection)  




